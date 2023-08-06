#!/usr/bin/env python

"""Tests for `testing_project` package."""

__author__ = """Elle Smith"""
__contact__ = "eleanor.smith@stfc.ac.uk"
__copyright__ = "Copyright 2020 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"

from testing_project.testing_project import my_function


def test_my_function():
    resp = my_function()
    assert resp == "Hello World"
