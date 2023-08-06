#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `set_cell_step` package."""

import pytest  # noqa: F401
import set_cell_step  # noqa: F401


def test_construction():
    """Just create an object and test its type."""
    result = set_cell_step.SetCell()
    assert str(type(result)) == (
        "<class 'set_cell_step.set_cell.SetCell'>"  # noqa: E501
    )
