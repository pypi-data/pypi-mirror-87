#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains tests for edit events.
"""
import pytest
import pandas as pd
import json
import random

from mitosheet.example import sheet
from mitosheet.tests.test_utils import create_mito_wrapper, create_mito_wrapper_dfs

from mitosheet.save_utils import write_analysis, read_analysis, read_saved_analysis_names

# We assume only column A exists
PERSIST_ANALYSIS_TESTS = [
    (0, '=0'),
    (1, '=1'),
    (2, '=A + 1'),
    ('APPLE', '=UPPER(\'apple\')'),
    (2, '=LEFT((A + 1) * 100)'),
    ('APPLE', '=UPPER(LOWER(UPPER(\'apple\')))')
]
@pytest.mark.parametrize("b_value,b_formula", PERSIST_ANALYSIS_TESTS)
def test_recover_analysis(b_value, b_formula):
    mito = create_mito_wrapper([1])
    mito.set_formula(b_formula, 0, 'B', add_column=True)
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df = pd.DataFrame(data={'A': [1]})
    new_mito = sheet(df)
    new_mito.receive_message(new_mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert curr_step['column_metatype'][0]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][0]['B'] == b_formula
    assert new_mito.widget_state_container.dfs[0]['B'].tolist() == [b_value]
    assert new_mito.column_spreadsheet_code_json == json.dumps(curr_step['column_spreadsheet_code'])


# We assume only column A exists
PERSIST_ANALYSIS_TESTS = [
    (0, '=0'),
    (1, '=1'),
    (2, '=A + 1'),
    ('APPLE', '=UPPER(\'apple\')'),
    (2, '=LEFT((A + 1) * 100)'),
    ('APPLE', '=UPPER(LOWER(UPPER(\'apple\')))')
]
@pytest.mark.parametrize("b_value,b_formula", PERSIST_ANALYSIS_TESTS)
def test_persist_analysis_multi_sheet(b_value, b_formula):
    mito = create_mito_wrapper([1], sheet_two_A_data=[1])
    mito.set_formula(b_formula, 0, 'B', add_column=True)
    mito.set_formula(b_formula, 1, 'B', add_column=True)
    # We first write out the analysis
    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})
    df2 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1, df2)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert curr_step['column_metatype'][0]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][0]['B'] == b_formula
    assert new_mito.widget_state_container.dfs[0]['B'].tolist() == [b_value]

    assert curr_step['column_metatype'][1]['B'] == 'formula'
    assert curr_step['column_spreadsheet_code'][1]['B'] == b_formula
    assert new_mito.widget_state_container.dfs[1]['B'].tolist() == [b_value]
    
    assert new_mito.column_spreadsheet_code_json == json.dumps(curr_step['column_spreadsheet_code'])


def test_persist_rename_column():
    mito = create_mito_wrapper([1])
    mito.rename_column(0, 'A', 'NEW_COLUMN')

    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert curr_step['dfs'][0].equals(pd.DataFrame(data={'NEW_COLUMN': [1]}))

def test_persisit_delete_column():
    mito = create_mito_wrapper([1])
    mito.delete_column(0, 'A')

    analysis_name = mito.mito_widget.analysis_name
    write_analysis(mito.mito_widget.widget_state_container)

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysis_name
    })

    curr_step = new_mito.widget_state_container.curr_step

    assert len(curr_step['dfs'][0].keys()) == 0


def test_save_analysis():
    mito = create_mito_wrapper([1])
    mito.add_column(0, 'B')
    mito.delete_column(0, 'A')

    random_name = 'UUID-test_save' + str(random.random())

    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': random_name
    })

    curr_step = new_mito.widget_state_container.curr_step
    assert curr_step['dfs'][0].keys() == ['B']

def test_save_analysis_and_overwrite():
    mito = create_mito_wrapper([1])
    mito.add_column(0, 'B')

    random_name = 'UUID-test_save' + str(random.random())

    # Save it once
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    mito.delete_column(0, 'A')
    mito.delete_column(0, 'B')

    # Save it again
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    df1 = pd.DataFrame(data={'A': [1]})

    new_mito = sheet(df1)
    new_mito.receive_message(mito, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': random_name
    })

    curr_step = new_mito.widget_state_container.curr_step
    assert len(curr_step['dfs'][0].keys()) == 0

def test_saved_analysis_in_saved_analysis():
    mito = create_mito_wrapper([1])
    mito.add_column(0, 'B')

    random_name = 'test_save' + str(random.random())

    # Save it once
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    saved_analysis_names = read_saved_analysis_names()
    assert random_name in saved_analysis_names

def test_failed_replay_does_not_add_steps():
    # Make an analysis and save it
    mito = create_mito_wrapper([1])
    mito.set_formula('=A + 1', 0, 'B', add_column=True)
    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe it cannot be rerun on
    df = pd.DataFrame(data={'A': [1], 'B': [3]})
    new_mito = create_mito_wrapper_dfs(df)

    new_mito.mito_widget.receive_message(new_mito.mito_widget, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': random_name
    })

    # Make sure no step was added
    assert len(new_mito.mito_widget.widget_state_container.steps) == 1



def test_group_by_replays():
    # Make an analysis and save it
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    mito = create_mito_wrapper_dfs(df1)
    mito.group_sheet(
        0, 
        ['Name'],
        [],
        {'Height': 'sum'}
    )
    
    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe it cannot be rerun on
    df1 = pd.DataFrame(data={'Name': ['Nate', 'Nate'], 'Height': [4, 5]})
    new_mito = create_mito_wrapper_dfs(df1)

    new_mito.mito_widget.receive_message(new_mito.mito_widget, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': random_name
    })

    # Make sure no step was added
    wsc = new_mito.mito_widget.widget_state_container
    assert len(wsc.steps) == 2
    assert wsc.steps[1]['step_type'] == 'group'
    assert len(wsc.curr_step['dfs']) == 2
    assert wsc.curr_step['dfs'][1].equals(
        pd.DataFrame(data={'Name': ['Nate'], 'Height': [9]})
    )


def test_replay_analysis_does_not_make_removed_columns():
    df1 = pd.DataFrame(data={'A': [123], 'B': [1234]})
    mito = create_mito_wrapper_dfs(df1)

    mito.add_column(0, 'C')

    random_name = 'UUID-test_save' + str(random.random())
    mito.mito_widget.receive_message(mito.mito_widget, {
        'event': 'update_event',
        'type': 'save_analysis',
        'analysis_name': random_name
    })

    # Try and rerun it on a dataframe with no column B, and it shouldn't recreate B
    df1 = pd.DataFrame(data={'A': [123]})
    new_mito = create_mito_wrapper_dfs(df1)

    new_mito.mito_widget.receive_message(new_mito.mito_widget, {
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': random_name
    })

    assert list(new_mito.mito_widget.widget_state_container.dfs[0].keys()) == ['A', 'C']

