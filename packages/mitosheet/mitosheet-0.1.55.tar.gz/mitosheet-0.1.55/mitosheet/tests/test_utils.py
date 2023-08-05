#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
This file contains helpful functions and classes for testing operations.
"""

import pandas as pd

from mitosheet.example import sheet, MitoWidget

class MitoWidgetTestWrapper:
    """
    This class adds some simple wrapper functions onto the MitoWidget 
    to make interacting with it easier for testing purposes.

    It allows you to create just the backend piece of Mito, create columns,
    set formulas, and get values to check the result.
    """

    def __init__(self, mito_widget: MitoWidget):
        self.mito_widget = mito_widget

    def add_column(self, sheet_index: int, column_header: str):
        """
        Adds a column.
        """
        self.mito_widget.receive_message(self.mito_widget, {
            'event': 'edit_event',
            'type': 'add_column_edit',
            'sheet_index': sheet_index,
            'column_header': column_header
        })
    
    def set_formula(
            self, 
            formula: str, 
            sheet_index: int,
            column_header: str, 
            add_column=False,
        ):
        """
        Sets the given column to have formula, and optionally
        adds the column if it does not already exist.
        """
        if add_column:
            self.add_column(sheet_index, column_header)
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'set_column_formula_edit',
                'sheet_index': sheet_index,
                'column_header': column_header,
                'new_formula': formula,
            }
        )

    def merge_sheets(
            self, 
            sheet_index_one, 
            merge_key_one, 
            selected_columns_one,
            sheet_index_two, 
            merge_key_two,
            selected_columns_two
        ):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'merge_edit',
                'sheet_index_one': sheet_index_one,
                'merge_key_one': merge_key_one,
                'selected_columns_one': selected_columns_one,
                'sheet_index_two': sheet_index_two,
                'merge_key_two': merge_key_two,
                'selected_columns_two': selected_columns_two
            }
        )

    def group_sheet(
            self, 
            sheet_index, 
            group_rows,
            group_columns,
            values
        ):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'group_edit',
                'sheet_index': sheet_index,
                'group_rows': group_rows,
                'group_columns': group_columns,
                'values': values
            }
        )

    def filter(
            self, 
            sheet_index, 
            column,
            operator,
            type_,
            condition, 
            value
        ):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'filter_column_edit',
                'sheet_index': sheet_index,
                'column_header': column,
                'operator': operator,
                'filters': [{
                    'type': type_,
                    'condition': condition,
                    'value': value
                }]
            }
        )
    
    def filters(
            self, 
            sheet_index, 
            column,
            operator,
            filters
        ):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'filter_column_edit',
                'sheet_index': sheet_index,
                'column_header': column,
                'operator': operator,
                'filters': filters
            }
        )

    def reorder_column(
            self, 
            sheet_index, 
            column_header, 
            new_column_index
        ):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'reorder_column_edit',
                'sheet_index': sheet_index,
                'column_header': column_header,
                'new_column_index': new_column_index
            }
        )

    def rename_column(self, sheet_index: int, old_column_header: str, new_column_header):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'rename_column_edit',
                'sheet_index': sheet_index,
                'old_column_header': old_column_header,
                'new_column_header': new_column_header
            }
        )

    def delete_column(self, sheet_index: int, column_header: str):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'edit_event',
                'type': 'delete_column_edit',
                'sheet_index': sheet_index,
                'column_header': column_header
            }
        )
    
    def undo(self):
        self.mito_widget.receive_message(
            self.mito_widget,
            {
                'event': 'update_event',
                'type': 'undo'
            }
        )
        

    def get_formula(self, sheet_index: int, column_header: str):
        """
        Gets the formula for a given column. Returns an empty
        string if nothing exists.
        """
        if column_header not in self.mito_widget.column_spreadsheet_code[sheet_index]:
            return ''
        return self.mito_widget.column_spreadsheet_code[sheet_index][column_header]

    def get_value(self, sheet_index: int, column_header: str, row: int):
        """
        Returns a value in a given dataframe at the a given
        index in a column. NOTE: the row is 1 indexed!

        Errors if the value does not exist
        """
        return self.mito_widget.widget_state_container.dfs[sheet_index].at[row - 1, column_header]

    def get_column(self, sheet_index: int, column_header: str, as_list: bool):
        """
        Returns a series object of the given column, or a list if
        as_list is True. 

        Errors if the column does not exist. 
        """
        if as_list:
            return self.mito_widget.widget_state_container.dfs[sheet_index][column_header].tolist()
        return self.mito_widget.widget_state_container.dfs[sheet_index][column_header]

def create_mito_wrapper(sheet_one_A_data, sheet_two_A_data=None) -> MitoWidgetTestWrapper:
    """
    Returns a MitoWidgetTestWrapper instance wrapped around a MitoWidget
    that contains just a column A, containing sheet_one_A_data.
    
    If sheet_two_A_data is defined, then also creates a second dataframe
    with column A defined as this as well.
    """
    dfs = [pd.DataFrame(data={'A': sheet_one_A_data})]

    if sheet_two_A_data is not None:
        dfs.append(pd.DataFrame(data={'A': sheet_two_A_data}))

    mito_widget = sheet(*dfs)
    return MitoWidgetTestWrapper(mito_widget)

def create_mito_wrapper_dfs(*args):
    """
    Creates a MitoWidgetTestWrapper with a mito instance with the given
    data frames.
    """
    mito_widget = sheet(*args)
    return MitoWidgetTestWrapper(mito_widget)