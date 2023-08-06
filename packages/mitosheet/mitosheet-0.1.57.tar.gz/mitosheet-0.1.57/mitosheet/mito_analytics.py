#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains analytics objects; exported here to avoid
circular references!
"""
from typing import List
import analytics
import getpass
import pandas as pd

# Write key taken from segement.com
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 
# For now, we identify users with their logged in user name
# which is fine, because we manage user accounts on trymito.io
static_user_id = getpass.getuser()
analytics.identify(static_user_id, {
    'location': __file__
}) #TODO: get information to store as traits?

def log_dfs_metadata(dfs: List[pd.DataFrame]):
    """
    A helper function to log metadata about a list of dataframes, 
    that does not pass any sensitive information of the dataframe
    elsewhere.
    """
    df_shapes = {f'df_{idx}_shape': {'row': df.shape[0], 'col': df.shape[1]} for idx, df in enumerate(dfs)}
    df_headers = {f'df_{idx}_headers': list(df.keys()) for idx, df in enumerate(dfs)}

    analytics.track(static_user_id, 'df_metadata_log_event', dict(
        {'df_count': len(dfs)},
        **df_shapes,
        **df_headers
    ))
