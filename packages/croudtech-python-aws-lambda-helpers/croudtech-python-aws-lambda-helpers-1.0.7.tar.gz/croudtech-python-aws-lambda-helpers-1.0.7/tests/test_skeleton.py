# -*- coding: utf-8 -*-

import pytest
from croudtech_python_aws_lambda_helpers.skeleton import fib

__author__ = "Jim Robinson"
__copyright__ = "Jim Robinson"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
