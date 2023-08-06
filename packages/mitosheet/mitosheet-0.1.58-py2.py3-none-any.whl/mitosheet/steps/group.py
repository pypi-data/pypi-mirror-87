#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A group step, which allows you to group data
from an existing dataframe along some keys, and then
aggregate other columns with specific functions.
"""
from pandas.core.base import DataError
import pandas as pd

from mitosheet.errors import (
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_aggregation_error,
    make_invalid_aggregation_error,
)

GROUP_EVENT = 'group_edit'
GROUP_STEP_TYPE = 'group'

GROUP_PARAMS = [
    'sheet_index', # int
    'group_rows', # list of column_headers, could be empty
    'group_columns', # list of column_headers, could be empty
    'values', # a dict from column_header -> aggregation function
]

def execute_group_step(
        wsc,
        sheet_index,
        group_rows,
        group_columns,
        values
    ):
    """
    The function responsible for updating the widget state container
    with a new group step.

    If it fails part of the way through, deletes the new group step entirely.
    """

    # if the sheets don't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the group by doesn't use any columns that don't exist
    columns_used = set(group_rows).union(set(group_columns))
    missing_group_keys = columns_used.difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_group_keys) > 0:
        raise make_no_column_error(missing_group_keys)

    missing_value_keys = set(values.keys()).difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_value_keys) > 0:
        raise make_no_column_error(missing_value_keys)

    # Create a new step
    wsc._create_and_checkout_new_step(GROUP_STEP_TYPE)
    # Save the params of the current step
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['group_rows'] = group_rows
    wsc.curr_step['group_columns'] = group_columns
    wsc.curr_step['values'] = values

    # Actually execute the grouping
    try:
        new_df = _execute_group(
            wsc.curr_step['dfs'][sheet_index], 
            group_rows,
            group_columns,
            values
        )
    except DataError as e:
        # A data-error occurs when you try to aggregate on a column where the function
        # cannot be applied (e.g. 'mean' on a column of strings)
        print(e)
        # Generate an error informing the user
        raise make_invalid_aggregation_error()

    # Add it to the dataframe
    wsc.add_df_to_curr_step(new_df)

def _execute_group(df, group_rows, group_columns, values):
    """
    Helper function for executing the groupby on a specific dataframe
    and then aggregating the values with the passed values mapping
    """

    # First, we handle a special case where the only row is also the value
    # the user wants to count. In this case, we
    # This is something that C.M. wants + needs :) 
    if len(group_rows) == 1 and len(group_columns) == 0 and len(values) == 1 and values == {group_rows[0]: 'count'}:
        groupby_obj = df.groupby([group_rows[0]], as_index=False)
        return groupby_obj.size()


    values_keys = list(values.keys())

    # Built the args, leaving out any unused values
    args = {}

    if len(group_rows) > 0:
        args['index'] = group_rows

    if len(group_columns) > 0:
        args['columns'] = group_columns

    if len(values) > 0:
        args['values'] = values_keys
        args['aggfunc'] = values

    pivot_table = df.pivot_table(**args) # type: pd.DataFrame

    # Flatten the column headers
    pivot_table.columns = [
        '_'.join([str(c) for c in col]).strip() if isinstance(col, tuple) else col
        for col in pivot_table.columns.values
    ]

    # flatten the column headers & reset the indexes
    pivot_table = pivot_table.rename_axis(None, axis=1).reset_index()

    return pivot_table

# Helpful constants for code formatting
TAB = '    '
NEWLINE_TAB = f'\n{TAB}'


def build_args_code(
        group_rows,
        group_columns,
        values
    ):
    """
    Helper function for building an arg string, while leaving
    out empty arguments. 
    """
    values_keys = list(values.keys())

    args = []
    if len(group_rows) > 0:
        args.append(f'index={group_rows},')

    if len(group_columns) > 0:
        args.append(f'columns={group_columns},')

    if len(values) > 0:
        args.append(f'values={values_keys},')
        args.append(f'aggfunc={values}')

    return NEWLINE_TAB.join(args)


def transpile_group_step(
        widget_state_container,
        step,
        sheet_index,
        group_rows,
        group_columns,
        values
    ):
    """
    Transpiles a group step to python code!
    """
    new_df_name = f'df{len(step["dfs"])}'


    # First, we handle a special case where the only row is also the value the user wants to count. 
    # In this case, we simply count it! This handles a common case users bump into
    if len(group_rows) == 1 and len(group_columns) == 0 and len(values) == 1 and values == {group_rows[0]: 'count'}:
        return [
            f'groupby_obj = {widget_state_container.df_names[sheet_index]}.groupby([\'{group_rows[0]}\'], as_index=False)',
            f'{new_df_name} = groupby_obj.size()'
        ]

    transpiled_code = []
    
    # Pivot 
    pivot_comment = '# Pivot the data'
    pivot_table_args = build_args_code(group_rows, group_columns, values)
    pivot_table_call = f'pivot_table = {widget_state_container.df_names[sheet_index]}.pivot_table({NEWLINE_TAB}{pivot_table_args}\n)'
    transpiled_code.append(f'{pivot_comment}\n{pivot_table_call}')

    # Flatten column headers. 
    # NOTE: this only needs to happen if there is more than one group_column, as the columns
    # will be flat if there are no columns grouped
    if len(group_columns) > 0:
        flatten_comment = '# Flatten the column headers'
        flatten_code = f'pivot_table.columns = [{NEWLINE_TAB}\'_\'.join([str(c) for c in col]).strip() if isinstance(col, tuple) else col{NEWLINE_TAB}for col in pivot_table.columns.values\n]'
        transpiled_code.append(f'{flatten_comment}\n{flatten_code}')

    # Finially, reset the column name, and the indexes!
    reset_index_comment = f'# Reset the column name and the indexes'
    reset_index_code = f'{new_df_name} = pivot_table.rename_axis(None, axis=1).reset_index()'
    transpiled_code.append(f'{reset_index_comment}\n{reset_index_code}')

    return transpiled_code


GROUP_STEP = {
    'step_version': 1,
    'event_type': GROUP_EVENT,
    'step_type': GROUP_STEP_TYPE,
    'params': GROUP_PARAMS,
    'execute': execute_group_step,
    'transpile': transpile_group_step
}