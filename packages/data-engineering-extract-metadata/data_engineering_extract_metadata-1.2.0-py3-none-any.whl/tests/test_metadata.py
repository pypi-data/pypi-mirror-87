import os
import tests.mocked_responses as mocks

from pathlib import Path
from tests import MockConnection, MockCursor
from data_engineering_extract_metadata.utils import read_json
from data_engineering_extract_metadata.metadata import (
    create_json_for_database,
    create_json_for_tables,
    get_table_meta,
    get_primary_keys,
    get_partitions,
    get_subpartitions,
    find_not_nullable,
)

test_path = Path("./tests/data")


def test_create_json_for_database():
    """Tests json file is created with correct content"""
    try:
        create_json_for_database(
            "This is a database",
            "test_database",
            "bucket-name",
            "hmpps/delius/DELIUS_APP_SCHEMA",
            test_path,
        )
        output = read_json("database.json", test_path)
    finally:
        os.remove(test_path / "database.json")

    expected = read_json("database_expected.json", test_path)

    assert output == expected


def test_create_json_for_tables():
    """Tests that the correct json is created for multiple tables"""
    # List of query responses. Empty dicts are for primary key & partition queries
    responses = [
        mocks.test_constraints,
        mocks.first_table,
        {},
        {},
        mocks.second_table,
        {},
        {},
    ]
    try:
        create_json_for_tables(
            tables=["TEST_TABLE1", "TEST_TABLE2"],
            schema="TEST_DB",
            location=test_path,
            include_op_column=True,
            include_timestamp_column=True,
            include_derived_columns=False,
            include_objects=False,
            connection=MockConnection(responses),
        )
        output1 = read_json("test_table1.json", test_path)
        output2 = read_json("test_table2.json", test_path)

    finally:
        os.remove(test_path / "test_table1.json")
        os.remove(test_path / "test_table2.json")

    expected1 = read_json("table1_expected.json", test_path)
    expected2 = read_json("table2_expected.json", test_path)

    assert output1 == expected1
    assert output2 == expected2


def test_get_table_meta():
    """Tests option flags, document_history tables and data type conversion
    Partitions and primary key fields tested separately

    This function receives a cursor that's already had .execute run
    This means it should already have a description and data if needed

    That's why MockCursors used here are initialised with the description parameter
    """
    # All flag parameters set to False
    output_no_flags = get_table_meta(
        MockCursor(description=mocks.first_table["desc"]),
        table="TEST_TABLE1",
        not_nullable=["test_id", "test_number"],
        include_op_column=False,
        include_timestamp_column=False,
        include_derived_columns=False,
        include_objects=False,
    )
    columns_no_flags = [
        {
            "name": "test_number",
            "type": "decimal(38,0)",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_id",
            "type": "decimal(38,10)",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_date",
            "type": "datetime",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_varchar",
            "type": "character",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_flag",
            "type": "character",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_raw",
            "type": "binary",
            "description": "",
            "nullable": True,
        }
    ]
    expected_no_flags = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": "test_table1",
        "description": "",
        "data_format": "parquet",
        "columns": columns_no_flags,
        "location": "TEST_TABLE1/",
        "partitions": None,
        "primary_key": None,
    }

    # All parameter flags set to True
    output_all_flags = get_table_meta(
        MockCursor(description=mocks.first_table["desc"]),
        table="TEST_TABLE1",
        not_nullable=["test_flag", "test_varchar"],
        include_op_column=True,
        include_timestamp_column=True,
        include_derived_columns=True,
        include_objects=True,
    )
    columns_all_flags = [
        {
            "name": "op",
            "type": "character",
            "description": "Type of change, for rows added by ongoing replication.",
            "nullable": True,
            "enum": ["I", "U", "D"],
        },
        {
            "name": "extraction_timestamp",
            "type": "datetime",
            "description": "DMS extraction timestamp",
            "nullable": False,
        },
        {
            "name": "test_number",
            "type": "decimal(38,0)",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_id",
            "type": "decimal(38,10)",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_date",
            "type": "datetime",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_varchar",
            "type": "character",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_flag",
            "type": "character",
            "description": "",
            "nullable": False,
        },
        {
            "name": "test_raw",
            "type": "binary",
            "description": "",
            "nullable": True,
        },
        {
            "name": "test_object_skip",
            "type": "array<character>",
            "description": "",
            "nullable": True,
        },
        {
            "name": "mojap_current_record",
            "type": "boolean",
            "description": "If the record is current",
            "nullable": False,
        },
        {
            "name": "mojap_start_datetime",
            "type": "datetime",
            "description": "When the record became current",
            "nullable": False,
        },
        {
            "name": "mojap_end_datetime",
            "type": "datetime",
            "description": "When the record ceased to be current",
            "nullable": False,
        },
    ]
    expected_all_flags = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": "test_table1",
        "description": "",
        "data_format": "parquet",
        "columns": columns_all_flags,
        "location": "TEST_TABLE1/",
        "partitions": None,
        "primary_key": None,
    }

    # DOCUMENT_HISTORY table
    output_doc_history = get_table_meta(
        MockCursor(description=mocks.doc_history["desc"]),
        table="DOCUMENT_HISTORY",
        not_nullable=[],
        include_op_column=False,
        include_timestamp_column=False,
        include_derived_columns=False,
        include_objects=False,
    )
    columns_doc_history = [
        {
            "name": "test_id",
            "type": "decimal(38,10)",
            "description": "",
            "nullable": True,
        },
        {
            "name": "mojap_document_path",
            "type": "character",
            "description": "The path to the document",
            "nullable": True,
        },
    ]
    expected_doc_history = {
        "$schema": (
            "https://moj-analytical-services.github.io/metadata_schema/table/"
            "v1.4.0.json"
        ),
        "name": "document_history",
        "description": "",
        "data_format": "parquet",
        "columns": columns_doc_history,
        "location": "DOCUMENT_HISTORY/",
        "partitions": None,
        "primary_key": None,
    }

    assert output_no_flags == expected_no_flags
    assert output_all_flags == expected_all_flags
    assert output_doc_history == expected_doc_history


def test_get_primary_keys():
    """Tests that primary key output is formatted correctly
    Doesn't check that the SQL results are right
    """
    output_key = get_primary_keys("TEST_TABLE_KEY", MockCursor([mocks.primary_key]))
    output_keys = get_primary_keys("TEST_TABLE_KEYS", MockCursor([mocks.primary_keys]))
    output_no_keys = get_primary_keys("TEST_TABLE_NO_KEYS", MockCursor())

    expected_key = [
        "long_postcode_id",
    ]
    expected_keys = ["long_postcode_id", "team_id"]
    expected_no_keys = None

    assert output_key == expected_key
    assert output_keys == expected_keys
    assert output_no_keys == expected_no_keys


def test_get_partitions():
    """Tests that partitions are returned correctly.
    Subpartitions are tested separately.
    """
    output_partition = get_partitions("PARTITION_TEST", MockCursor([mocks.partition]))
    output_partitions = get_partitions(
        "PARTITIONS_TEST", MockCursor([mocks.partitions])
    )
    output_no_partitions = get_partitions("NO_PARTITIONS_TEST", MockCursor())

    expected_partition = [{"name": "P_ADDITIONAL_IDENTIFIER", "subpartitions": None}]
    expected_partitions = [
        {"name": "P_ADDITIONAL_IDENTIFIER", "subpartitions": None},
        {"name": "P_ADDITIONAL_OFFENCE", "subpartitions": None},
        {"name": "P_ADDITIONAL_SENTENCE", "subpartitions": None},
        {"name": "P_ADDRESS", "subpartitions": None},
        {"name": "P_ADDRESS_ASSESSMENT", "subpartitions": None},
        {"name": "P_ALIAS", "subpartitions": None},
        {"name": "P_APPROVED_PREMISES_REFERRAL", "subpartitions": None},
    ]
    expected_no_partitions = None

    assert output_partition == expected_partition
    assert output_partitions == expected_partitions
    assert output_no_partitions == expected_no_partitions


def test_get_subpartitions():
    output_subpartition = get_subpartitions(
        table="SUBPARTITION_TABLE",
        partition="SUBPARTITION",
        cursor=MockCursor([mocks.subpartition]),
    )
    output_subpartitions = get_subpartitions(
        table="SUBPARTITIONS_TABLE",
        partition="SUBPARTITIONS",
        cursor=MockCursor([mocks.subpartitions]),
    )
    output_no_subpartitions = get_subpartitions(
        table="NO_SUBPARTITIONS_TABLE",
        partition="NO_SUBPARTITIONS",
        cursor=MockCursor(),
    )

    expected_subpartition = ["SUBPARTITION_A"]
    expected_subpartitions = [
        "SUBPARTITION_A",
        "SUBPARTITION_B",
        "SUBPARTITION_C",
        "SUBPARTITION_D",
    ]
    expected_no_subpartitions = []

    assert output_subpartition == expected_subpartition
    assert output_subpartitions == expected_subpartitions
    assert output_no_subpartitions == expected_no_subpartitions


def test_find_not_nullable():
    output = find_not_nullable(MockCursor([mocks.test_constraints]), "TEST_SCHEMA")
    assert output == {
        "test_table1": ["test_number", "test_id"],
        "test_table2": ["message_crn", "incident_id"],
        "table_not_present": ["no_data"],
    }
