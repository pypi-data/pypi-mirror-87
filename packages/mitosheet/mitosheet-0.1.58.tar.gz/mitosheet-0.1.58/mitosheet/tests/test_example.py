#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.
import pandas as pd
import pytest

from ..example import MitoWidget, sheet
from ..utils import get_invalid_headers
from mitosheet.errors import EditError

def test_example_creation_blank():
    df = pd.DataFrame()
    w = MitoWidget(df)

VALID_DATAFRAMES = [
    (pd.DataFrame()),
    (pd.DataFrame(data={'A': [1, 2, 3]})),
    (pd.DataFrame(data={'A0123': [1, 2, 3]})),
]
@pytest.mark.parametrize("df", VALID_DATAFRAMES)
def test_sheet_creates_valid_dataframe(df):
    mito = sheet(df)
    assert mito is not None

NON_VALID_HEADER_DATAFRAMES = [
    (pd.DataFrame(data={0: [1, 2, 3]}), ['0_']),
    (pd.DataFrame(data={0.1: [1, 2, 3]}), ['0_1_']),
    (pd.DataFrame(data={'A': [1, 2, 3], 0: [1, 2, 3]}), ['A', '0_']),
    (pd.DataFrame(data={'A': [1, 2, 3], '000': [1, 2, 3]}), ['A', '000_']),
    (pd.DataFrame(data={'A': [1, 2, 3], 'abc-123': [1, 2, 3]}), ['A', 'abc_123']),
    (pd.DataFrame(data={'A': [1, 2, 3], '-123': [1, 2, 3]}), ['A', '_123']),
    (pd.DataFrame(data={'A': [1, 2, 3], '-123_': [1, 2, 3]}), ['A', '_123_']),
    (pd.DataFrame(data={'A': [1, 2, 3], '-abc_': [1, 2, 3]}), ['A', '_abc_']),
    (pd.DataFrame(data={'123': [1, 2, 3], '-abc_': [1, 2, 3]}), ['123_', '_abc_']),
    (pd.DataFrame(data={'ABC!DEF': [1, 2, 3], '123': [1, 2, 3]}), ['ABC_DEF', '123_']),
    (pd.DataFrame(data={'ABC?DEF': [1, 2, 3], '123': [1, 2, 3]}), ['ABC_DEF', '123_']),
    (pd.DataFrame(data={' ': [1, 2, 3], '123': [1, 2, 3]}), ['_', '123_']),
    (pd.DataFrame(data={'-': [1, 2, 3], ' !': [1, 2, 3]}), ['_', '__']),
    (pd.DataFrame(data={'##': [1, 2, 3], ' !': [1, 2, 3]}), ['numnum', '__']),
    (pd.DataFrame(data={'#!?5': [1, 2, 3], '#123': [1, 2, 3]}), ['num__5', 'num123']),
    (pd.DataFrame(data={'()': [1, 2, 3], '.,,': [1, 2, 3]}), ['__', '___']),
    (pd.DataFrame(data={'nate': [1, 2, 3], '.,,': [1, 2, 3]}), ['nate', '___']),
    (pd.DataFrame(data={'//': [1, 2, 3], '-': [1, 2, 3]}), ['__', '_']),
]

@pytest.mark.parametrize("df, new_keys", NON_VALID_HEADER_DATAFRAMES)
def test_sheet_errors_during_non_string_headers(df, new_keys):
    assert len(get_invalid_headers(df)) != 0
    mito = sheet(df)
    assert list(mito.widget_state_container.curr_step['dfs'][0].keys()) == new_keys

def test_create_with_multiple_dataframes():
    mito = sheet(pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(data={'A': [1, 2, 3]}))
    assert mito is not None