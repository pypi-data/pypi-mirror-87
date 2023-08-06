#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains all functions that don't particularly fit in any other category

All functions describe their behavior with a function documentation object
in the function docstring. Function documentation objects are described
in more detail in docs/README.md.

NOTE: This file is alphabetical order!
"""
import pandas as pd
import numpy as np

from mitosheet.sheet_function_types import as_types
from mitosheet.sheet_functions.sheet_function_utils import fill_series_list_to_max

@as_types('series', 'number')
def OFFSET(series: pd.Series, offset) -> pd.Series:
    """
    {
        "function": "OFFSET",
        "description": "Shifts the given series by the given offset. Use a negative offset to reference a previous row, and a offset number to reference a later row.",
        "examples": [
            "OFFSET(Nums, 10)",
            "OFFSET(call_time, -1)"
        ],
        "syntax": "OFFSET(series, offset)",
        "syntax_elements": [{
                "element": "series",
                "description": "The series to shift up or down."
            },
            {
                "element": "offset",
                "description": "An integer amount to shift. Use a negative number to reference a previous row, and a positive number to reference a later row."
            }
        ]
    }
    """
    length = len(series)
    # If the shift is too big, we just return an empty series
    if abs(offset) >= length:
        return pd.Series([np.NaN] * length)
    
    if offset < 0:
        # Otherwise, append the NaNs to the front, and chop at the correct length
        return pd.concat([pd.Series([np.NaN] * (offset * -1)), series], ignore_index=True).head(length)
    else:
        remaining_series = series.tail(length - offset)
        return pd.concat([remaining_series, pd.Series([np.NaN] * offset)], ignore_index=True).head(length)


# TODO: we should see if we can list these automatically!
MISC_FUNCTIONS = {
    'OFFSET': OFFSET
}