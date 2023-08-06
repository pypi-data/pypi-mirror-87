#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains all functions that are useful for control flow. For now, this
is just IF statements.

All functions describe their behavior with a function documentation object
in the function docstring. Function documentation objects are described
in more detail in docs/README.md.

NOTE: This file is alphabetical order!
"""
import pandas as pd
from functools import reduce

from mitosheet.sheet_function_types import as_types, get_series_type_of_first_arg, MITO_TYPE_CONVERSION_MAP
from mitosheet.sheet_functions.sheet_function_utils import fill_series_list_to_max, fill_series_to_length

@as_types(
    'boolean_series', 
    remaining=True
)
def AND(*argv) -> pd.Series:
    """
    {
        "function": "AND",
        "description": "Returns True if all of the provided arguments are True, and False if any of the provided arguments are False.",
        "examples": [
            "AND(True, False)",
            "AND(Nums > 100, Nums < 200)",
            "AND(Pay > 10, Pay < 20, Status == 'active')"
        ],
        "syntax": "AND(boolean_condition1, [boolean_condition2, ...])",
        "syntax_elements": [{
                "element": "boolean_condition1",
                "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."
            },
            {
                "element": "boolean_condition2 ... [OPTIONAL]",
                "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."
            }
        ]
    }
    """
    argv = fill_series_list_to_max(argv)

    return reduce((lambda x, y: x & y), argv)


@as_types(
    'boolean_series', 
    'series',
    'series'
)
def IF(condition, true_series, false_series) -> pd.Series:
    """
    {
        "function": "IF",
        "description": "Returns one value if the condition is True. Returns the other value if the conditon is False.",
        "examples": [
            "IF(Status == 'success', 1, 0)",
            "IF(Nums > 100, 100, Nums)",
            "IF(AND(Grade >= .6, Status == 'active'), 'pass', 'fail')"
        ],
        "syntax": "IF(boolean_condition, value_if_true, value_if_false)",
        "syntax_elements": [{
                "element": "boolean_condition",
                "description": "An expression or series that returns True or False values. Valid conditions for comparison include ==, !=, >, <, >=, <=."
            },
            {
                "element": "value_if_true",
                "description": "The value the function returns if condition is True."
            },
            {
                "element": "value_if_false",
                "description": "The value the function returns if condition is False."
            }
        ]
    }
    """
    # NOTE: condition should just be a boolean series. true_series, false_series can be series
    # of any type!

    true_series = fill_series_to_length(true_series, len(condition))
    false_series = fill_series_to_length(false_series, len(condition))


    return pd.Series(
        data=[true_series[i] if c else false_series[i] for i, c in enumerate(condition)]
    )

@as_types(
    'boolean_series', 
    remaining=True
)
def OR(*argv) -> pd.Series:
    """
    {
        "function": "OR",
        "description": "Returns True if any of the provided arguments are True, and False if all of the provided arguments are False.",
        "examples": [
            "OR(True, False)",
            "OR(Status == 'success', Status == 'pass', Status == 'passed')"
        ],
        "syntax": "OR(boolean_condition1, [boolean_condition2, ...])",
        "syntax_elements": [{
                "element": "boolean_condition1",
                "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."
            },
            {
                "element": "boolean_condition2 ... [OPTIONAL]",
                "description": "An expression or series that returns True or False values. See IF documentation for a list of conditons."
            }
        ]
    }
    """

    argv = fill_series_list_to_max(argv)
    return reduce((lambda x, y: x | y), argv)



# TODO: we should see if we can list these automatically!
CONTROL_FUNCTIONS = {
    'AND': AND,
    'IF': IF,
    'OR': OR,
}