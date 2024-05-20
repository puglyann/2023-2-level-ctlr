"""
Common functions for checks.
"""

import sys


def check_result(return_code: int) -> None:
    """
    Check result and exit if failed.

    Args:
        return_code (int): Return code of check
    """
    print(return_code)
    if return_code != 0:
        print("Check failed.")
        sys.exit(1)
    else:
        print("Check passed.")
