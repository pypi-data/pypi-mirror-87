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

from typing import Dict

# Is of type float
total_time = 0.0

# Global counter for all tests
# total_tests -> Total number of tests to be run
# current_test -> The current test to be run
number_success = number_failed = total_tests = current_test = 0

# Displays the number of times a function has been tested
func_name = "(NONE)"
func_count = 1

file_name: str = "Interactive Mode"
