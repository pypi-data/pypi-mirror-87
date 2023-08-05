"""Test functions for Airtable interface functionality.
"""
import os

import airtable
from aracnid_api import AirtableInterface


DATETIME_TEST_STR = '2020-08-05T12:00:00-04:00'

def test_init_airtable():
    """Test that Airtable Interface was imported successfully.
    """
    base_id = os.environ.get('AIRTABLE_TEST_BASE_ID')
    air = AirtableInterface(base_id=base_id)
    assert air

def test_get_table():
    """Tests retrieving table.
    """
    base_id = os.environ.get('AIRTABLE_TEST_BASE_ID')
    air = AirtableInterface(base_id=base_id)

    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    assert table
    assert isinstance(table, airtable.airtable.Airtable)

def test_get_airtable_datetime():
    """Tests the datetime processing of Airtable Interface.
    """
    base_id = os.environ.get('AIRTABLE_TEST_BASE_ID')
    air = AirtableInterface(base_id=base_id)

    table_name = 'test_date'
    table = air.get_table(table_name=table_name)

    record_id = 'recuaPzY7QvSbysW1'
    record = table.get(record_id)

    assert record
    dtetime = air.get_airtable_datetime(record, 'datetime_field')
    assert dtetime.isoformat() == DATETIME_TEST_STR
