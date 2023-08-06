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

from inspect import stack
from time import time
from sys import modules
import __main__ as main
from error404 import config, test_results
from typing import Any

# Checks if being run in .ipnyb file
in_ipnyb = "ipykernel" in modules

# If file is being run in Interactive Mode (i.e. IDLE, iPython, etc.)
interactive_mode = not hasattr(main, "__file__")


def test(function: Any, value: Any = True) -> None:
    """error404 Default Test Function

    Concept based on spscah test function
    Note that any data type can be accepted as a value

    Args:
        function: Function to be run
        value: Expected value
    Returns:
        Outputs whether test failed/succeeded. If failed, additional information supplied
    """
    start_time: float = time()  # Time taken

    # Retrieves info about the caller function from the stack
    line_num = str(stack()[1][2])

    # If it isn't running in interactive mode or if it's in a .pynb
    # File and function name is determined
    if not interactive_mode or in_ipnyb:
        function_name = "".join(stack()[1][4])

        config.file_name = stack()[1][1]
        if not in_ipnyb:
            with open(config.file_name) as f:
                contents = (
                    f.read()
                )  # Counts the total number of tests written in the file
                config.total_tests = contents.count("test(")
    else:
        config.file_name = "Interactive Mode"
        function_name = "(Function("

    # Where the user's function begins and finishes
    starting_bracket: int = function_name.index("(") + 1
    finish_bracket: int = function_name.index("(", starting_bracket + 1)

    # Removes irrelevent info from code_context
    function_name = function_name[starting_bracket:finish_bracket]

    # Increases function counter if the same function is retested
    if config.func_name == function_name:
        config.func_count += 1
    else:
        config.func_name = function_name
        config.func_count = 1

    # If the output was expected
    if function == value:
        print(f"✅ {function_name} ({config.func_count}) Succeeded")
        config.number_success += 1
    else:
        print(
            f"\n❌ {function_name} ({config.func_count}) failed at line {line_num} in {config.file_name}"
        )
        # Format adds output data types
        print(f"Program Output: {function} ({type(function).__name__})")
        print(f"Expected Output: {value} ({type(value).__name__})\n")
        config.number_failed += 1
    config.current_test += 1
    config.total_time += time() - start_time

    if in_ipnyb or interactive_mode:
        config.total_tests += 1
    elif (
        config.current_test == config.total_tests
    ):  # Runs when all counted tests have finished
        test_results()
