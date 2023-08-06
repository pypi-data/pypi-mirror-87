"""LICENSE
Copyright 2020 Hermann Krumrey <hermann@krumreyh.com>

This file is part of jerrycan.

jerrycan is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

jerrycan is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with jerrycan.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""


class ApiException(Exception):
    """
    Api raised when an API-related exception occurs
    """

    def __init__(self, reason: str, status_code: int):
        """
        Initializes the exception
        :param reason: The reason the API Exception was raised
        :param status_code: The status code associated with the exception
        """
        super().__init__(reason)
        self.reason = reason
        self.status_code = status_code
