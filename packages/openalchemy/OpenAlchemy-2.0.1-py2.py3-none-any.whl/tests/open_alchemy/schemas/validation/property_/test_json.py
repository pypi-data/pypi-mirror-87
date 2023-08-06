"""Tests for JSON property validation."""

import pytest

from open_alchemy.schemas.validation.property_ import json

CHECK_TESTS = [
    pytest.param({}, {}, (True, None), id="empty"),
    pytest.param(
        {"nullable": "False"},
        {},
        (False, "malformed schema :: A nullable value must be of type boolean. "),
        id="malformed nullable",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"nullable": "True"},
            ]
        },
        {"RefSchema": {"nullable": True}},
        (False, "malformed schema :: A nullable value must be of type boolean. "),
        id="integer nullable prefer local not boolean",
    ),
    pytest.param(
        {"description": True},
        {},
        (False, "malformed schema :: A description value must be of type string. "),
        id="malformed description",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"description": True},
            ]
        },
        {"RefSchema": {"description": "description 1"}},
        (False, "malformed schema :: A description value must be of type string. "),
        id="integer description prefer local not string",
    ),
    pytest.param(
        {"readOnly": "False"},
        {},
        (False, "malformed schema :: A readOnly property must be of type boolean. "),
        id="malformed readOnly",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"readOnly": "True"},
            ]
        },
        {"RefSchema": {"readOnly": True}},
        (False, "malformed schema :: A readOnly property must be of type boolean. "),
        id="integer readOnly prefer local not boolean",
    ),
    pytest.param(
        {"writeOnly": "False"},
        {},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="malformed writeOnly",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"writeOnly": "True"},
            ]
        },
        {"RefSchema": {"writeOnly": True}},
        (False, "malformed schema :: A writeOnly property must be of type boolean. "),
        id="integer writeOnly prefer local not boolean",
    ),
    pytest.param(
        {"x-index": "False"},
        {},
        (False, "malformed schema :: A index value must be of type boolean. "),
        id="malformed x-index",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-index": "True"},
            ]
        },
        {"RefSchema": {"x-index": True}},
        (False, "malformed schema :: A index value must be of type boolean. "),
        id="integer x-index prefer local not boolean",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {},
        (False, "reference :: 'RefSchema was not found in schemas.' "),
        id="$ref miss",
    ),
    pytest.param(
        {"$ref": "#/components/schemas/RefSchema"},
        {"RefSchema": {"x-index": "False"}},
        (False, "malformed schema :: A index value must be of type boolean. "),
        id="$ref malformed x-index",
    ),
    pytest.param(
        {"allOf": [{"x-index": "False"}]},
        {},
        (False, "malformed schema :: A index value must be of type boolean. "),
        id="allOf malformed x-index",
    ),
    pytest.param({"x-index": True}, {}, (True, None), id="x-index"),
    pytest.param(
        {"x-unique": "False"},
        {},
        (False, "malformed schema :: A unique value must be of type boolean. "),
        id="malformed x-unique",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-unique": "True"},
            ]
        },
        {"RefSchema": {"x-unique": True}},
        (False, "malformed schema :: A unique value must be of type boolean. "),
        id="integer x-unique prefer local not boolean",
    ),
    pytest.param({"x-unique": True}, {}, (True, None), id="x-unique"),
    pytest.param(
        {"x-primary-key": "False"},
        {},
        (
            False,
            "malformed schema :: The x-primary-key property must be of type boolean. ",
        ),
        id="malformed x-primary-key",
    ),
    pytest.param(
        {
            "allOf": [
                {"$ref": "#/components/schemas/RefSchema"},
                {"x-primary-key": "True"},
            ]
        },
        {"RefSchema": {"x-primary-key": True}},
        (
            False,
            "malformed schema :: The x-primary-key property must be of type boolean. ",
        ),
        id="integer x-primary-key prefer local not boolean",
    ),
    pytest.param({"x-primary-key": True}, {}, (True, None), id="x-primary-key"),
    pytest.param(
        {"x-autoincrement": "False"},
        {},
        (False, "json properties do not support x-autoincrement"),
        id="x-autoincrement defined",
    ),
    pytest.param(
        {"x-server-default": "False"},
        {},
        (False, "json properties do not support x-server-default"),
        id="x-server-default defined",
    ),
    pytest.param(
        {"x-foreign-key": True},
        {},
        (
            False,
            "malformed schema :: The x-foreign-key property must be of type string. ",
        ),
        id="x-foreign-key not string",
    ),
    pytest.param(
        {"x-foreign-key": "foreign.key"},
        {},
        (True, None),
        id="x-foreign-key not string",
    ),
    pytest.param(
        {"type": "integer", "x-kwargs": {"nullable": True}},
        {},
        (False, "x-kwargs :: may not contain the nullable key"),
        id="x-kwargs has nullable",
    ),
    pytest.param(
        {"x-foreign-key-kwargs": {"key": "value"}},
        {},
        (False, "x-foreign-key-kwargs :: can only be defined alongside x-foreign-key"),
        id="x-foreign-key-kwargs without x-foreign-key",
    ),
]


@pytest.mark.parametrize("schema, schemas, expected_result", CHECK_TESTS)
@pytest.mark.schemas
@pytest.mark.validate
def test_check(schema, schemas, expected_result):
    """
    GIVEN schemas, schema and the expected result
    WHEN check is called with the schemas schema
    THEN the expected result is returned.
    """
    returned_result = json.check(schemas, schema)

    assert returned_result == expected_result
