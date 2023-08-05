#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains @decorators to help Mito sheet functions return and handle
types in a consistent way.
"""
import pandas as pd
import numpy as np
from functools import wraps
from mitosheet.errors import make_invalid_arguments_error, make_function_execution_error

# Because type(1) = int, thus 1 is a 'number' in the Mito type system
MITO_PRIMITIVE_TYPE_MAPPING = {
    'number': [int, float],
    'string': [str],
    'boolean': [bool],
    'timestamp': [pd.Timestamp]
}

# NOTE: these are the dtype strings of series used by pandas!
MITO_SERIES_TYPE_MAPPING = {
    'number_series': ['int64', 'float64'],
    'string_series': ['str', 'object'],
    'boolean_series': ['bool'],
    'datetime_series': ['datetime64[ns]']
}

MITO_TYPE_PRIMITIVE_TO_SERIES_MAPPING = {
    'number': 'number_series',
    'string': 'string_series',
    'boolean': 'boolean_series',
    'timestamp': 'datetime_series'
}

def identity(x):
    """
    Helper function for the MITO_TYPE_CONVERSION_MAP, when turning from the conversion is from
    one type to itself (and so no work needs to be done).
    """
    return x


"""
A mapping of functions from converting from one Mito type to another. 

MITO_TYPE_CONVERSION_MAP['number']['string'] returns a function that 
converts from a number to a string. 

If there is no conversion possible the above is defined as None!

NOTE: the conversion functions may error and this should be handeled!
"""
MITO_TYPE_CONVERSION_MAP = {
    'number': {
        'number': identity,
        'string': lambda num: str(num),
        'boolean': lambda num: bool(num),
        'timestamp': None,
        'number_series': lambda num: pd.Series(data=[num]),
        'string_series': lambda num: pd.Series(data=[str(num)]),
        'boolean_series': lambda num: pd.Series(data=[bool(num)]),
        'datetime_series': None
    },
    'string': {
        'number': lambda string: float(string),
        'string': identity,
        'boolean': lambda string: bool(string),
        'timestamp': None,
        'number_series': lambda string: pd.Series(data=[float(string)]),
        'string_series': lambda string: pd.Series(data=[string]),
        'boolean_series': lambda string: pd.Series(data=[bool(string)]),
        'datetime_series': lambda string: pd.Series(data=[pd.to_datetime(string)], dtype='datetime64[ns]')
    },
    'boolean': {
        'number': lambda boolean: float(boolean),
        'string': lambda boolean: str(boolean),
        'boolean': identity,
        'timestamp': None,
        'number_series': lambda boolean: pd.Series(data=[float(boolean)]),
        'string_series': lambda boolean: pd.Series(data=[str(boolean)]),
        'boolean_series': lambda boolean: pd.Series(data=[boolean]),
        'datetime_series': None
    },
    'timestamp': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': identity,
        'number_series': None,
        'string_series': lambda timestamp: pd.Series(data=[timestamp.strftime('%Y-%m-%d %X')]),
        'boolean_series': None,
        'datetime_series': lambda timestamp: pd.Series(data=[timestamp], dtype='datetime64[ns]')
    },
    'number_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': identity,
        'string_series': lambda num_series: num_series.astype('str'),
        'boolean_series': lambda num_series: num_series.astype('bool'),
        'datetime_series': None
    },
    'string_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': lambda str_series: str_series.astype('float64'),
        'string_series': lambda str_series: str_series.astype('str'),
        'boolean_series': lambda str_series: str_series.astype('bool'),
        'datetime_series': lambda str_series: pd.to_datetime(str_series)
    },
    'boolean_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': lambda bool_series: bool_series.astype('float64'),
        'string_series': lambda bool_series: bool_series.astype('str'),
        'boolean_series': identity,
        'datetime_series': None
    },
    'datetime_series': {
        'number': None,
        'string': None,
        'boolean': None,
        'timestamp': None,
        'number_series': None,
        'string_series': lambda datetime_series: datetime_series.dt.strftime('%Y-%m-%d %X'),
        'boolean_series': None,
        'datetime_series': identity
    }
}

# Supertypes are the parent types of other types. There is only one currently:
# 'series' has subtypes that end in _series.
SUPERTYPES = set(['series'])

MITO_TYPES = set(MITO_PRIMITIVE_TYPE_MAPPING.keys()).union(MITO_SERIES_TYPE_MAPPING.keys()).union(SUPERTYPES)


def get_mito_type(obj):

    if isinstance(obj, pd.Series):
        dtype = obj.dtype
        for key, value in MITO_SERIES_TYPE_MAPPING.items():
            if dtype in value:
                return key

    elif isinstance(obj, pd.Timestamp):
        return 'timestamp'
    else:
        obj_type = type(obj)

        for key, value in MITO_PRIMITIVE_TYPE_MAPPING.items():
            if obj_type in value:
                return key

    return None

def is_in_type_set(type_set, obj):
    mito_type = get_mito_type(obj)

    if mito_type is None:
        return False

    return mito_type in type_set


def as_types(
        *args, 
        remaining=False, 
        ignore_conversion_failures=False, 
        num_optional=0,
        attempt_output_types=None
    ):
    """
    This generator factory will attempt to take the given arguments to the decorated sheet
    function and cast them to type arguments given in the decorator.

    This will primarily error if:
    0. If the wrong number of types are passed to the sheet function.
    1. A conversion cannot be made from the passed type to the target type:
        - You can't convert from a string_series to a string, for example
        - You can't convert from the string "hi" to a number
        - See the mappings defined above in the MITO_TYPE_CONVERSION_MAP above!

    However, if ignore_conversion_failures is True, will ignore errors of type (1), 
    and instead will just leave out the arguments that fail to convert.

    attempt_output_types is an optional parameter. If passed, it should be a function
    that takes all arguments as input, and returns the Mito type that it wants the result
    to be returned as.
    """

    types = args

    if set(args).difference(MITO_TYPES):
        raise Exception(f'Types to as_types must be from {MITO_TYPES}, not {args}')

    def wrap(sheet_function):
        @wraps(sheet_function)
        def wrapped_f(*args):
            # First, we check that the number of arguments passed is correct
            if not remaining:
                # If not remaining, then the function has a specific number of arguments
                if len(types) > len(args) + num_optional:
                    raise make_invalid_arguments_error(sheet_function.__name__)

            else:
                # Otherwise, the function takes a variable number of arguments, so we must have less
                # arguments than the number of given types
                if len(types) > len(args):
                    raise make_invalid_arguments_error(sheet_function.__name__)

            # before changing the types, determine the indexes that contain nan values
            nan_indexes = get_nan_indexes(*args)

            # for each arg that is an instance of a pd.series, filter out the nan_indexes
            new_args = []
            for arg in args:
                if isinstance(arg, pd.Series): 
                    # only keep the rows at indexes that don't contain a nan_index in any of the
                    # series arguments to the sheet function
                    processed_arg = arg.loc[[not boolean for boolean in nan_indexes]]

                    # then reset the indexes so that when the sheet function creates a new series
                    # it will have the same indexes as the passed in series

                    # drop = True Just resets the index, without inserting it as a column in the new DataFrame.
                    processed_arg = processed_arg.reset_index(drop=True)
                    new_args.append(processed_arg)

                else:
                    new_args.append(arg)

            # Then, we fill the types to make sure there is a type for each of the passed arguments
            filled_types = [types[index] if index < len(types) else types[-1] for index, _ in enumerate(new_args)]
            new_arguments = []

            # Finally, we check that each given argument is of the valid type
            for to_type, argument in zip(filled_types, new_args):
                from_type = get_mito_type(argument)

                # If we just want it as a series, we convert it whatever type of
                # series doesn't change the type of data
                if to_type == 'series':
                    if from_type.endswith('series'):
                        # If it's already a series, we don't need to convert
                        new_arguments.append(argument)
                        continue
                    to_type = MITO_TYPE_PRIMITIVE_TO_SERIES_MAPPING[from_type]

                # We actually try and make a conversion
                conversion_function = MITO_TYPE_CONVERSION_MAP[from_type][to_type]

                # Error if no conversion is possible
                if conversion_function is None:
                    if not ignore_conversion_failures:
                        # Occurs if you cannot convert from {from_type} to {to_type}
                        raise make_invalid_arguments_error(sheet_function.__name__)

                    else:
                        continue

                try:
                    converted_arg = conversion_function(argument)

                except Exception as e:
                    if not ignore_conversion_failures:
                        # Occurs if you cannot convert from {from_type} to {to_type}

                        raise make_invalid_arguments_error(sheet_function.__name__)
                    else:
                        continue
                
                # If we can convert, then save the conversion as an argument!
                new_arguments.append(converted_arg)
                
            try:
                # actually apply the sheet function
                result = sheet_function(*new_arguments)

                # If we should cast the output, we try to cast it
                if attempt_output_types is not None:
                    attempt_output_type = attempt_output_types(*new_args)
                    # If there is no conversion available, we give up
                    if attempt_output_type is not None:

                        original_output_type = get_mito_type(result)
                        final_conversion_function = MITO_TYPE_CONVERSION_MAP[original_output_type][attempt_output_type]

                        if final_conversion_function is not None:
                            # NOTE: This can error during the conversion, in which case an error
                            # is reported back to the user that this function failed...
                            result = final_conversion_function(result)

                            # add back the nan values
                            return put_nan_indexes_back(result, nan_indexes) 
                
                # If we don't want to cast it, or if no cast is available, we just add back the nan values and return 
                return put_nan_indexes_back(result, nan_indexes)
            except:
                raise make_function_execution_error(sheet_function.__name__)

            return result
        return wrapped_f
    return wrap


def get_series_type_of_first_arg(*args):
    """
    Given a tuple of arguments, returns the Mito type of the first argument,
    in it's series interpretation.

    Useful for being passed as attempt_output_types for functions like 
    LEFT, RIGHT, MID, etc - where we want the function to preserve
    the output types if possible.
    """ 
    if len(args) == 0:
        return None

    mito_type = get_mito_type(args[0])

    # If it's a primitive type, we want it to be returned as a series
    if mito_type in MITO_PRIMITIVE_TYPE_MAPPING.keys():
        return MITO_TYPE_PRIMITIVE_TO_SERIES_MAPPING[mito_type]
    else:
        return mito_type


def get_nan_indexes(*argv): 
    """
    Given the list of arguments to a function, as *argv, 
    returns a list of row indexes that is True iff one of the series 
    params is NaN at that index. Otherwise the index is False

    This function is called by the as_types decorator 
    """

    # we find the max length of the args because we are unsure ahead of time which arg 
    # is a series. we need the max_length to construct the boolean index array
    max_length = -1
    for arg in argv:
        # check the type to make sure an error is not thrown for calling len() on an int
        if isinstance(arg, pd.Series) and len(arg) > max_length:
            max_length = len(arg)

    # if there are no series, then:
    #   1. there are no NaN values
    #   2. all of the args are a length of 1
    if max_length == -1:
        return [False]

    nan_indexes = [False for i in range(max_length)]

    # for each row, check for NaN values in the function
    for arg in argv:
        if isinstance(arg, pd.Series): 
            for idx in range(len(arg)):
                if pd.isna(arg[idx]):
                    nan_indexes[idx] = True

    return nan_indexes


def put_nan_indexes_back(series, nan_indexes):
    """
    This functions takes a series and a boolean index list that is True 
    if the index in the series should be NaN and false if it should
    be left alone. 

    Returns the series with the NaN values put in

    This function is called by the as_types decorator 
    """
    original_length = len(nan_indexes)
    final_series = []
    real_index = 0
    non_nan_index = 0

    while real_index < original_length:
        if nan_indexes[real_index]:
            final_series.append(np.NaN)
        else:
            final_series.append(series[non_nan_index])
            non_nan_index += 1
        real_index +=1

    final_series = pd.Series(final_series)
    return final_series