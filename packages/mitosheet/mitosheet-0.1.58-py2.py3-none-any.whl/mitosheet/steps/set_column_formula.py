#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A set_column_formula step, which allows you to set the formula
of a given column in the sheet (and then recalculates this column)
and it's dependents.
"""
from mitosheet.topological_sort import creates_circularity, topological_sort_columns
from mitosheet.sheet_functions import FUNCTIONS
from mitosheet.parser import parse_formula
from mitosheet.utils import get_column_filter_type

from mitosheet.errors import (
    make_circular_reference_error, 
    make_no_column_error, 
    make_unsupported_function_error, 
    make_wrong_column_metatype_error
)

SET_COLUMN_FORMULA_EVENT = 'set_column_formula_edit'
SET_COLUMN_FORMULA_STEP_TYPE = 'set_column_formula'

SET_COLUMN_FORMULA_PARAMS = [
    'sheet_index', # int
    'column_header', # the new column to create
    'old_formula', # the previous formula, or None (if there is None)
    'new_formula', # the new formula for the column
]


def _update_column_formula_in_curr_step(
        wsc,
        sheet_index,
        column_header,
        old_formula,
        new_formula
    ):
    """
    A  helper function for updating the formula of a column. It assumes
    that the passed information is all _correct_ and will not:
    1. Introduce a circular reference error.
    2. Add an invalid formula.

    It DOES NOT "reexecute" the dataframes, just updates the state variables.
    """

    new_python_code, _, new_dependencies = parse_formula(
        new_formula, 
        column_header
    )

    _, _, old_dependencies = parse_formula(
        old_formula, 
        column_header
    )

    wsc.curr_step['column_spreadsheet_code'][sheet_index][column_header] = new_formula
    wsc.curr_step['column_python_code'][sheet_index][column_header] = new_python_code

    # Update the column dependency graph
    for old_dependency in old_dependencies:
        wsc.curr_step['column_evaluation_graph'][sheet_index][old_dependency].remove(column_header)
    for new_dependency in new_dependencies:
        wsc.curr_step['column_evaluation_graph'][sheet_index][new_dependency].add(column_header)


def execute_set_column_formula_step(
        wsc,
        sheet_index,
        column_header,
        old_formula,
        new_formula
    ):
    """
    Sets the column with column_header to have the new_formula, and 
    updates the dataframe as a result.

    Errors if:
    - The given column_header is not a column. 
    - The new_formula introduces a circular reference.
    - The new_formula causes an execution error in any way. 

    In the case of an error, this function rolls back all variables
    variables to their state at the start of this function.
    """
    if column_header not in wsc.curr_step['column_metatype'][sheet_index]:
        raise make_no_column_error([column_header])

    # First, we check the column_metatype, and make sure it's a formula
    if wsc.curr_step['column_metatype'][sheet_index][column_header] != 'formula':
        raise make_wrong_column_metatype_error(column_header)

    # If nothings changed, there's no work to do
    if (old_formula == new_formula):
        return

    # Then we try and parse the formula
    new_python_code, new_functions, new_dependencies = parse_formula(
        new_formula, 
        column_header
    )

    # We check that the formula doesn't reference any columns that don't exist
    missing_columns = new_dependencies.difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if any(missing_columns):
        raise make_no_column_error(missing_columns)

    # The formula can only reference known formulas
    missing_functions = new_functions.difference(set(FUNCTIONS.keys()))
    if any(missing_functions):
        raise make_unsupported_function_error(missing_functions)

    # Then, we get the list of old column dependencies and new dependencies
    # so that we can update the graph
    old_python_code, old_functions, old_dependencies = parse_formula(old_formula, column_header)

    # Before changing any variables, we make sure this edit didn't
    # introduct any circularity
    circularity = creates_circularity(
        wsc.curr_step['column_evaluation_graph'][sheet_index], 
        column_header,
        old_dependencies,
        new_dependencies
    )
    if circularity:
        raise make_circular_reference_error()

    # We check out a new step, and save the params there
    wsc._create_and_checkout_new_step(SET_COLUMN_FORMULA_STEP_TYPE)
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['column_header'] = column_header
    wsc.curr_step['old_formula'] = old_formula
    wsc.curr_step['new_formula'] = new_formula

    # Update the column formula, and then execute the new formula graph
    _update_column_formula_in_curr_step(wsc, sheet_index, column_header, old_formula, new_formula)
    _execute(wsc, wsc.curr_step['dfs'][sheet_index], sheet_index)

    # Finially, update the type of the filters of this column, for all the filters
    new_type = get_column_filter_type(wsc.curr_step['dfs'][sheet_index][column_header])
    wsc.curr_step['column_type'][sheet_index][column_header] = new_type
    wsc.curr_step['column_filters'][sheet_index][column_header]['filters'] = [
        {'type': new_type, 'condition': filter_['condition'], 'value': filter_['value']} 
        for filter_ in wsc.curr_step['column_filters'][sheet_index][column_header]['filters']
    ]

def _execute(wsc, df, sheet_index):
    """
    Executes the given state variables for  
    """

    topological_sort = topological_sort_columns(wsc.curr_step['column_evaluation_graph'][sheet_index])

    for column_header in topological_sort:
        # Exec the code, where the df is the original dataframe
        # See explination here: https://www.tutorialspoint.com/exec-in-python
        exec(
            wsc.curr_step['column_python_code'][sheet_index][column_header],
            {'df': df}, 
            FUNCTIONS
        )


def transpile_set_column_formula_step(
        widget_state_container,
        step,
        sheet_index,
        column_header,
        old_formula,
        new_formula
    ):
    """
    Transpiles an set_column_formula step to python code!
    """
    code = []

    # We only look at the sheet that was changed, and sort it's columns
    topological_sort = topological_sort_columns(step['column_evaluation_graph'][sheet_index])

    # For all columns downstream of the changed column
    topological_sort = topological_sort[topological_sort.index(column_header):]

    # We compile all of their formulas
    for column in topological_sort:
        column_formula_changes = step['column_python_code'][sheet_index][column]
        if column_formula_changes != '':
            # We replace the data frame in the code with it's parameter name!
            column_formula_changes = column_formula_changes.strip().replace('df', f'{widget_state_container.df_names[sheet_index]}')
            code.append(column_formula_changes)

    return code


SET_COLUMN_FORMULA_STEP = {
    'step_version': 1,
    'event_type': SET_COLUMN_FORMULA_EVENT,
    'step_type': SET_COLUMN_FORMULA_STEP_TYPE,
    'params': SET_COLUMN_FORMULA_PARAMS,
    'execute': execute_set_column_formula_step,
    'transpile': transpile_set_column_formula_step
}