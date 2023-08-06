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

from setuptools import setup, find_packages

if __name__ == "__main__":

    setup(
        name="jerrycan",
        version=open("version", "r").read(),
        description="A python library that contains commonly used routes, "
                    "database models and functions for flask applications",
        long_description=open("README.md", "r").read(),
        long_description_content_type="text/markdown",
        author="Hermann Krumrey",
        author_email="hermann@krumreyh.com",
        classifiers=[
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
        ],
        url="https://gitlab.namibsun.net/namibsun/python/jerrycan",
        license="GNU GPL3",
        packages=find_packages(),
        install_requires=[
            "flask",
            "flask-sqlalchemy",
            "flask-login",
            "sqlalchemy",
            "cheroot",
            "werkzeug",
            "sentry-sdk[flask]",
            "blinker",
            "bokkichat",
            "python-telegram-bot",
            "puffotter[crypto]"
        ],
        test_suite='nose.collector',
        tests_require=['nose'],
        include_package_data=True,
        zip_safe=False
    )
