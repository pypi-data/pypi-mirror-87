###############################################################################
# (c) Copyright 2020 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
from os.path import relpath, isfile, join
import re
import yaml
import jinja2
from strictyaml import (
    Any,
    Bool,
    Enum,
    load,
    Map,
    MapPattern,
    Optional,
    Regex,
    Seq,
    Str,
)

from LbAPCommon import config

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

RE_APPLICATION = r"^([A-Za-z]+/)+v\d+r\d+(p\d+)?"
RE_JOB_NAME = r"^[a-zA-Z0-9][a-zA-Z0-9_\-]+$"
RE_OUTPUT_FILE_TYPE = r"^([A-Za-z][A-Za-z0-9_]+\.)+((ROOT|root)|.?(DST|dst))$"
RE_OPTIONS_FN = r"^\$?[a-zA-Z0-9/\.\-\+\=_]+$"
RE_INFORM = r"^(?:[a-zA-Z]{3,}|[^@\s]+@[^@\s]+\.[^@\s]+)$"

RE_ROOT_IN_TES = r"^\/.+$"
RE_DDDB_TAG = r"^.{1,50}$"
RE_CONDDB_TAG = r"^.{1,50}$"

BASE_JOB_SCHEMA = {
    "application": Regex(RE_APPLICATION),
    "input": MapPattern(Str(), Any()),
    "output": Regex(RE_OUTPUT_FILE_TYPE) | Seq(Regex(RE_OUTPUT_FILE_TYPE)),
    "options": Regex(RE_OPTIONS_FN) | Seq(Regex(RE_OPTIONS_FN)),
    "wg": Enum(config.known_working_groups),
    "inform": Regex(RE_INFORM) | Seq(Regex(RE_INFORM)),
    # Automatic configuration
    "automatically_configure": Bool(),
    "turbo": Bool(),
    Optional("root_in_tes"): Regex(RE_ROOT_IN_TES),
    Optional("simulation"): Bool(),
    Optional("luminosity"): Bool(),
    Optional("data_type"): Enum(config.known_data_types),
    Optional("input_type"): Enum(config.known_input_types),
    Optional("dddb_tag"): Regex(RE_DDDB_TAG),
    Optional("conddb_tag"): Regex(RE_CONDDB_TAG),
}
DEFAULT_JOB_VALUES = {
    "automatically_configure": False,
    "turbo": False,
}


def _ordered_dict_to_dict(a):
    if isinstance(a, (OrderedDict, dict)):
        return {k: _ordered_dict_to_dict(v) for k, v in a.items()}
    elif isinstance(a, (list, tuple)):
        return [_ordered_dict_to_dict(v) for v in a]
    else:
        return a


def render_yaml(raw_yaml):
    try:
        rendered_yaml = jinja2.Template(
            raw_yaml, undefined=jinja2.StrictUndefined
        ).render()
    except jinja2.TemplateError as e:
        raise ValueError(
            "Failed to render with jinja2 on line %s: %s"
            % (getattr(e, "lineno", "unknown"), e)
        )
    return rendered_yaml


def parse_yaml(rendered_yaml):
    data1 = load(
        rendered_yaml, schema=MapPattern(Regex(RE_JOB_NAME), Any(), minimum_keys=1)
    )

    if "defaults" in data1:
        defaults_schema = {}
        for key, value in BASE_JOB_SCHEMA.items():
            if isinstance(key, Optional):
                key = key.key
            key = Optional(key, default=DEFAULT_JOB_VALUES.get(key))
            defaults_schema[key] = value

        data1["defaults"].revalidate(Map(defaults_schema))
        defaults = data1.data["defaults"]
        # Remove the defaults data from the snippet
        del data1["defaults"]
    else:
        defaults = DEFAULT_JOB_VALUES.copy()

    job_names = list(data1.data.keys())
    if len(set(n.lower() for n in job_names)) != len(job_names):
        raise ValueError(
            "Found multiple jobs with the same name but different capitalisation"
        )

    job_name_schema = Regex(r"(" + r"|".join(map(re.escape, job_names)) + r")")

    # StrictYAML has non-linear complexity when parsing many keys
    # Avoid extremely slow parsing by doing each key individually
    data2 = {}
    for k, v in data1.items():
        k = k.data
        v = _ordered_dict_to_dict(v.data)

        production_schema = {}
        for key, value in BASE_JOB_SCHEMA.items():
            if isinstance(key, Optional):
                key = key.key
                production_schema[Optional(key, default=defaults.get(key))] = value
            elif key in defaults:
                production_schema[Optional(key, default=defaults[key])] = value
            else:
                production_schema[key] = value

        data2.update(
            load(
                yaml.safe_dump({k: v}),
                MapPattern(job_name_schema, Map(production_schema), minimum_keys=1),
            ).data
        )

    return data2


def validate_yaml(data, repo_root, prod_name):
    # Ensure all values that cam be either a list or a string are lists of strings
    for job_data in data.values():
        for prop in ["output", "options", "inform"]:
            if not isinstance(job_data[prop], list):
                job_data[prop] = [job_data[prop]]
        job_data["output"] = [s.upper() for s in job_data["output"]]

    # Normalise the options filenames
    for job_data in data.values():
        normalised_options = []
        for fn in job_data["options"]:
            if fn.startswith("$"):
                normalised_options.append(fn)
                continue

            fn_normed = relpath(join(repo_root, fn), start=repo_root)
            if fn_normed.startswith("../"):
                raise ValueError("{} not found inside {}".format(fn, repo_root))
            if not isfile(join(repo_root, prod_name, fn_normed)):
                raise FileNotFoundError(isfile(join(repo_root, prod_name, fn_normed)))
            normalised_options.append(
                join("$ANALYSIS_PRODUCTIONS_BASE", prod_name, fn_normed)
            )
        job_data["options"] = normalised_options
