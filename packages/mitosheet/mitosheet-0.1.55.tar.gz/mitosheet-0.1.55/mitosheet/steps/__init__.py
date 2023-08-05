#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
See mito/mitosheet/steps/README.md for more information about 
how to add a step!

NOTE: this new step refactor is a WIP, and will not be finished
until we remove all the manual step casing that occurs throughout the 
codebase. This is an incremental process that will take time!
"""

from mitosheet.steps.group import GROUP_STEP
from mitosheet.steps.filter import FILTER_STEP
from mitosheet.steps.reorder_column import REORDER_COLUMN_STEP
from mitosheet.steps.add_column import ADD_COLUMN_STEP
from mitosheet.steps.set_column_formula import SET_COLUMN_FORMULA_STEP
from mitosheet.steps.merge import MERGE_STEP
from mitosheet.steps.column_delete import DELETE_COLUMN_STEP
from mitosheet.steps.column_rename import RENAME_COLUMN_STEP

# All steps must be listed in this variable.
STEPS = [
    GROUP_STEP,
    REORDER_COLUMN_STEP,
    FILTER_STEP,
    ADD_COLUMN_STEP,
    SET_COLUMN_FORMULA_STEP,
    MERGE_STEP,
    DELETE_COLUMN_STEP,
    RENAME_COLUMN_STEP
]