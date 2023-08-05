#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
NOTE: this step should not be included in the export in __init__.py, as it is 
a special sort of step that does not get saved in the step list!

An initial rename, which is a step that only occurs at the start of an analysis (and
does not error if replayed when already run), but is responsible for renaming invalid
column headers to headers mito can handle.

NOTE: this step is not the same as a column rename for a variety of reasons, including:
1. With many column headers getting renamed, indivigual column rename steps generate too much code. 
   Though this could be optimized out, doing so it tricky with our current approach of inserting
   formula steps in-between all steps.
2. This step is automatically generated at the start of every analysis it needs to be generated at,
   and so needs to handle being replayed differently than column renames (because it should never
   error if it has been run before, because it _always_ has run before when replayed)!
"""
import json
from mitosheet.utils import is_valid_header, make_valid_header

INITIAL_RENAME_EVENT = 'initial_rename_edit' # NOTE: this should never be generated by the frontend!
INITIAL_RENAME_STEP_TYPE = 'initial_rename'

# It has no parameters, other than the dataframes in the wsc!
INITIAL_RENAME_PARAMS = []

def execute_initial_rename_step(dfs):
    """
    The function responsible for updating the widget state container
    with an initial rename step. This is not logged as step in the step list
    and just implicitly occurs at the start of every analysis!

    """
    for sheet_index, df in enumerate(dfs):
        renames = dict()
        for column_header in df.keys():
            if not is_valid_header(column_header):
                valid_header = make_valid_header(column_header)
                renames[column_header] = valid_header
        
        df.rename(columns=renames, inplace=True)

    return dfs

def transpile_initial_rename_step(
        widget_state_container
    ):
    """
    Transpiles an initial rename to Python code! May be empty if there is nothing to rename.

    NOTE: we still have a df naming problem, and so in this case, we simply use the names of the 
    dataframes as they are pased in the initial step, which has them unchanged, as they originially
    were.
    """
    rename_lines = []
    for sheet_index, column_headers in enumerate(widget_state_container.original_df_keys):
        renames = dict()
        for column_header in column_headers:
            if not is_valid_header(column_header):
                valid_header = make_valid_header(column_header)
                renames[column_header] = valid_header

        if len(renames) == 0:
            continue

        rename_lines.append(
            f'{widget_state_container.df_names[sheet_index]}.rename(columns={json.dumps(renames)}, inplace=True)'
        )

    return rename_lines


"""
This object wraps all the information for the initial rename step
"""
INITIAL_RENAME_STEP = {
    'event_type': INITIAL_RENAME_EVENT,
    'step_type': INITIAL_RENAME_STEP_TYPE,
    'params': INITIAL_RENAME_PARAMS,
    'execute': execute_initial_rename_step,
    'transpile': transpile_initial_rename_step
}





