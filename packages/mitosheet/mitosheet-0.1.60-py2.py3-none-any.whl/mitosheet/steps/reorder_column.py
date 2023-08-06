#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A reorder_column step, which allows you to move 
a column to a different location in the df.
"""
from mitosheet.errors import (
    make_no_sheet_error,
    make_no_column_error,
)

REORDER_COLUMN_EVENT = 'reorder_column_edit'
REORDER_COLUMN_STEP_TYPE = 'reorder_column'

REORDER_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # the column to reorder
    'new_column_index', # the new location for the column
]

def execute_reorder_column_step(
        wsc,
        sheet_index,
        column_header,
        new_column_index
    ):
    """
    The function responsible for updating the widget state container
    with a new column reorder step.

    If it fails part of the way through, deletes the new column reorder step entirely.
    """

    # if the sheet doesn't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the column to be reordered exists
    missing_column = set([column_header]).difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_column) > 0:
        raise make_no_column_error(missing_column)

    # make sure new_column_index is valid
    if new_column_index < 0:
        new_column_index = 0

    if new_column_index >= len(wsc.curr_step['dfs'][sheet_index].columns):
        new_column_index = len(wsc.curr_step['dfs'][sheet_index].columns) - 1
        
    # Create a new step
    wsc._create_and_checkout_new_step(REORDER_COLUMN_STEP_TYPE)
    # Save the params of the current step
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['column_header'] = column_header
    wsc.curr_step['new_column_index'] = new_column_index

    # Actually execute the column reordering
    wsc.curr_step['dfs'][sheet_index] = _execute_reorder_column(
        wsc.curr_step['dfs'][sheet_index],
        column_header,
        new_column_index
    )

def _execute_reorder_column(df, column_header, new_column_index):
    """
    Helper function for reordering a column in the dataframe
    """
    df_columns = [col for col in df.columns if col != column_header]
    df_columns.insert(new_column_index, column_header)
    return df[df_columns]


def transpile_reorder_column_step(
        widget_state_container,
        step,
        sheet_index,
        column_header,
        new_column_index
    ):
    """
    Transpiles a column reorder step to python code!
    """

    # get columns in df
    columns_list_line = f'{widget_state_container.df_names[sheet_index]}_columns = [col for col in {widget_state_container.df_names[sheet_index]}.columns if col != \'{column_header}\']'

    # insert column into correct location 
    insert_line = f'{widget_state_container.df_names[sheet_index]}_columns.insert({new_column_index}, \'{column_header}\')'
    
    # Apply reorder line
    apply_reorder_line = f'{widget_state_container.df_names[sheet_index]} = {widget_state_container.df_names[sheet_index]}[{widget_state_container.df_names[sheet_index]}_columns]'

    return [columns_list_line, insert_line, apply_reorder_line]


REORDER_COLUMN_STEP = {
    'step_version': 1,
    'event_type': REORDER_COLUMN_EVENT,
    'step_type': REORDER_COLUMN_STEP_TYPE,
    'params': REORDER_COLUMN_PARAMS,
    'execute': execute_reorder_column_step,
    'transpile': transpile_reorder_column_step
}