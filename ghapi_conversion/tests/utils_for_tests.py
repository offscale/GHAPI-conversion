"""
Shared utility functions used by tests
"""

from unittest import main


def unittest_main():
    """ Runs unittest.main if __main__ """
    if __name__ == "__main__":
        main()


def mock_function(*args, **kwargs):
    """
    Mock function to check if it is called

    :returns: True
    :rtype: ```Literal[True]```
    """
    return True


__all__ = ["unittest_main"]