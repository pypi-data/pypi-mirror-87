# /usr/bin/env python

# This file is part of checkdigit.

# checkdigit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# checkdigit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with checkdigit.  If not, see <http://www.gnu.org/licenses/>.

"""Parity Validation Functions.

UPC-A codes are the main variant of Universal Product Codes.
They contain 12 digits and are mainly used for product identification.

For more information, please look at the wiki page for this module:
https://github.com/harens/checkdigit/wiki/📦-UPC-A

"""

from checkdigit import isbn

# WARNING: Data beginning with 0 must be as a string due to PEP 3127

# ISBN calculations are very similar to that of UPC
# The only major difference is that the ODD instead of even placed digits are multiplied by 3

# Spaces and hyphens do not need to be removed
# This is since it's removed by the ISBN-13 Function


def calculate(data: str) -> str:
    """Calculates UPC Check Digits.

    Args:
        data: A string of UPC digits

    Returns:
        str: The missing check digit
    """
    return isbn.calculate13(data, "upc")


def validate(data: str) -> bool:
    """Determines if the calculated check digit of the data is the last digit given.

    Args:
        data: A string of characters representing a full UPC code

    Returns:
        bool: A boolean representing whether the check digit validates the data or not
    """
    return calculate(data[:-1]) == data[-1]
