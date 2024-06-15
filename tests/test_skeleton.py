import pytest
from gilda_opts.skeleton import main

__author__ = "Marcelo Matus"
__copyright__ = "Marcelo Matus"
__license__ = "EPL-1.0"


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    # main(["-h"])


#     captured = capsys.readouterr()
#     #assert "The 7-th Fibonacci number is 13" in captured.out
