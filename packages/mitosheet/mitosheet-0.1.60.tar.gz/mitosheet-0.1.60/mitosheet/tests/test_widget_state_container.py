#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

import pandas as pd
import pytest

from mitosheet.errors import EditError
from mitosheet.widget_state_container import WidgetStateContainer
from mitosheet.steps.add_column import execute_add_column_step


def test_create_widget_state_container():
    df = pd.DataFrame(data={'A': [123]})
    wsc = WidgetStateContainer([df])
    assert wsc.curr_step_id == 0
    
    assert wsc.curr_step['step_type'] == 'initialize'
    assert wsc.curr_step['column_metatype'] == [{'A': 'value'}]
    assert wsc.curr_step['column_spreadsheet_code'] == [{'A': ''}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}]
    assert wsc.curr_step['column_evaluation_graph'] == [{'A': set()}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}]
    assert wsc.curr_step['dfs'][0].equals(df)

def test_create_widget_state_container_multiple_dfs():
    df1 = pd.DataFrame(data={'A': [123]})
    df2 = pd.DataFrame(data={'A': [123]})

    wsc = WidgetStateContainer([df1, df2])
    assert wsc.curr_step_id == 0
    assert wsc.curr_step['step_type'] == 'initialize'
    assert wsc.curr_step['column_metatype'] == [{'A': 'value'}, {'A': 'value'}]
    assert wsc.curr_step['column_spreadsheet_code'] == [{'A': ''}, {'A': ''}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}, {'A': ''}]
    assert wsc.curr_step['column_evaluation_graph'] == [{'A': set()}, {'A': set()}]
    assert wsc.curr_step['column_python_code'] == [{'A': ''}, {'A': ''}]
    assert wsc.curr_step['dfs'][0].equals(df1)
    assert wsc.curr_step['dfs'][1].equals(df2)

# We assume only column A exists
CELL_EDIT_ERRORS = [
    ('=HI()', 'unsupported_function_error'),
    ('=UPPER(HI())', 'unsupported_function_error'),
    ('=UPPER(HI())', 'unsupported_function_error'),
    ('=C', 'no_column_error'),
    ('=C + D', 'no_column_error'),
    ('=ABCDEFG', 'no_column_error'),
    ('=UPPER(C)', 'no_column_error'),
    ('UPPER(A)', 'invalid_formula_error'),
    ('10', 'invalid_formula_error'),
    ('=B', 'circular_reference_error'),
    ('=UPPER(A, 100)', 'execution_error'),
    ('=UPPER(LOWER(A, 100))', 'execution_error')
]

@pytest.mark.parametrize("formula,error_type", CELL_EDIT_ERRORS)
def test_widget_state_container_cell_edit_errors(formula,error_type):
    df = pd.DataFrame(data={'A': [123]})
    wsc = WidgetStateContainer([df])
    execute_add_column_step(wsc, 0, 'B')
    with pytest.raises(EditError) as e_info:
        wsc.handle_edit_event({
            'event': 'edit_event',
            'type': 'set_column_formula_edit',
            'sheet_index': 0,
            'column_header': 'B',
            'old_formula': '=0',
            'new_formula': formula
        })
    assert e_info.value.type_ == error_type

def test_column_exists_error():
    df = pd.DataFrame(data={'A': [123]})
    wsc = WidgetStateContainer([df])
    execute_add_column_step(wsc, 0, 'B')
    with pytest.raises(EditError) as e_info:
        execute_add_column_step(wsc, 0, 'B')
    assert e_info.value.type_ == 'column_exists_error'

def test_wrong_column_metatype():
    df = pd.DataFrame(data={'A': [123]})
    wsc = WidgetStateContainer([df])
    execute_add_column_step(wsc, 0, 'B')
    with pytest.raises(EditError) as e_info:
        wsc.handle_edit_event({
            'event': 'edit_event',
            'type': 'set_column_formula_edit',
            'sheet_index': 0,
            'column_header': 'A',
            'old_formula': '=0',
            'new_formula': '=1'
        })
    assert e_info.value.type_ == 'wrong_column_metatype_error'

