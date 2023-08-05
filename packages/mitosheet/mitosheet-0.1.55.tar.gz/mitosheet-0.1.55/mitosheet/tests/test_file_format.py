#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains tests for edit events.
"""
from typing import List

from mitosheet.steps import ADD_COLUMN_STEP, STEPS
from mitosheet.steps import DELETE_COLUMN_STEP
from mitosheet.steps import RENAME_COLUMN_STEP
from mitosheet.steps import FILTER_STEP
from mitosheet.steps import GROUP_STEP
from mitosheet.steps import MERGE_STEP
from mitosheet.steps import REORDER_COLUMN_STEP
from mitosheet.steps import SET_COLUMN_FORMULA_STEP


def check_step(
        step_definition, 
        step_version: int, 
        step_type: str, 
        params: List[str]
    ):
    """
    Helper function that checks a given step definition against the 
    expected step_version, step_type, and params for that step. 

    Throws an assertion error if any of them do not match! 
    """
    assert step_definition['step_version'] == step_version
    assert step_definition['step_type'] == step_type
    assert step_definition['params'] == params

def test_params_static():
    """
    NOTE: This is a regression test! Before changing this test to make it pass, talk to 
    the engineering team and make sure you know what you're doing. 

    Remeber:
    1. Each Mito analysis is written to a file, where each step is saved with its
       parameters.
    2. If the _name_ of the step, or the _parameters to the step_ change, then this
       will break existing user analyses. 
    
    Thus, this test is to make sure that we _know_ when we're breaking things. 
    
    However, note that there are ways to break existing user analyses other than this. 
    For example, if you change how the group step flattens headers, this may cause
    issues if the user then later renames one of those flattened columns. So, this
    regression test is not perfect, but it is a good start!
    """

    check_step(
        ADD_COLUMN_STEP,
        1,
        'add_column',
        ['sheet_index', 'column_header']
    )

    check_step(
        DELETE_COLUMN_STEP,
        1,
        'delete_column',
        ['sheet_index', 'column_header']
    )

    check_step(
        RENAME_COLUMN_STEP,
        1,
        'rename_column',
        ['sheet_index', 'old_column_header', 'new_column_header']
    )

    check_step(
        FILTER_STEP,
        1,
        'filter_column',
        ['sheet_index', 'column_header', 'operator', 'filters']
        # TODO: this param "filters" is really weakly typed here, and could totally
        # change without being detected by this test. Boo!
    )
    
    check_step(
        GROUP_STEP,
        1,
        'group',
        ['sheet_index', 'group_rows', 'group_columns', 'values']
        # TODO: the param "values" is also very weakly typed, and could change
        # without this test detecting it
    )

    check_step(
        MERGE_STEP,
        1,
        'merge',
        ['sheet_index_one', 'merge_key_one', 'selected_columns_one', 'sheet_index_two', 'merge_key_two', 'selected_columns_two']
    )

    check_step(
        REORDER_COLUMN_STEP,
        1,
        'reorder_column',
        ['sheet_index', 'column_header', 'new_column_index']
    )

    check_step(
        SET_COLUMN_FORMULA_STEP,
        1,
        'set_column_formula',
        ['sheet_index', 'column_header', 'old_formula', 'new_formula']
    )

    assert len(STEPS) == 8



