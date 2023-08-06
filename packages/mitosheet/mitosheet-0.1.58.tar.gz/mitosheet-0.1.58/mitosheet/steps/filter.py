#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
A filter steps, which allows you to filter a column based on some
conditions and some values. 

NOTE: there are some workarounds in this step with old filter steps being deleted
and remade (like the one right) - simply because we don't have a way of editing
old steps otherwise!
"""
from copy import deepcopy
import functools
from numbers import Number
import pandas as pd

from mitosheet.errors import (
    EditError,
    make_execution_error,
    make_no_sheet_error,
    make_no_column_error,
    make_invalid_filter_error
)

FILTER_COLUMN_EVENT = 'filter_column_edit'
FILTER_COLUMN_STEP_TYPE = 'filter_column'

FILTER_COLUMN_PARAMS = [
    'sheet_index', # int
    'column_header', # column to filter from
    'operator', # 'Or' or 'And'
    'filters', # the trippples of ({'type': <type>, 'condition': <condition>, 'value': <value>})
]


# CONSTANTS USED IN THE FILTER STEP ITSELF

STRING_TYPE = 'string'
NUMBER_TYPE = 'number'
DATETIME_TYPE = 'datetime'

SHARED_FILTER_CONDITIONS = [
    'empty',
    'not_empty'
]

STRING_FILTER_CONDITIONS = [
    'contains',
    'string_does_not_contain',
    'string_exactly'
]

NUMBER_FILTER_CONDITIONS = [
    'number_exactly',
    'greater',
    'greater_than_or_equal',
    'less',
    'less_than_or_equal'
]

DATETIME_FILTER_CONDITIONS = [
    'datetime_exactly',
    'datetime_greater',
    'datetime_greater_than_or_equal',
    'datetime_less',
    'datetime_less_than_or_equal',
]


def execute_filter_column(
        wsc,
        sheet_index,
        column_header,
        operator,
        filters
    ):
    """
    Filters an existing sheet with the given filters, which 
    each contain a condition and an optional value.
    """
    # if the sheet doesn't exist, throw an error
    if not wsc.does_sheet_index_exist(sheet_index):
        raise make_no_sheet_error(sheet_index)

    # We check that the filtered column exists 
    missing_column = set([column_header]).difference(wsc.curr_step['column_metatype'][sheet_index].keys())
    if len(missing_column) > 0: 
        raise make_no_column_error(missing_column)

    # if the condition is none, don't create a new step and delete the current filter if it exists
    if len(filters) == 0:
        # if there is a filter already applied to the column, remove it
        _reset_filter(wsc, sheet_index, column_header, ignore_last_step=False)
        return

    # If no errors we create a new step for this filter
    wsc._create_and_checkout_new_step(FILTER_COLUMN_STEP_TYPE)
    # update the step to save the variables needed to reconstruct the filter
    wsc.curr_step['sheet_index'] = sheet_index
    wsc.curr_step['column_header'] = column_header
    wsc.curr_step['filters'] = filters
    wsc.curr_step['operator'] = operator

    # Then we update the dataframe, first by executing on a fake dataframe
    try:
        # TODO: Remove this speculative execution, when it's safe to do so
        # (e.g. when we have proper step editing). 
        # For now, because filter is wacky, we leave it in here... 

        # make a copy of our data frame to test operate on 
        df_copy = deepcopy(wsc.curr_step['dfs'][sheet_index])

        # We execute on the copy first to see if there will be errors
        _execute_filter(
            df_copy, 
            column_header,
            operator,
            filters
        )

    except EditError as e:
        # If an edit error occurs, we delete the filter step
        wsc._delete_curr_step()
        # And we propagate this error upwards
        raise e
    except Exception as e:
        print(e)
        # If any other error occurs, we delete the filter step
        wsc._delete_curr_step()
        # We raise a generic execution error in this case!
        raise make_execution_error()

    # if there is a filter already applied to the column, remove it
    # NOTE: we ignore the last step as _the step we are currently executing_ 
    # would get deleted otherwise, which we do not want. 
    _reset_filter(wsc, sheet_index, column_header, ignore_last_step=True)

    # if there was no error in execution on the copy, execute on real dataframes
    wsc.dfs[sheet_index] = _execute_filter(
        wsc.dfs[sheet_index], 
        column_header,
        operator,
        filters
    )

    # keep track of which columns are filtered
    wsc.curr_step['column_filters'][sheet_index][column_header]['operator'] = operator
    wsc.curr_step['column_filters'][sheet_index][column_header]['filters'] = filters

def _reset_filter(wsc, sheet_index, column_header, ignore_last_step=False):
    """
    To reset the filter, we:

    1. Delete the filter step.
    2. Save the analysis.
    3. Delete _all_ the steps (ik, crazy).
    4. Replay the analysis.

    NOTE: we do this as a workaround because we want users to be able to edit
    filters, but there is currently no way to go back to a step and edit it. 

    We should _heavily_ re-evaluate this screwy-ness when we allow editing of steps, 
    and rolling back to steps.
    """
    # NOTE: we import here to avoid circular imports. This is an unfortunate
    # side effect of this entire workaround :( )
    from mitosheet.save_utils import read_analysis, write_analysis

    deleted_step_id = None

    # find the step to delete
    for step_id, step in enumerate(wsc.steps):
        if ignore_last_step and step_id == wsc.curr_step_id:
            continue

        if step['step_type'] == FILTER_COLUMN_STEP_TYPE:
            # If this is the step that added a filter to the column, mark it as the one to delete
            if step['sheet_index'] == sheet_index and step['column_header'] == column_header:
                deleted_step_id = step_id

    # if there are no step to delete, return
    if deleted_step_id == None:
        return
    
    # Delete the filter step
    wsc.steps.pop(deleted_step_id)

    # save the current analysis, now without the filter step
    write_analysis(wsc)

    # Delete _all the steps_ except the first
    wsc.steps = [wsc.steps[0]]

    # Rerun the analysis
    saved_analysis = read_analysis(wsc.analysis_name)
    wsc._rerun_analysis(saved_analysis['steps'])

def _execute_filter(
        df, 
        column_header,
        operator,
        filters
    ):
    """
    Executes a filter on the given column, filtering by removing any rows who
    don't meet the condition.
    """

    applied_filters = []

    for filter_ in filters:
        type_ = filter_['type']
        condition = filter_['condition']
        value = filter_['value']

        # First, we case on the shared conditions, to get them out of the way
        if condition in SHARED_FILTER_CONDITIONS:
            if condition == 'empty':
                applied_filters.append(df[column_header].isna())
            elif condition == 'not_empty':
                applied_filters.append(df[column_header].notnull())
            continue

        if type_ == STRING_TYPE:
            if condition not in STRING_FILTER_CONDITIONS:
                raise Exception(f'Invalid condition passed to string filter {condition}')

            # Check that the value is the valid
            if not isinstance(value, str):
                raise make_invalid_filter_error(value, STRING_TYPE)

            if condition == 'contains':
                applied_filters.append(df[column_header].str.contains(value, na=False))
            if condition == 'string_does_not_contain':
                applied_filters.append(~df[column_header].str.contains(value, na=False))
            elif condition == 'string_exactly':
                applied_filters.append(df[column_header] == value)

        elif type_ == NUMBER_TYPE:
            if condition not in NUMBER_FILTER_CONDITIONS:
                raise Exception(f'Invalid condition passed to number filter {condition}')
            
            # Check that the value is the valid
            if not isinstance(value, Number):
                raise make_invalid_filter_error(value, NUMBER_TYPE)

            if condition == 'number_exactly':
                applied_filters.append(df[column_header] == value)
            elif condition == 'greater':
                applied_filters.append(df[column_header] > value)
            elif condition == 'greater_than_or_equal':
                applied_filters.append(df[column_header] >= value)
            elif condition == 'less':
                applied_filters.append(df[column_header] < value)
            elif condition == 'less_than_or_equal':
                applied_filters.append(df[column_header] <= value)

        elif type_ == DATETIME_TYPE:
            if condition not in DATETIME_FILTER_CONDITIONS:
                raise Exception(f'Invalid condition passed to datetime filter {condition}')

            # Check that we were given something that can be understood as a date
            try:
                timestamp = pd.to_datetime(value)
            except:
                raise make_invalid_filter_error(value, DATETIME_TYPE)

            if condition == 'datetime_exactly':
                applied_filters.append(df[column_header] == timestamp)
            elif condition == 'datetime_greater':
                applied_filters.append(df[column_header] > timestamp)
            elif condition == 'datetime_greater_than_or_equal':
                applied_filters.append(df[column_header] >= timestamp)
            elif condition == 'datetime_less':
                applied_filters.append(df[column_header] < timestamp)
            elif condition == 'datetime_less_than_or_equal':
                applied_filters.append(df[column_header] <= timestamp)

        else:
            raise Exception(f'Invalid type passed in filter {type_}')

    def filter_reducer(filter_one, filter_two):
        # helper for combining filters based on the operations
        if operator == 'Or':
            return (filter_one) | (filter_two)
        elif operator == 'And':
            return (filter_one) & (filter_two)
        else:
            raise Exception(f'Operator {operator} is unsupported')

    # Combine all the filters into a single filter
    final_filter = functools.reduce(filter_reducer, applied_filters)
    
    return df[final_filter].reset_index(drop=True)


def transpile_filter_column(
        widget_state_container,
        step,
        sheet_index,
        column_header,
        operator,
        filters
    ):
    """
    Transpiles a filter step to Python code. 
    """
    df_name = widget_state_container.df_names[sheet_index]

    # build the filter code
    partial_filter_code = []
    for filter_ in filters:
        condition = filter_['condition']
        value = filter_['value']

        FILTER_FORMAT_STRING_DICT = {
            # SHARED CONDITIONS
            'empty': '{df_name}.{column_header}.isna()',
            'not_empty': '{df_name}.{column_header}.notnull()',

            # NUMBERS
            'number_exactly': '{df_name}[\'{column_header}\'] == {value}',
            'greater': '{df_name}[\'{column_header}\'] > {value}',
            'greater_than_or_equal': '{df_name}[\'{column_header}\'] >= {value}',
            'less': '{df_name}[\'{column_header}\'] < {value}',
            'less_than_or_equal': '{df_name}[\'{column_header}\'] <= {value}',
            
            # STRINGS
            'contains': '{df_name}[\'{column_header}\'].str.contains(\'{value}\', na=False)',
            'string_does_not_contain': '~{df_name}[\'{column_header}\'].str.contains(\'{value}\', na=False)',
            'string_exactly': '{df_name}[\'{column_header}\'] == \'{value}\'',

            # DATES
            'datetime_exactly': '{df_name}[\'{column_header}\'] == pd.to_datetime(\'{value}\')',
            'datetime_greater': '{df_name}[\'{column_header}\'] > pd.to_datetime(\'{value}\')',
            'datetime_greater_than_or_equal': '{df_name}[\'{column_header}\'] >= pd.to_datetime(\'{value}\')',
            'datetime_less': '{df_name}[\'{column_header}\'] < pd.to_datetime(\'{value}\')',
            'datetime_less_than_or_equal': '{df_name}[\'{column_header}\'] <= pd.to_datetime(\'{value}\')',            
        }

        if condition in FILTER_FORMAT_STRING_DICT:
            partial_filter_code.append(
                FILTER_FORMAT_STRING_DICT[condition].format(
                    df_name=df_name,
                    column_header=column_header,
                    value=value
                )
            )
        else:
            continue

    if len(partial_filter_code) == 0:
        return []
    elif len(partial_filter_code) == 1:
        return [
            f'{df_name} = {df_name}[{partial_filter_code[0]}]',
            f'{df_name} = {df_name}.reset_index(drop=True)'
        ]
    else:
        # If there are multiple conditions, we combine them together, with the
        # given operator in the middle
        OPERATOR_SIGNS = {
            'Or': '|',
            'And': '&'
        }
        filter_string = f' {OPERATOR_SIGNS[operator]} '.join([f'({pfc})' for pfc in partial_filter_code])
        return [
            f'{df_name} = {df_name}[{filter_string}]',
            f'{df_name} = {df_name}.reset_index(drop=True)'
        ]


FILTER_STEP = {
    'step_version': 1,
    'event_type': FILTER_COLUMN_EVENT,
    'step_type': FILTER_COLUMN_STEP_TYPE,
    'params': FILTER_COLUMN_PARAMS,
    'execute': execute_filter_column,
    'transpile': transpile_filter_column
}