#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains helpful utility functions
"""
import json
import pandas as pd
import numpy as np
import numbers
from string import ascii_letters, digits

ALLOWED_CHARS = ascii_letters + digits + '_'


def make_valid_header(column_header):
    """
    Takes a header, and performs replaces against common characters
    to make the column_header valid!
    """
    # If it's just numbers, turn it into a string (with an underscore)
    if isinstance(column_header, numbers.Number):
        return str(column_header).replace('.', '_') + '_'

    # If it's just numbers in a string, add an underscore
    if column_header.isdigit():
        return column_header + "_"

    # Replace common invalid seperators with valid seperators
    replace_dict = {
        ' ': '_',
        '-': '_',
        '(': '_',
        ')': '_',
        '/': '_',
        '#': 'num',
        ',': '_',
        '.': '_',
        '!': '_',
        '?': '_'
    }
    for find, replace in replace_dict.items():
        column_header = column_header.replace(find, replace)
    
    if not is_valid_header(column_header):
        # If our reasonable replacements don't work, we just ban any character not from a set
        new_header = ''.join([
            c for c in column_header if c in ALLOWED_CHARS
        ])
        # And then append an underscore, for good measure
        new_header = new_header + '_'

        return new_header
    return column_header

def is_valid_header(column_header):
    """
    A header is valid if:
    1. It is a string
    2. It only contains alphanumber characters, or _
    3. It has at least one non-numeric character.

    Valid examples: A, ABC, 012B, 213_bac, 123_123
    Invalid examples: 123, 123!!!, ABC!, 123-123

    This is a result of not being able to distingush column headers from constants
    otherwise, and would not be necessary if we had a column identifier!
    """

    return isinstance(column_header, str) and ( # Condition (1)
        set(column_header).issubset(set(ascii_letters).union(set(digits)).union(set(['_']))) and # Condition (2)
        not column_header.isdigit() # Condition (3)
    )


def get_invalid_headers(df: pd.DataFrame):
    """
    Given a dataframe, returns a list of all the invalid headers this list has. 
    """
    return [
        header for header in df.columns.tolist()
        if not is_valid_header(header)
    ]


def dfs_to_json(dfs):
    return json.dumps([df_to_json_dumpsable(df) for df in dfs])


def df_to_json_dumpsable(df: pd.DataFrame):
    """
    Returns a dataframe represented in a way that can be turned into a 
    JSON object with json.dumps
    """
    # We make a copy, as we modify the df below
    df = df.copy(deep=True).head(n=2000) # we only show the first 2k rows!
    
    # First, we figure out which of the columns contain dates, and we
    # convert them to string columns (for formatting reasons).
    # NOTE: we don't use date_format='iso' in df.to_json call as it appends seconds to the object, 
    # see here: https://stackoverflow.com/questions/52730953/pandas-to-json-output-date-format-in-specific-form
    date_columns = df.select_dtypes(include=['datetime64'])
    for key in date_columns:
        df[key] = date_columns[key].dt.strftime('%Y-%m-%d %X')

    json_obj = json.loads(df.to_json(orient="split"))
    # Then, we go through and find all the null values (which are infinities),
    # and set them to 'NaN' for display in the frontend.
    for d in json_obj['data']:
        for idx, e in enumerate(d):
            if e is None:
                d[idx] = 'NaN'

    return json_obj


def get_column_filter_type(series):
    """
    Given a series, take's the series dtype and catergorizes the correct
    column_filter_type so that the filter modal can display only
    valid filtering options
    
    TODO: unify this with the other Mito types!
    """
    try: 
        if series.dtype == np.float64 or series.dtype == np.int64:
            return 'number'
        elif series.dtype == 'datetime64[ns]':
            return 'datetime'
        elif series.dtype == np.object:
            return 'string'
    except:
        # If there is an error, we just call this a string column. In the wild, we have
        # seen errors where dtype is not defined on the df object, but we have been
        # unable to replicate this or figure out when it occurs.
        return 'string'
    
    # TODO: what do we do if it's none? for now just return string, for no reason.
    return 'string'
    