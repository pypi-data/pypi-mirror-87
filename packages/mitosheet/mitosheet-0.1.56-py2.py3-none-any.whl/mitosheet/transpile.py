#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the transpile function, which takes the backend widget
container and generates transpiled Python code.
"""

from mitosheet.mito_analytics import analytics, static_user_id
from mitosheet.topological_sort import topological_sort_columns
from mitosheet.sheet_functions import FUNCTIONS
from mitosheet.steps import STEPS
from mitosheet.steps.initial_rename import transpile_initial_rename_step


def get_previous_formula_step(steps, step_id):
    """
    Returns the most recent formula step before the step with step_id. 

    Returns None if this is the first formula step!
    """
    for step in reversed(steps[:step_id]):
        if step['step_type'] == 'formula':
            return step
    
    return None

def formula_step_changes_formulas_for_sheet(steps, formula_step, formula_step_id, sheet_index):
    """
    Returns true if there are changes to the formulas for the given sheet_index
    in this formula step, as compared to the formula step before it. 
    """
    previous_step = get_previous_formula_step(steps, formula_step_id)

    # If the first formula step, then it is a change from nothing!
    if previous_step is None:
        return True

    # Then, we check that the column spreadsheet code is the same, for each of the sheets
    curr_column_spreadsheet_code = formula_step['column_spreadsheet_code'][sheet_index]
    # If this is a new sheet, then the formulas are new too!
    if sheet_index >= len(previous_step['column_spreadsheet_code']):
        return True
    prev_column_spreadsheet_code = previous_step['column_spreadsheet_code'][sheet_index]

    return curr_column_spreadsheet_code != prev_column_spreadsheet_code

def get_formula_step_code(
        widget_state_container,
        steps, 
        formula_step, 
        formula_step_id
    ):
    """
    Returns the code for a formula step, making sure to define columns in the correct
    order.
    
    Optimizes out formula steps that:
    1. Don't make changes to a sheet
    2. Initilize code in order (and thus to 0) twice.
    """

    step_code = []

    for sheet_index in range(len(formula_step['column_evaluation_graph'])):

        # If no changes were made to the sheet, we skip. Note that we can't _just_
        # skip all unedited formulas, as we want "live updating" to work.
        if not formula_step_changes_formulas_for_sheet(steps, formula_step, formula_step_id, sheet_index):
            continue

        topological_sort = topological_sort_columns(formula_step['column_evaluation_graph'][sheet_index])

        # If there are columns that were created during this step that aren't defined in their 
        # original creation order, we write them out in the creation order
        topological_sort_of_new_columns = [column for column in topological_sort if column in formula_step['added_columns'][sheet_index]]
        added_in_order_code = False
        if topological_sort_of_new_columns != formula_step['added_columns'][sheet_index]:
            # Append a comment to explain what's going on
            step_code.append(
                '# Make sure the columns are defined in the correct order'
            )
            step_code.append(
                '; '.join(
                    [
                        f'{widget_state_container.df_names[sheet_index]}[\'{added_column}\'] = 0'
                        for added_column in formula_step['added_columns'][sheet_index]
                    ]
                )
            )
            added_in_order_code = True

        for column in topological_sort:
            column_formula_changes = formula_step['column_python_code'][sheet_index][column]['column_formula_changes']
            column_spreadsheet_code = formula_step['column_spreadsheet_code'][sheet_index][column]
            if column_formula_changes != '':
                if column in formula_step['added_columns'][sheet_index] and added_in_order_code and column_spreadsheet_code == '=0':
                    # We skip columns that have been initalized above to the correct formula
                    # in order to keep them in the correct order.
                    continue

                # We replace the data frame in the code with it's parameter name!
                column_formula_changes = column_formula_changes.strip().replace('df', f'{widget_state_container.df_names[sheet_index]}')
                step_code.append(column_formula_changes)
    
    return step_code


def transpile(widget_state_container):
    """
    Takes the Python code in the widget_state_container and linearizes it
    so it can be consumed by the front-end. 
    
    When there are multiple sheets, the first sheets code is first, followed
    by the second sheets code, etc. 
    """
    analytics.track(static_user_id, 'transpiler_started_log_event')

    code = []
    filled_step_count = 0

    # First, we manually code an initial rename_step, which occurs
    initial_rename_step = transpile_initial_rename_step(widget_state_container)
    if len(initial_rename_step) > 0:
        code.append("# Step 1 (rename headers to make them work with Mito)")
        code.extend(initial_rename_step)
        filled_step_count += 1

    for step_id, step in enumerate(widget_state_container.steps):

        step_code = []

        if step['step_type'] == 'formula':
            step_code = get_formula_step_code(
                widget_state_container, 
                widget_state_container.steps,
                step, 
                step_id
            )
        elif step['step_type'] == 'merge':
            step_code = step['merge_code']
        elif step['step_type'] == 'column_rename':
            step_code = step['rename_code']
        elif step['step_type'] == 'column_delete':
            step_code = step['delete_code']
        else:
            """
            The code below contains the _new_ step handling, where all steps as specified in a similar
            format and the can be looped over as such. 

            This code will eventually replace the code above which cases manually!
            """
            for new_step in STEPS:
                if step['step_type'] == new_step['step_type']:
                    # Get the params for this event
                    params = {key: value for key, value in step.items() if key in new_step['params']}
                    # Actually execute this event
                    step_code = new_step['transpile'](
                        widget_state_container, 
                        f'df{len(step["dfs"])}',
                        **params
                    )


        if len(step_code) > 0:
            # We start each step with a comment saying which step it is.
            # NOTE: the step number displayed is _not_ the step id that is used in the backend.
            # as we only display non empty steps - so we keep things incrementing so users aren't
            # confused!
            code.append(f'# Step {filled_step_count + 1}')
            filled_step_count += 1
            
            code.extend(step_code)


    analytics.track(static_user_id, 'transpiler_finished_log_event')

    return {
        'imports': f'from mitosheet import *',
        'code': code
    }