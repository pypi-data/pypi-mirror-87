#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""
import sys
import analytics
import pandas as pd
from typing import List
import traceback

from ipywidgets import DOMWidget
import traitlets as t

from ._frontend import module_name, module_version
from .errors import EditError, get_recent_traceback_as_list, log_recent_error
from .save_utils import (
    read_analysis, 
    write_analysis,
    saved_analysis_names_json
)
from mitosheet.widget_state_container import WidgetStateContainer
from mitosheet.profiling import timeit

from mitosheet.mito_analytics import analytics, static_user_id

class MitoWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = t.Unicode('ExampleModel').tag(sync=True)
    _model_module = t.Unicode(module_name).tag(sync=True)
    _model_module_version = t.Unicode(module_version).tag(sync=True)
    _view_name = t.Unicode('ExampleView').tag(sync=True)
    _view_module = t.Unicode(module_name).tag(sync=True)
    _view_module_version = t.Unicode(module_version).tag(sync=True)

    value = t.Unicode('Hello World').tag(sync=True)
    analysis_name = t.Unicode('').tag(sync=True)
    sheet_json = t.Unicode('').tag(sync=True)
    code_json = t.Unicode('').tag(sync=True)
    df_names_json = t.Unicode('').tag(sync=True)
    df_shape_json = t.Unicode('').tag(sync=True)
    saved_analysis_names_json = t.Unicode('').tag(sync=True)
    user_id = t.Unicode(static_user_id).tag(sync=True)
    column_spreadsheet_code_json = t.Unicode('').tag(sync=True)
    column_filters_json = t.Unicode('').tag(sync=True)
    column_type_json = t.Unicode('').tag(sync=True)


    def __init__(self, *args, **kwargs):
        """
        Takes a list of dataframes, passed through *args. 

        NOTE: assumes that the passed arguments are all dataframes, 
        and also have all valid headers. These conditions are checked in the
        mitosheet.sheet function. 
        """
        # Call the DOMWidget constructor to set up the widget properly
        super(MitoWidget, self).__init__()

        # Set up the state container to hold private widget state
        self.widget_state_container = WidgetStateContainer(args)

        # Set up starting shared state variables
        self.update_shared_state_variables()

        # Set up message handler
        self.on_msg(self.receive_message)

    def update_shared_state_variables(self):
        """
        Helper function for updating all the variables that are shared
        between the backend and the frontend through trailets.
        """
        self.sheet_json = self.widget_state_container.sheet_json
        self.column_spreadsheet_code_json = self.widget_state_container.column_spreadsheet_code_json
        self.code_json = self.widget_state_container.code_json
        self.df_names_json = self.widget_state_container.df_names_json
        self.df_shape_json = self.widget_state_container.df_shape_json
        self.analysis_name = self.widget_state_container.analysis_name
        self.saved_analysis_names_json = saved_analysis_names_json()
        self.column_filters_json = self.widget_state_container.column_filters_json
        self.column_type_json = self.widget_state_container.column_type_json

    @timeit 
    def send(self, msg):
        """
        We overload the DOMWidget's send function, so that 
        we log all outgoing messages
        """
        # Send the message though the DOMWidget's send function
        super().send(msg)

    @timeit
    def saturate(self, event):
        """
        Saturation is when the server fills in information that
        is missing from the event client-side. This is for consistency
        and because the client may not have easy access to the info
        all the time.
        """
        curr_step = self.widget_state_container.curr_step

        if event['event'] == 'edit_event':
            if event['type'] == 'set_column_formula_edit':
                sheet_index = event['sheet_index']
                column_header = event['column_header']
                event['old_formula'] = curr_step['column_spreadsheet_code'][sheet_index][column_header]
        if event['event'] == 'update_event':
            if event['type'] == 'use_existing_analysis_update':
                # If we're getting an event telling us to update 
                analysis_name = event['analysis_name']
                analysis = read_analysis(analysis_name)
                for key, value in analysis.items():
                    event[key] = value

    @timeit
    def handle_edit_event(self, event):
        """
        Handles an edit_event. Per the spec, an edit_event
        updates both the sheet and the codeblock, and as such
        the sheet is re-evaluated and the code for the codeblock
        is re-transpiled.

        Useful for any event that changes the state of both the sheet
        and the codeblock!
        """
        # First, we log the edit that we just got
        analytics.track(self.user_id, event['type'], event)

        # First, we send this new edit to the evaluator
        self.widget_state_container.handle_edit_event(event)

        # We update the state variables 
        self.update_shared_state_variables()

        # Also, write the analysis to a file!
        write_analysis(self.widget_state_container)

        # Tell the front-end to render the new sheet and new code
        self.send({"event": "update_sheet"})
        self.send({"event": "update_code"})

    @timeit
    def handle_update_event(self, event):
        """
        This event is not the user editing the sheet, but rather information
        that has been collected from the frontend (after render) that is being
        passed back.

        For example:
        - Names of the dataframes
        - Name of an existing analysis
        """
        # First, we log the update event that we just got
        analytics.track(self.user_id, event['type'], event)

        self.widget_state_container.handle_update_event(event)

        # Update all state variables and send out an update
        self.update_shared_state_variables()

        # Also, write the analysis to a file!
        write_analysis(self.widget_state_container)

        # Tell the front-end to render the new sheet and new code
        self.send({"event": "update_sheet"})
        self.send({"event": "update_code"})

    def receive_message(self, widget, content, buffers=None):
        """
        Handles all incoming messages from the JS widget. There are two main
        types of events:

        1. edit_event: any event that updates the state of the sheet and the
        code block at once. Leads to reevaluation, and a re-transpile.

        2. update_event: any event that isn't caused by an edit, but instead
        other types of new data coming from the frontend (e.g. the df names 
        or some existing steps).

        3. A log_event is just an event that should get logged on the backend.
        """
        # First, we saturate the event
        event = content
        self.saturate(event)

        try:
            if event['event'] == 'edit_event':
                self.handle_edit_event(event)
            if event['event'] == 'update_event':
                self.handle_update_event(event)
            if event['event'] == 'log_event':
                analytics.track(
                    self.user_id, 
                    event['type'], 
                    event
                )
        except EditError as e:
            # If we hit an error during editing, log that it has occured
            analytics.track(
                self.user_id, 
                f'{e.type_}_log_event', 
                {
                    'header': e.header, 
                    'to_fix': e.to_fix,
                    'traceback': get_recent_traceback_as_list()
                }
            )
            # Report it to the user, and then return
            self.send({
                'event': 'edit_error',
                'type': e.type_,
                'header': e.header,
                'to_fix': e.to_fix
            })
        except:
            # We log the error
            log_recent_error()
            # Report it to the user, and then return
            self.send({
                'event': 'edit_error',
                'type': 'execution_error',
                'header': 'Execution Error',
                'to_fix': 'Sorry, there was an error during executing this code.'
            })

@timeit
def sheet(*args: List[pd.DataFrame]) -> MitoWidget:
    """
    Returns a Mito Widget defined on the passed data frames.

    Note: errors if any of the arguments are not data frames
    """
    args = list(args)

    for df in args:
        if not isinstance(df, pd.DataFrame):
            # Log the error
            analytics.track(
                static_user_id, 
                'sheet_error_log_event', 
                {'error': f'Invalid argument passed to sheet: {df}. Please pass all dataframes.'}
            )

            raise ValueError(f'Invalid argument passed to sheet: {df}. Please pass all dataframes.')

    try:
        widget = MitoWidget(*args) 
    except:
        # We log the error
        log_recent_error('sheet_error_log_event')
        # And then bubble it to the user
        raise

    return widget
