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

from enum import Enum
from typing import Dict, Any
from jerrycan.base import db
from jerrycan.db.ModelMixin import ModelMixin
from jerrycan.test.TestFramework import _TestFramework


class TestModelMixin(_TestFramework):
    """
    Class that tests the ModelMixin class
    """

    def test_enum_attributes(self):
        """
        Tests if enum attributes are handled correctly
        :return: None
        """
        class A(Enum):
            B = 1
            C = 2

        class Tester(ModelMixin, db.Model):
            enum = db.Column(db.Enum(A))

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        tester = Tester(id=1, enum=A.B)
        self.assertEqual(repr(tester), "Tester(id=1, enum=A.B)")
        self.assertEqual(tester.__json__()["enum"], "B")

    def test_json_representation(self):
        """
        Tests the JSOn representation of a ModelMixin
        :return: None
        """
        class A(ModelMixin, db.Model):
            __tablename__ = "a"
            s = db.Column(db.String(255))

        class B(ModelMixin, db.Model):
            __tablename__ = "b"
            a_id = db.Column(db.Integer, db.ForeignKey("a.id"))
            a = db.relationship("A")
            user_id: int = db.Column(
                db.Integer,
                db.ForeignKey("users.id"),
                nullable=False
            )

        # noinspection PyArgumentList
        b1 = B(a=A(), a_id=1)
        # noinspection PyArgumentList
        b2 = B(a=None)
        self.assertNotEqual(b1.__json__(), b2.__json__())
        self.assertNotEqual(b1.__json__(True), b2.__json__(True))
