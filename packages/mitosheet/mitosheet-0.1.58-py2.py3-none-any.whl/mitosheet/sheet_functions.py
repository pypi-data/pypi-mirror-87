#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains all functions that can be used in a sheet. 

All functions describe their behavior with a function documentation object
in the function docstring. Function documentation objects are described
in more detail in docs/README.md.

NOTE: This file is alphabetical order!
"""
from typing import List, Union, Any
from functools import reduce
import pandas as pd

from mitosheet.sheet_function_types import as_types, get_series_type_of_first_arg

def fill_series_to_length(series, length):
    """
    Extends a given series to length, padding it with the last
    defined element in the series. 

    Given all dataframes we use are square, this only occurs when one adds
    1 + df['nums'] (where df['nums'] has more than one row), and then our 
    as_type code converts this to:

    pd.Series(data=[1]) + pd.Series(data=[1, 2]) = pd.Series(data=[1, NaN])

    If we ever are adding non-equal length series, we need to fix this!

    TODO: fix the bug that results from this filling undefined values generally!
    """

    return series.append(
        pd.Series(data=([None] * (length - len(series)))), ignore_index=True
    ).ffill()

def fill_series_list_to_max(series_list):
    """
    Extends all series in the series_list to the max_length of any series
    in the list, padding them all with their last defined elements. 

    Useful so we can add two series together, as:
    -----
    pd.Series(data=[1]) + pd.Series(data=[1, 2]) = pd.Series(data=[1, Nan])
    -----
    which isn't really what we want!
    """
    max_length = max([series.size for series in series_list])
    return [fill_series_to_length(series, max_length) for series in series_list]

@as_types('number_series', remaining=True, ignore_conversion_failures=True)
def AVG(*argv) -> pd.Series:
    """
    {
        "function": "AVG",
        "description": "Returns the numerical mean value of the passed numbers and series.",
        "examples": [
            "AVG(1, 2)",
            "AVG(A, B)",
            "AVG(A, 2)"
        ],
        "syntax": "AVG(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or series to consider when calculating the average."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or series to consider when calculating the average."
            }
        ]
    }
    """
    return SUM(*argv) / len(argv)


@as_types('string_series')
def CLEAN(series) -> pd.Series:
    """
    {
        "function": "CLEAN",
        "description": "Returns the text with the non-printable ASCII characters removed.",
        "examples": [
            "CLEAN('ABC\\n')"
        ],
        "syntax": "CLEAN(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series whose non-printable characters are to be removed."
            }
        ]
    }
    """
    # TODO: this function is wacked out. It removes spaces (Excel's does not!)
    # Also, I'm not sure it makes any sense in the context of Python + pandas
    # reading in dataframes, given they handle all characters here.
    return series.apply(lambda x:''.join([i if 32 <= ord(i) < 126 else "" for i in x]))


@as_types('string_series', remaining=True, ignore_conversion_failures=True)
def CONCAT(*argv) -> pd.Series:
    """
    {
        "function": "CONCAT",
        "description": "Returns the passed strings and series appended together.",
        "examples": [
            "CONCAT('Bite', 'the bullet')",
            "CONCAT(A, B)"
        ],
        "syntax": "CONCAT(string1, [string2, ...])",
        "syntax_elements": [{
                "element": "string1",
                "description": "The first string or series."
            },
            {
                "element": "string2, ... [OPTIONAL]",
                "description": "Additional strings or series to append in sequence."
            }
        ]
    }
    """

    # We make sure all the series are the max length, so the concat has something at every index
    argv = fill_series_list_to_max(argv)

    return reduce((lambda x, y: x + y), argv)


@as_types('string_series', 'string_series')
def FIND(series, substrings) -> pd.Series:
    """
    {
        "function": "FIND",
        "description": "Returns the position at which a string is first found within text, case-sensitive. Returns 0 if not found.",
        "examples": [
            "FIND(A, 'Jack')",
            "FIND('Ben has a friend Jack', 'Jack')"
        ],
        "syntax": "FIND(text_to_search, search_for)",
        "syntax_elements": [{
                "element": "text_to_search",
                "description": "The text or series to search for the first occurrence of search_for."
            },
            {
                "element": "search_for",
                "description": "The string to look for within text_to_search."
            }
        ]
    }
    """

    # If there aren't enough substrings, we fill it to the end
    substrings = fill_series_to_length(substrings, series.size)

    # Then, we find each substring
    return pd.Series(data=[string.find(substring) + 1 for string, substring in zip(series, substrings)])


@as_types(
    'string_series', 
    'number_series', 
    num_optional=1, 
    attempt_output_types=get_series_type_of_first_arg
)
def LEFT(series, num_chars=None) -> pd.Series:
    """
    {
        "function": "LEFT",
        "description": "Returns a substring from the beginning of a specified string.",
        "examples": [
            "LEFT(A, 2)",
            "LEFT('The first character!')"
        ],
        "syntax": "LEFT(string, [number_of_characters])",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series from which the left portion will be returned."
            },
            {
                "element": "number_of_characters [OPTIONAL, 1 by default]",
                "description": "The number of characters to return from the start of string."
            }
        ]
    }
    """
    if num_chars is None:
        num_chars = pd.Series(data=[1] * series.size)

    # If there aren't enough char splits, we fill it to the end
    num_chars = fill_series_to_length(num_chars, series.size)
    # And then slice the string on the left
    return pd.Series(data=[string[:num_char] for string, num_char in zip(series, num_chars)])

@as_types('string_series')
def LEN(series: pd.Series) -> pd.Series:
    """
    {
        "function": "LEN",
        "description": "Returns the length of a string.",
        "examples": [
            "LEN(A)",
            "LEN('This is 21 characters')"
        ],
        "syntax": "LEN(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series whose length will be returned."
            }
        ]
    }
    """
    return series.str.len()


@as_types(
    'string_series', 
    attempt_output_types=get_series_type_of_first_arg
)
def LOWER(series) -> pd.Series:
    """
    {
        "function": "LOWER",
        "description": "Converts a given string to lowercase.",
        "examples": [
            "=LOWER('ABC')",
            "=LOWER(A)",
            "=LOWER('Nate Rush')"
        ],
        "syntax": "LOWER(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to convert to lowercase."
            }
        ]
    }
    """
    return series.str.lower()

@as_types(
    'string_series', 'number_series', 'number_series',
    attempt_output_types=get_series_type_of_first_arg
)
def MID(series, start_loc, num_chars) -> pd.Series:
    """
    {
        "function": "MID",
        "description": "Returns a segment of a string.",
        "examples": [
            "MID(A, 2, 2)",
            "MID('Some middle characters!', 3, 4)"
        ],
        "syntax": "MID(string, starting_at, extract_length)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to extract the segment from."
            },
            {
                "element": "starting_at",
                "description": "The index from the left of string from which to begin extracting."
            },
            {
                "element": "extract_length",
                "description": "The length of the segment to extract."
            }
        ]
    }
    """
    # If there aren't enough char splits, we fill it to the end
    start_loc = fill_series_to_length(start_loc, series.size)
    num_chars = fill_series_to_length(num_chars, series.size)
    # And then slice the string on the left
    return pd.Series(data=[
        string[start - 1: start - 1 + num_char] for string, start, num_char 
        in zip(series, start_loc, num_chars)
    ])

@as_types(
    'number_series', 
    remaining=True, 
    ignore_conversion_failures=True
)
def MULTIPLY(*argv) -> pd.Series:
    """
    {
        "function": "MULTIPLY",
        "description": "Returns the product of two numbers.",
        "examples": [
            "MULTIPLY(2,3)",
            "MULTIPLY(A,3)"
        ],
        "syntax": "MULTIPLY(factor1, [factor2, ...])",
        "syntax_elements": [{
                "element": "factor1",
                "description": "The first number to multiply."
            },
            {
                "element": "factor2, ... [OPTIONAL]",
                "description": "Additional numbers or series to multiply."
            }
        ]
    }
    """
    # We make sure all the series are the max length, so the * has something at every index
    argv = fill_series_list_to_max(argv)

    return reduce((lambda x, y: x * y), argv) 


@as_types(
    'string_series',
    attempt_output_types=get_series_type_of_first_arg
)
def PROPER(series) -> pd.Series:
    """
    {
        "function": "PROPER",
        "description": "Capitalizes the first letter of each word in a specified string.",
        "examples": [
            "=PROPER('nate nush')",
            "=PROPER(A)"
        ],
        "syntax": "PROPER(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The value or series to convert to convert to proper case."
            }
        ]
    }
    """
    return series.str.title()

@as_types(
    'string_series', 'number_series', 
    num_optional=1,
    attempt_output_types=get_series_type_of_first_arg
)
def RIGHT(series, num_chars=None) -> pd.Series:
    """
    {
        "function": "RIGHT",
        "description": "Returns a substring from the beginning of a specified string.",
        "examples": [
            "RIGHT(A, 2)",
            "RIGHT('The last character!')"
        ],
        "syntax": "RIGHT(string, [number_of_characters])",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series from which the right portion will be returned."
            },
            {
                "element": "number_of_characters [OPTIONAL, 1 by default]",
                "description": "The number of characters to return from the end of string."
            }
        ]
    }
    """
    if num_chars is None:
        num_chars = pd.Series(data=[1] * series.size)

    # If there aren't enough char splits, we fill it to the end
    num_chars = fill_series_to_length(num_chars, series.size)
    # And then slice the string on the left
    return pd.Series(data=[string[-num_char:] if num_char > 0 else '' for string, num_char in zip(series, num_chars)])
        

@as_types(
    'number_series', 'number_series',
    num_optional=1,
    attempt_output_types=get_series_type_of_first_arg
)
def ROUND(series, decimals=None):
    """
    {
        "function": "ROUND",
        "description": "Rounds a number to a given number of decimals.",
        "examples": [
            "ROUND(1.3)",
            "ROUND(A, 2)"
        ],
        "syntax": "ROUND(value, [decimals])",
        "syntax_elements": [{
                "element": "value",
                "description": "The value or series to round."
            },
            {
                "element": "decimals",
                "description": " The number of decimals to round to. Default is 0."
            }
        ]
    }
    """

    # If no decimals option is passed, round to no decimals
    if decimals is None:
        return series.round()
    
    # Otherwise, fill the decimals to length
    decimals = fill_series_to_length(decimals, series.size)

    return pd.Series(
        [round(num, dec) for num, dec in zip(series, decimals)]
    )


@as_types(
    'string_series', 'string_series', 'string_series', 'number_series', 
    num_optional=1,
    attempt_output_types=get_series_type_of_first_arg
)
def SUBSTITUTE(series, old_text, new_text, count=None):
    """
    {
        "function": "SUBSTITUTE",
        "description": "Replaces existing text with new text in a string.",
        "examples": [
            "SUBSTITUTE('Better great than never', 'great', 'late')",
            "SUBSTITUTE(A, 'dog', 'cat')"
        ],
        "syntax": "SUBSTITUTE(text_to_search, search_for, replace_with, [count])",
        "syntax_elements": [{
                "element": "text_to_search",
                "description": "The text within which to search and replace."
            },
            {
                "element": "search_for",
                "description": " The string to search for within text_to_search."
            },
            {
                "element": "replace_with",
                "description": "The string that will replace search_for."
            },
            {
                "element": "count",
                "description": "The number of times to perform the substitute. Default is all."
            }
        ]
    }
    """
    old_text = fill_series_to_length(old_text, series.size)
    new_text = fill_series_to_length(new_text, series.size)
    if count is None:
        count = fill_series_to_length(pd.Series(data=[-1]), series.size)

    return pd.Series(
        [string.replace(old, new, c) for string, old, new, c in zip(series, old_text, new_text, count)]
    )

@as_types('number_series', remaining=True, ignore_conversion_failures=True)
def SUM(*argv) -> pd.Series:
    """
    {
        "function": "SUM",
        "description": "Returns the sum of the given numbers and series.",
        "examples": [
            "SUM(10, 11)",
            "SUM(A, B, D, F)",
            "SUM(A, B, D, F)"
        ],
        "syntax": "SUM(value1, [value2, ...])",
        "syntax_elements": [{
                "element": "value1",
                "description": "The first number or column to add together."
            },
            {
                "element": "value2, ... [OPTIONAL]",
                "description": "Additional numbers or columns to sum."
            }
        ]
    }
    """
    # Fill sum to the max length of any series
    argv = fill_series_list_to_max(argv)

    return reduce((lambda x, y: x + y), argv) 

@as_types(
    'string_series',
    attempt_output_types=get_series_type_of_first_arg
)
def TRIM(series) -> pd.Series:
    """
    {
        "function": "TRIM",
        "description": "Returns a string with the leading and trailing whitespace removed.",
        "examples": [
            "=TRIM('  ABC')",
            "=TRIM('  ABC  ')",
            "=TRIM(A)"
        ],
        "syntax": "TRIM(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The value or series to remove the leading and trailing whitespace from."
            }
        ]
    }
    """
    return series.apply(lambda x: x.strip())


@as_types(
    'string_series',
    attempt_output_types=get_series_type_of_first_arg
)
def UPPER(series) -> pd.Series:
    """
    {
        "function": "UPPER",
        "description": "Converts a given string to uppercase.",
        "examples": [
            "=UPPER('abc')",
            "=UPPER(A)",
            "=UPPER('Nate Rush')"
        ],
        "syntax": "UPPER(string)",
        "syntax_elements": [{
                "element": "string",
                "description": "The string or series to convert to uppercase."
            }
        ]
    }
    """

    return series.str.upper()


# TODO: we should see if we can list these automatically!
FUNCTIONS = {
    'AVG': AVG,
    'CLEAN': CLEAN,
    'CONCAT': CONCAT,
    'FIND': FIND,
    'LEFT': LEFT,
    'LEN': LEN,
    'LOWER': LOWER,
    'MID': MID,
    'MULTIPLY': MULTIPLY,
    'PROPER': PROPER,
    'RIGHT': RIGHT,
    'ROUND': ROUND,
    'SUBSTITUTE': SUBSTITUTE,
    'SUM': SUM,
    'TRIM': TRIM,
    'UPPER': UPPER,
}