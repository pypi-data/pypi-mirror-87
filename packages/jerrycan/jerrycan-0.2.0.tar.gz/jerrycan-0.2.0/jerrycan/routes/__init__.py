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

from flask.blueprints import Blueprint
from typing import List, Tuple, Callable
from jerrycan.routes.static import define_blueprint as __static
from jerrycan.routes.user_management import define_blueprint \
    as __user_management
from jerrycan.routes.api.user_management import define_blueprint \
    as __api_user_management

blueprint_generators: List[Tuple[Callable[[str], Blueprint], str]] = [
    (__static, "static"),
    (__user_management, "user_management"),
    (__api_user_management, "api_user_management")
]
"""
Defines the functions used to create the various blueprints
as well as their names
"""
