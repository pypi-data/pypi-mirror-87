# /usr/bin/env python

# This file is part of error404.

# error404 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# error404 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with error404.  If not, see <http://www.gnu.org/licenses/>.

from error404 import config
from sys import modules, exit
import __main__ as main

# Checks if being run in .ipnyb file
in_ipnyb = "ipykernel" in modules

# If file is being run in Interactive Mode (i.e. IDLE, iPython, etc.)
interactive_mode = not hasattr(main, "__file__")


def test_results(decimal_points: int = 4) -> None:
    """Overview of test results.

    Provides extended information about how successful the tests were
    Outputted once all tests are complete

    If run explicitly, results are only returned if more than one test was run

    Returns:
        exit(1) if any test fails
    """
    if (
        config.total_tests != 0
    ):  # Output only if tests were run (or always if in interactive)
        func_time = round(config.total_time, decimal_points)
        print("\n" * 2)
        if config.number_failed == 0:
            print(
                f"Out of {config.total_tests} tests, all succeeded in {func_time} seconds"
            )
        elif config.number_success == 0:
            print(
                f"Out of {config.total_tests} tests, all failed in {func_time} seconds"
            )
            if not in_ipnyb and not interactive_mode:
                exit(1)
        # If some tests failed and others succeeded
        else:
            print(
                f"Out of {config.total_tests} tests, {config.number_success} succeeded and {config.number_failed} failed in {func_time} seconds"
            )
            success_rate = (config.number_success / config.total_tests) * 100
            # Success rate rounded to 2 d.p.
            print(f"This gives a success rate of {round(success_rate, 2)}%")
            if not in_ipnyb and not interactive_mode:
                exit(1)
    clear_results()


def clear_results() -> None:
    """Clears total test successes/failures

    Does not return any values
    """
    config.number_success = (
        config.number_failed
    ) = config.total_tests = config.total_time = config.current_test = 0

    config.func_name = "(NONE)"
    config.func_count = 1
