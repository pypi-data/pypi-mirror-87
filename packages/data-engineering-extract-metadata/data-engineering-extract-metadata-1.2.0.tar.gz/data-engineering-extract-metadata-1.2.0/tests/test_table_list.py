import os
import tests.mocked_responses as mocks

from pathlib import Path
from datetime import datetime
from tests import MockConnection
from data_engineering_extract_metadata.utils import read_json
from data_engineering_extract_metadata.table_list import (
    get_table_list,
    get_names_and_spaces,
    save_tables,
)

test_path = Path("./tests/data")


def test_get_table_list():
    """Checks that a fake filter function works, and that no filter function works"""

    def simple_filter(tables):
        """Example filter function for selecting tables by tablespace"""
        return [t[0] for t in tables if t[1].startswith("T_")]

    try:
        get_table_list(
            MockConnection([mocks.table_names, mocks.blob_list]),
            test_path,
            "unfiltered",
            "TEST_LIST",
            None,
        )
        output_unfiltered = read_json("unfiltered.json", test_path)
    finally:
        os.remove(test_path / "unfiltered.json")

    try:
        get_table_list(
            MockConnection([mocks.table_names, mocks.blob_list]),
            test_path,
            "filtered",
            "TEST_LIST",
            simple_filter,
        )
        output_filtered = read_json("filtered.json", test_path)
    finally:
        os.remove(test_path / "filtered.json")

    date_unfiltered = datetime.strptime(
        output_unfiltered["extraction_date"][:10], "%Y-%m-%d"
    ).date()
    date_filtered = datetime.strptime(
        output_filtered["extraction_date"][:10], "%Y-%m-%d"
    ).date()

    expected_unfiltered = read_json("table_list_unfiltered.json", test_path)
    expected_filtered = read_json("table_list_filtered.json", test_path)
    expected_date = datetime.now().date()

    assert output_unfiltered["tables_from"] == expected_unfiltered["tables_from"]
    assert output_filtered["tables_from"] == expected_filtered["tables_from"]

    assert date_unfiltered == expected_date
    assert date_filtered == expected_date

    assert output_unfiltered["tables"] == expected_unfiltered["tables"]
    assert output_filtered["tables"] == expected_filtered["tables"]

    assert output_unfiltered["blobs"] == expected_unfiltered["blobs"]
    assert output_filtered["blobs"] == expected_filtered["blobs"]


def test_get_names_and_spaces():
    """Checks that table names are pulled out of
    their tuples and listed with original capitalisation
    """
    result_no_tablespace = get_names_and_spaces(
        "TEST_DB", MockConnection([mocks.table_names]), False
    )
    result_tablespace = get_names_and_spaces(
        "TEST_DB", MockConnection([mocks.table_names]), True
    )

    assert result_no_tablespace == ["TEST_TABLE1", "TEST_TABLE2", "CUSTODY_HISTORY"]
    assert result_tablespace == [
        ("TEST_TABLE1", "T_DATA"),
        ("TEST_TABLE2", "T_DOCUMENT_DATA"),
        ("CUSTODY_HISTORY", "USERS"),
    ]


def test_save_tables():
    """Tests json file is created with correct content"""
    try:
        save_tables(
            "unfiltered", test_path, ["TEST_TABLE1", "TEST_TABLE2", "CUSTODY_HISTORY"]
        )
        output = read_json("unfiltered.json", test_path)
    finally:
        os.remove(test_path / "unfiltered.json")

    expected = read_json("table_list_unfiltered.json", test_path)
    output_date = datetime.strptime(output["extraction_date"][:10], "%Y-%m-%d").date()

    assert output["tables_from"] == expected["tables_from"]
    assert output["tables"] == expected["tables"]
    assert output_date == datetime.now().date()
