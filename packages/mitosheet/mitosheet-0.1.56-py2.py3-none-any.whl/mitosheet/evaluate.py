#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the evaluate function, which takes a list of edit events
as well as the original dataframe, and returns the current state 
of the sheet as a dataframe
"""
import re
from itertools import chain

from mitosheet.mito_analytics import analytics, static_user_id
from .errors import make_invalid_formula_error, make_invalid_column_reference_error

def parse_formula(formula, address):
    """
    Returns a representation of the formula that is easy to handle.

    Specifically, this function returns the triple:
    (python_code, functions, dependencies).

    python_code : a string of Python code that executes
    this formula.
    functions : a set of a strings (function names) that 
    are called
    dependencies : a set of columns this formula references
    """
    if formula is None:
        return '', set(), set()

    # We remove the leading =, as we don't need it
    if not formula.startswith('='):
        raise make_invalid_formula_error(formula)
    formula = formula[1:]

    # First, we find the ranges of the formula that are string constants;
    # we do not edit these! Taken from: https://stackoverflow.com/a/63707053/13113837
    string_matches_double_quotes = re.finditer(r'"(?:(?:(?!(?<!\\)").)*)"', formula)
    string_matches_single_quotes = re.finditer(r'\'(?:(?:(?!(?<!\\)\').)*)\'', formula)
    string_ranges = []
    for string_match in chain(string_matches_double_quotes, string_matches_single_quotes):
        string_ranges.append(string_match.span())

    functions = set()
    dependencies = set()
    def replace(match):
        """
        Each word match can be:
            1. A constant.
                - A number. Thus, all characters must be digits
                - A string. Must be surrounded by single or double quotes.
                - A boolean. True or False only.
            2. A function call. 
                - This MUST be followed by a '('
            3. A column_reference
                - Any word that isn't any of the above!
        """
        text: str = match.group()
        start = match.start()
        end = match.end() # this is +1 after the last char of the string

        # We skip this token if it is within a string!
        for string_range in string_ranges:
            string_start = string_range[0]
            string_end = string_range[1]

            if (string_start <= start and string_end >= end):
                return text

        # CONSTANTS

        # Number
        if text.isnumeric():
            return text
        # String (check it's in quotes)
        if start - 1 >= 0 and (formula[start - 1] == '\"' or formula[start - 1] == '\'') \
            and end < len(formula) and (formula[end] == '\"' or formula[end] == '\''):
            return text
        # Boolean
        if text == 'True' or text == 'False':
            return text

        # Function
        if end < len(formula) and formula[end] == '(':
            # We turn all used functions into upper case in the translated Python
            # NOTE: this does not effect the original spreadsheet formula, which
            # may remaind lower case. 
            function = text.upper()
            analytics.track(static_user_id, f'{function}_used_log_event')
            functions.add(function)
            return function

        # If the reference is to A1, we throw an A1 reference error
        # TODO: fix this up so this doesn't happen when there _is_ an A1 column, lol
        if text.upper() == 'A1':
            raise make_invalid_column_reference_error()

        # Finially, columns
        dependencies.add(text)
        return f'df[\'{text}\']'
    
    # We match all words in formula, and send them through the replace function.
    # See documentation here: https://docs.python.org/3/library/re.html#re.sub
    formula = re.sub('\w+', replace, formula)
    
    # Finially, prepend the address to set the dataframe
    formula = f'df[\'{address}\'] = {formula}'

    return formula, functions, dependencies