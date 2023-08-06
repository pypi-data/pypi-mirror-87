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

from textwrap import dedent

import pytest
import strictyaml
import LbAPCommon

OPTIONAL_KEYS = [
    "root_in_tes",
    "simulation",
    "luminosity",
    "data_type",
    "input_type",
    "dddb_tag",
    "conddb_tag",
]


def test_good_no_defaults():
    rendered_yaml = dedent(
        """\
    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: /some/query
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 1
    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py", "$VAR/a.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is False
    assert data["job_1"]["turbo"] is False
    assert data["job_1"]["inform"] == "a.b@c.d"


@pytest.mark.parametrize(
    "value,expected",
    [
        ("FILETYPE.ROOT", ["FILETYPE.ROOT"]),
        ("filetype.root", ["FILETYPE.ROOT"]),
        ("filetype.ROOT", ["FILETYPE.ROOT"]),
        ("\n        - filetype.ROOT", ["FILETYPE.ROOT"]),
        (
            "\n        - filetype.ROOT\n        - filetype.dst",
            ["FILETYPE.ROOT", "FILETYPE.DST"],
        ),
    ],
)
def test_good_output_filetype_scalar(value, expected):
    rendered_yaml = dedent(
        """\
    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: /some/query
        output: {value}
        options:
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
    """.format(
            value=value
        )
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    LbAPCommon.validate_yaml(data, "a", "b")
    assert len(data) == 1

    assert data["job_1"]["output"] == expected

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["options"] == ["$VAR/a.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is False
    assert data["job_1"]["turbo"] is False
    assert data["job_1"]["inform"] == ["a.b@c.d"]


def test_good_with_defaults():
    rendered_yaml = dedent(
        """\
    defaults:
        wg: Charm
        automatically_configure: yes
        inform:
            - name@example.com

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        options:
            - options.py

    job_2:
        application: DaVinci/v44r0
        input:
            bk_query: "/some/other/query"
        output: FILETYPE.ROOT
        options:
            - other_options.py
        wg: B2OC
        automatically_configure: false
        inform:
            - other@example.com
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 2

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is True
    assert data["job_1"]["turbo"] is False
    assert data["job_1"]["inform"] == ["name@example.com"]

    assert data["job_2"]["application"] == "DaVinci/v44r0"
    assert data["job_2"]["input"] == {"bk_query": "/some/other/query"}
    assert data["job_2"]["output"] == "FILETYPE.ROOT"
    assert data["job_2"]["options"] == ["other_options.py"]
    assert data["job_2"]["wg"] == "B2OC"
    assert data["job_2"]["automatically_configure"] is False
    assert data["job_2"]["turbo"] is False
    assert data["job_2"]["inform"] == ["other@example.com"]


def test_good_all_turbo():
    rendered_yaml = dedent(
        """\
    defaults:
        wg: Charm
        automatically_configure: yes
        turbo: yes
        inform:
            - name@example.com

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        options:
            - options.py

    job_2:
        application: DaVinci/v44r0
        input:
            bk_query: "/some/other/query"
        output: FILETYPE.ROOT
        options:
            - other_options.py
        wg: B2OC
        automatically_configure: false
        inform:
            - other@example.com

    job_3:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        turbo: no
        options:
            - options.py
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 3

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is True
    assert data["job_1"]["turbo"] is True
    assert data["job_1"]["inform"] == ["name@example.com"]

    assert data["job_2"]["application"] == "DaVinci/v44r0"
    assert data["job_2"]["input"] == {"bk_query": "/some/other/query"}
    assert data["job_2"]["output"] == "FILETYPE.ROOT"
    assert data["job_2"]["options"] == ["other_options.py"]
    assert data["job_2"]["wg"] == "B2OC"
    assert data["job_2"]["automatically_configure"] is False
    assert data["job_2"]["turbo"] is True
    assert data["job_2"]["inform"] == ["other@example.com"]

    assert data["job_3"]["application"] == "DaVinci/v45r3"
    assert data["job_3"]["input"] == {"bk_query": "/some/query"}
    assert data["job_3"]["output"] == "FILETYPE.ROOT"
    assert data["job_3"]["options"] == ["options.py"]
    assert data["job_3"]["wg"] == "Charm"
    assert data["job_3"]["automatically_configure"] is True
    assert data["job_3"]["turbo"] is False
    assert data["job_3"]["inform"] == ["name@example.com"]

    for key in OPTIONAL_KEYS:
        for job in ["job_1", "job_2", "job_3"]:
            assert key not in data[job]


def test_good_some_turbo():
    rendered_yaml = dedent(
        """\
    defaults:
        wg: Charm
        automatically_configure: yes
        turbo: no
        inform:
            - name@example.com

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        options:
            - options.py

    job_2:
        application: DaVinci/v44r0
        input:
            bk_query: "/some/other/query"
        output: FILETYPE.ROOT
        options:
            - other_options.py
        wg: B2OC
        automatically_configure: false
        inform:
            - other@example.com

    job_3:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        turbo: yes
        options:
            - options.py
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 3

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is True
    assert data["job_1"]["turbo"] is False
    assert data["job_1"]["inform"] == ["name@example.com"]

    assert data["job_2"]["application"] == "DaVinci/v44r0"
    assert data["job_2"]["input"] == {"bk_query": "/some/other/query"}
    assert data["job_2"]["output"] == "FILETYPE.ROOT"
    assert data["job_2"]["options"] == ["other_options.py"]
    assert data["job_2"]["wg"] == "B2OC"
    assert data["job_2"]["automatically_configure"] is False
    assert data["job_2"]["turbo"] is False
    assert data["job_2"]["inform"] == ["other@example.com"]

    assert data["job_3"]["application"] == "DaVinci/v45r3"
    assert data["job_3"]["input"] == {"bk_query": "/some/query"}
    assert data["job_3"]["output"] == "FILETYPE.ROOT"
    assert data["job_3"]["options"] == ["options.py"]
    assert data["job_3"]["wg"] == "Charm"
    assert data["job_3"]["automatically_configure"] is True
    assert data["job_3"]["turbo"] is True
    assert data["job_3"]["inform"] == ["name@example.com"]

    for key in OPTIONAL_KEYS:
        for job in ["job_1", "job_2", "job_3"]:
            assert key not in data[job]


def test_good_automatically_configure_overrides():
    rendered_yaml = dedent(
        """\
    defaults:
        wg: Charm
        automatically_configure: yes
        turbo: no
        inform:
            - name@example.com

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        options:
            - options.py

    job_2:
        application: DaVinci/v44r0
        input:
            bk_query: "/some/other/query"
        output: FILETYPE.ROOT
        options:
            - other_options.py
        wg: B2OC
        automatically_configure: false
        inform:
            - other@example.com

    job_3:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        turbo: yes
        options:
            - options.py
        root_in_tes: "/Event/Charm"
        simulation: yes
        luminosity: no
        data_type: "2018"
        input_type: "DST"
        dddb_tag: "xyz-234"
        conddb_tag: "abc-def-20u"
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 3

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is True
    assert data["job_1"]["turbo"] is False
    assert data["job_1"]["inform"] == ["name@example.com"]
    for key in OPTIONAL_KEYS:
        assert key not in data["job_1"]

    assert data["job_2"]["application"] == "DaVinci/v44r0"
    assert data["job_2"]["input"] == {"bk_query": "/some/other/query"}
    assert data["job_2"]["output"] == "FILETYPE.ROOT"
    assert data["job_2"]["options"] == ["other_options.py"]
    assert data["job_2"]["wg"] == "B2OC"
    assert data["job_2"]["automatically_configure"] is False
    assert data["job_2"]["turbo"] is False
    assert data["job_2"]["inform"] == ["other@example.com"]

    assert data["job_3"]["application"] == "DaVinci/v45r3"
    assert data["job_3"]["input"] == {"bk_query": "/some/query"}
    assert data["job_3"]["output"] == "FILETYPE.ROOT"
    assert data["job_3"]["options"] == ["options.py"]
    assert data["job_3"]["wg"] == "Charm"
    assert data["job_3"]["automatically_configure"] is True
    assert data["job_3"]["turbo"] is True
    assert data["job_3"]["inform"] == ["name@example.com"]

    assert data["job_3"]["root_in_tes"] == "/Event/Charm"
    assert data["job_3"]["simulation"] is True
    assert data["job_3"]["luminosity"] is False
    assert data["job_3"]["data_type"] == "2018"
    assert data["job_3"]["input_type"] == "DST"
    assert data["job_3"]["dddb_tag"] == "xyz-234"
    assert data["job_3"]["conddb_tag"] == "abc-def-20u"


def test_good_automatically_configure_defaults_overrides():
    rendered_yaml = dedent(
        """\
    defaults:
        wg: Charm
        automatically_configure: yes
        turbo: no
        inform:
            - name@example.com
        root_in_tes: "/Event/Charm"
        simulation: yes
        luminosity: no
        data_type: "2018"
        input_type: "DST"
        dddb_tag: "xyz-234"
        conddb_tag: "abc-def-20u"

    job_1:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        options:
            - options.py

    job_2:
        application: DaVinci/v44r0
        input:
            bk_query: "/some/other/query"
        output: FILETYPE.ROOT
        options:
            - other_options.py
        wg: B2OC
        automatically_configure: false
        inform:
            - other@example.com

    job_3:
        application: DaVinci/v45r3
        input:
            bk_query: "/some/query"
        output: FILETYPE.ROOT
        turbo: yes
        options:
            - options.py
        root_in_tes: "/Event/Other"
        simulation: no
        luminosity: yes
        data_type: "2017"
        input_type: "MDST"
        dddb_tag: "tuv-345"
        conddb_tag: "ghj-20z"
    """
    )
    data = LbAPCommon.parse_yaml(rendered_yaml)
    assert len(data) == 3

    assert data["job_1"]["application"] == "DaVinci/v45r3"
    assert data["job_1"]["input"] == {"bk_query": "/some/query"}
    assert data["job_1"]["output"] == "FILETYPE.ROOT"
    assert data["job_1"]["options"] == ["options.py"]
    assert data["job_1"]["wg"] == "Charm"
    assert data["job_1"]["automatically_configure"] is True
    assert data["job_1"]["turbo"] is False
    assert data["job_1"]["inform"] == ["name@example.com"]

    assert data["job_2"]["application"] == "DaVinci/v44r0"
    assert data["job_2"]["input"] == {"bk_query": "/some/other/query"}
    assert data["job_2"]["output"] == "FILETYPE.ROOT"
    assert data["job_2"]["options"] == ["other_options.py"]
    assert data["job_2"]["wg"] == "B2OC"
    assert data["job_2"]["automatically_configure"] is False
    assert data["job_2"]["turbo"] is False
    assert data["job_2"]["inform"] == ["other@example.com"]

    for job in ["job_1", "job_2"]:
        assert data[job]["root_in_tes"] == "/Event/Charm"
        assert data[job]["simulation"] is True
        assert data[job]["luminosity"] is False
        assert data[job]["data_type"] == "2018"
        assert data[job]["input_type"] == "DST"
        assert data[job]["dddb_tag"] == "xyz-234"
        assert data[job]["conddb_tag"] == "abc-def-20u"

    assert data["job_3"]["application"] == "DaVinci/v45r3"
    assert data["job_3"]["input"] == {"bk_query": "/some/query"}
    assert data["job_3"]["output"] == "FILETYPE.ROOT"
    assert data["job_3"]["options"] == ["options.py"]
    assert data["job_3"]["wg"] == "Charm"
    assert data["job_3"]["automatically_configure"] is True
    assert data["job_3"]["turbo"] is True
    assert data["job_3"]["inform"] == ["name@example.com"]

    assert data["job_3"]["root_in_tes"] == "/Event/Other"
    assert data["job_3"]["simulation"] is False
    assert data["job_3"]["luminosity"] is True
    assert data["job_3"]["data_type"] == "2017"
    assert data["job_3"]["input_type"] == "MDST"
    assert data["job_3"]["dddb_tag"] == "tuv-345"
    assert data["job_3"]["conddb_tag"] == "ghj-20z"


@pytest.mark.parametrize(
    "missing_key", ["application", "input", "output", "wg", "inform"]
)
def test_bad_missing_key(missing_key):
    data = {
        "job_1": {
            "application": "DaVinci/v45r3",
            "input": {"bk_query": "/some/query"},
            "output": "FILETYPE.ROOT",
            "options": ["options.py"],
            "wg": "Charm",
            "inform": "a.b@c.d",
        }
    }
    del data["job_1"][missing_key]
    rendered_yaml = strictyaml.YAML(data).as_yaml()
    try:
        LbAPCommon.parse_yaml(rendered_yaml)
    except strictyaml.YAMLValidationError as e:
        assert "required key(s) '" + missing_key + "' not found" in str(e)


@pytest.mark.parametrize(
    "key,value",
    [
        ("application", "DaVinci"),
        ("input", "hello"),
        ("output", ""),
        ("wg", ""),
        ("inform", ""),
        ("automatically_configure", "null"),
        ("turbo", "absolutely"),
        ("root_in_tes", "DST"),
        ("simulation", "absolutely"),
        ("luminosity", "nope"),
        ("data_type", "MSDT"),
        ("input_type", "2016"),
        ("dddb_tag", ""),
        ("conddb_tag", ""),
    ],
)
def test_bad_invalid_value(key, value):
    data = {
        "job_1": {
            "application": "DaVinci/v45r3",
            "input": {"bk_query": "/some/query"},
            "output": "FILETYPE.ROOT",
            "options": ["options.py"],
            "wg": "Charm",
            "inform": "a.b@c.d",
        }
    }
    data["job_1"][key] = value
    rendered_yaml = strictyaml.YAML(data).as_yaml()
    with pytest.raises(strictyaml.YAMLValidationError, match=key + ":"):
        LbAPCommon.parse_yaml(rendered_yaml)
