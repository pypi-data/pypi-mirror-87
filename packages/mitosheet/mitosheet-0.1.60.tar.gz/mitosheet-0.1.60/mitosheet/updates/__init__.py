#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains the exports for update events, which are events that manipulate
the steps in some way, but do not _just generate a step_ (see ../steps for
more information about steps).

Examples of this sort of event are:
- Lots of steps being replayed from the front-end.
- A user undoing an existing step. 
"""

from mitosheet.updates.undo import UNDO_UPDATE


# All steps must be listed in this variable.
UPDATES = [
    UNDO_UPDATE
]