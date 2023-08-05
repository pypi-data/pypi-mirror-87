#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

from typing import List
import uuid
import sys
import pandas as pd
import json
from copy import deepcopy, copy

from mitosheet.mito_analytics import analytics, log_dfs_metadata, static_user_id
from mitosheet.steps import STEPS
from mitosheet.updates import UPDATES
from mitosheet.steps.initial_steps.initalize import execute_initialize_step
from mitosheet.steps.initial_steps.initial_rename import execute_initial_rename_step
from mitosheet.sheet_functions import FUNCTIONS
from mitosheet.utils import dfs_to_json, get_column_filter_type
from mitosheet.transpiler.transpile import transpile
from mitosheet.save_utils import write_analysis
from mitosheet.errors import (
    make_execution_error
)
from mitosheet.profiling import timeit


class WidgetStateContainer():
    """
    Holds the state of the steps, which represents operations that
    have been performed on the input dataframes. 
    """

    def __init__(self, dfs: pd.DataFrame):
        # Just in case they are a tuple, make them a list - as it's easier to operate with.
        # We also make a copy so we don't modify the original dataframes.
        dfs = deepcopy(list(dfs))

        # Log metadata about these dataframes
        log_dfs_metadata(dfs)

        # We also save a copy of the initial dataframe's keys, for easy access
        self.original_df_keys = [df.keys() for df in dfs]

        # The df_names are composed of two parts:
        # 1. The names of the variables passed into the mitosheet.sheet call (which don't change over time).
        # 2. The names of the dataframes that were created during the analysis (e.g. by a merge).
        # Until we get them from the frontend as an update_event, we default them to df1, df2, ...
        self.df_names = [f'df{i + 1}' for i in range(len(dfs))] 

        # For now, we just randomly generate analysis names. 
        # We append a UUID to note that this is not an analysis the user has saved.
        self.analysis_name = 'UUID-' + str(uuid.uuid4())

        # We generate an initial rename step, which handles any issues with invalid headers
        # by converting them all to valid headers - which occurs before any formula step.
        dfs = execute_initial_rename_step(dfs)

        # Then we initialize the first initalize step
        self.steps = []
        execute_initialize_step(self, dfs)        


    @property
    @timeit
    def curr_step_id(self):
        """
        The ID of the current step
        """
        return len(self.steps) - 1

    @property
    @timeit
    def curr_step(self):
        """
        Returns the current step object as a property of the object,
        so reference it with self.curr_step
        """
        return self.steps[self.curr_step_id]

    @property
    @timeit
    def num_sheets(self):
        """
        Duh. :)
        """
        return len(self.steps[self.curr_step_id]['dfs'])

    @property
    @timeit
    def dfs(self) -> List[pd.DataFrame]:
        return self.steps[self.curr_step_id]['dfs']

    @property
    @timeit
    def df_names_json(self):
        """
        A JSON object containing the names of the dataframes
        """
        return json.dumps({'df_names': self.df_names})

    @property
    @timeit
    def sheet_json(self):
        """
        sheet_json contains a serialized representation of the data
        frames that is then fed into the ag-grid in the front-end. 

        NOTE: we only display the _first_ 2,000 rows of the dataframe
        for speed reasons. This results in way less data getting 
        passed around
        """
        return dfs_to_json(self.curr_step['dfs'])
    
    @property
    @timeit
    def df_shape_json(self):
        """
        Returns the df shape (rows, columns) of each dataframe in the 
        current step!
        """
        return json.dumps([
            {'rows': df.shape[0], 'cols': df.shape[1]}
            for df in self.curr_step['dfs']
        ])

    @property
    @timeit
    def column_spreadsheet_code_json(self):
        """
        column_spreadsheet_code_json is a list of all the spreadsheet
        formulas that users have used, for each sheet they have. 
        """
        return json.dumps(self.curr_step['column_spreadsheet_code'])

    @property
    @timeit
    def code_json(self):
        """
        This code json string is sent to the front-end and is what
        ends up getting displayed in the codeblock. 
        """
        return json.dumps(transpile(self))

    @property
    @timeit
    def column_filters_json(self):
        """
        This column_filters list is used by the front end to display
        the filtered icons in the UI
        """
        return json.dumps(self.curr_step['column_filters'])
    
    @property
    @timeit
    def column_type_json(self):
        """
        Returns a list of JSON objects that hold the type of each
        data in each column.
        """
        return json.dumps(self.curr_step['column_type'])

    @timeit
    def handle_edit_event(self, edit_event):
        """
        Updates the widget state with a new step that was created
        by the edit_event. Each edit_event creates at most one step. 

        If there is an error in the creation of the new step, this
        function will delete the new, invalid step.
        """

        pre_update_step_num = len(self.steps) 

        for new_step in STEPS:
            if edit_event['type'] == new_step['event_type']:
                # Get the params for this event
                params = {key: value for key, value in edit_event.items() if key in new_step['params']}
                # Actually execute this event
                try:
                    new_step['execute'](self, **params)
                except:
                    # If there is _any_ error while executing this event, we:
                    # 1. Delete the new step, if it has been created at all.
                    # 2. Bubble the error up
                    if len(self.steps) > pre_update_step_num:
                        self.steps = self.steps[:pre_update_step_num]

                    # https://stackoverflow.com/questions/6593922/letting-an-exception-to-bubble-up
                    raise

                # Return if execution is sucessful
                return

        # If we didn't find anything, then we error!
        raise Exception(f'{edit_event} is not an edit event!')

    @timeit
    def handle_update_event(self, update_event):
        """
        Handles any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).
        """
        if update_event['type'] == 'df_names_update':
            df_names = update_event['df_names']
            self.df_names = df_names
        elif update_event['type'] == 'save_analysis':
            analysis_name = update_event['analysis_name']
            write_analysis(self, analysis_name)
        elif update_event['type'] == 'use_existing_analysis_update':
            step_summaries = update_event['steps']
            self._rerun_analysis(step_summaries)
        else:
            for update in UPDATES:
                if update_event['type'] == update['event_type']:
                    # Get the params for this event
                    params = {key: value for key, value in update_event.items() if key in update['params']}
                    # Actually execute this event
                    update['execute'](self, **params)
                    # And then return
                    return

            raise Exception(f'{update_event} is not an update event!')

    def _rerun_analysis(self, step_summaries):
        """
        This function reapplies all the steps summarized in the passed step summaries, 
        which come from a saved analysis. 

        If any of the step summaries fails, this function tries to roll back to before
        it applied any of the stems
        """   
        # We make a shallow copy of the steps, as none of the objects
        # will be changed by the step summaries we apply   
        old_steps = copy(self.steps)  
        
        try:
            for step_id, step_summary in step_summaries.items():
                step_type = step_summary['step_type']

                found = False
                for new_step in STEPS:
                    if step_type == new_step['step_type']:
                        found = True
                        # Get the params for this event
                        params = {key: value for key, value in step_summary.items() if key in new_step['params']}
                        # Actually execute this event
                        new_step['execute'](self, **params)

                if not found:
                    raise Exception('Trying to recreate invalid step:', step_summary)

        except Exception as e:
            print(e)
            # We remove all applied steps if there was an error
            self.steps = old_steps

            # And report a generic error to the user
            raise make_execution_error()


    def _create_and_checkout_new_step(self, step_type):
        """
        Creates a new step with new_step_id and step_type that starts
        with the ending state of the previous step
        """
        new_step_id = self.curr_step_id + 1

        # the new step is a copy of the previous step, where we only take the data we need
        # (which is the formula content only)
        new_step = dict()

        new_step['step_type'] = step_type
        new_step['column_metatype'] = deepcopy(self.steps[new_step_id - 1]['column_metatype'])
        new_step['column_type'] = deepcopy(self.steps[new_step_id - 1]['column_type'])
        new_step['column_spreadsheet_code'] = deepcopy(self.steps[new_step_id - 1]['column_spreadsheet_code'])
        new_step['added_columns'] = [[] for df in self.steps[new_step_id - 1]['dfs']]
        new_step['column_python_code'] = deepcopy(self.steps[new_step_id - 1]['column_python_code'])
        new_step['column_evaluation_graph'] = deepcopy(self.steps[new_step_id - 1]['column_evaluation_graph'])
        new_step['column_filters'] = deepcopy(self.steps[new_step_id - 1]['column_filters'])
        new_step['dfs'] = deepcopy(self.steps[new_step_id - 1]['dfs'])

        # add the new step to list of steps
        self.steps.append(new_step)

    def _delete_curr_step(self):
        """
        Deletes the current step and rolls back a step!
        """
        self.steps.pop()

    def add_df_to_curr_step(self, new_df):
        """
        Helper function for adding a new dataframe to the current step!
        """
        # update dfs by appending new df
        self.curr_step['dfs'].append(new_df)
        # Also update the dataframe name
        self.df_names.append(f'df{len(self.df_names) + 1}')

        # Update all the variables that depend on column_headers
        column_headers = new_df.keys()
        self.curr_step['column_metatype'].append({column_header: 'value' for column_header in column_headers})
        self.curr_step['column_type'].append({column_header: get_column_filter_type(new_df[column_header]) for column_header in column_headers})
        self.curr_step['column_spreadsheet_code'].append({column_header: '' for column_header in column_headers})
        self.curr_step['column_python_code'].append({column_header: '' for column_header in column_headers})
        self.curr_step['column_evaluation_graph'].append({column_header: set() for column_header in column_headers})
        self.curr_step['column_filters'].append({column_header: {'operator':'And', 'filters': []} for column_header in column_headers})

    def does_sheet_index_exist(self, index):
        return not (index < 0 or index >= self.num_sheets)
    