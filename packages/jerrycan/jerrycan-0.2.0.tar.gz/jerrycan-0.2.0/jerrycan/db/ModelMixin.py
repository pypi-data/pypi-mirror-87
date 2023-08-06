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
from typing import Dict, Any, Type, Optional, List
from jerrycan.base import db
from sqlalchemy.inspection import inspect


class ModelMixin:
    """
    A mixin class that specifies a couple of methods all database
    models should implement
    """

    id = db.Column(
        db.Integer, primary_key=True, nullable=False, autoincrement=True
    )
    """
    The ID is the primary key of the table and increments automatically
    """

    def __json__(
            self,
            include_children: bool = False,
            ignore_keys: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generates a dictionary containing the information of this model
        :param include_children: Specifies if children data models will be
                                 included or if they're limited to IDs
        :param ignore_keys: If provided, will not include any of these keys
        :return: A dictionary representing the model's values
        """
        if ignore_keys is None:
            ignore_keys = []

        json_dict = {}

        relations: Dict[str, Type] = {
            key: value.mapper.class_
            for key, value in inspect(self.__class__).relationships.items()
        }

        for attribute in inspect(self).attrs:
            key = attribute.key
            value = attribute.value
            relation_cls = relations.get(key)

            if key in ignore_keys:
                continue
            elif key.endswith("_hash"):  # Skip password hashes etc
                continue
            elif isinstance(value, Enum):
                value = value.name
            elif relation_cls is not None and \
                    issubclass(relation_cls, ModelMixin):

                recursion_keys = []
                other_relations = \
                    list(inspect(relation_cls).relationships.values())
                for other_relation in other_relations:
                    other_relation_cls = other_relation.mapper.class_
                    if other_relation_cls == self.__class__:
                        recursion_keys.append(other_relation.key)
                recursion_keys += ignore_keys

                if include_children and value is not None:
                    if isinstance(value, list):
                        value = [
                            x.__json__(include_children, recursion_keys)
                            for x in value
                        ]
                    else:
                        value = value.__json__(
                            include_children, recursion_keys
                        )
                elif include_children and value is None:
                    value = None
                else:
                    assert not include_children
                    continue  # pragma: no cover

            json_dict[attribute.key] = value

        return json_dict

    def __str__(self) -> str:
        """
        :return: The string representation of this object
        """
        data = self.__json__()
        _id = data.pop("id")
        return "{}:{} <{}>".format(self.__class__.__name__, _id, str(data))

    def __repr__(self) -> str:
        """
        :return: A string with which the object may be generated
        """
        params = ""
        json_repr = self.__json__()

        enums = {}
        for key in json_repr:
            attr = getattr(self, key)
            if isinstance(attr, Enum):
                enum_cls = attr.__class__.__name__
                enum_val = attr.name
                enums[key] = "{}.{}".format(enum_cls, enum_val)

        for key, val in self.__json__().items():
            repr_arg = enums.get(key, repr(val))
            params += "{}={}, ".format(key, repr_arg)

        params = params.rsplit(",", 1)[0]

        return "{}({})".format(self.__class__.__name__, params)

    def __eq__(self, other: Any) -> bool:
        """
        Checks the model object for equality with another object
        :param other: The other object
        :return: True if the objects are equal, False otherwise
        """
        if "__json__" in dir(other):
            return other.__json__() == self.__json__()
        else:
            return False  # pragma: no cover

    def __hash__(self) -> int:
        """
        Creates a hash so that the model objects can be used as keys
        :return: None
        """
        return self.id
