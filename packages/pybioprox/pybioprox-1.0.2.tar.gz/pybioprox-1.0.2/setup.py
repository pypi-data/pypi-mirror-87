#!/usr/bin/env python
"""
Setup script for pybioprox module

Copyright (C) 2020  Jeremy Metz

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
from typing import List
import importlib
from setuptools import setup, Command


__module_name__ = "pybioprox"


def create_cmdclass():
    """
    Adds coverage command class if coverage and pytest are available
    """
    try:
        importlib.import_module("coverage")
        importlib.import_module("pytest")
        return {
            "coverage": CoverageCommand
        }
    except ImportError:
        return {}


class CoverageCommand(Command):
    """Coverage Command"""
    description = "Run coverage on unit-tests (not integration tests!)"
    user_options: List = []

    def initialize_options(self):
        """init options"""
        pass

    def finalize_options(self):
        """finalize options"""
        pass

    def run(self):  # pylint: disable=no-self-use
        """runner"""
        # Coverage command
        # NOTE: Use API as follows for better control
        omitfiles = [
            os.path.join(__module_name__, "tests", "unit", "*"),
            os.path.join(__module_name__, "__main__.py"),
        ]
        for root, _, files in os.walk(__module_name__):
            omitfiles.extend(
                os.path.join(root, fname) for fname in
                filter(lambda f: f == "__init__.py", files)
            )
        coverage = importlib.import_module("coverage")
        pytest = importlib.import_module("pytest")

        print("Running coverage on", __module_name__)
        cov = coverage.Coverage(
            source=[__module_name__],
            omit=omitfiles,
            )
        cov.start()
        # Run normal tests
        # loader = unittest.TestLoader()
        # tests = loader.discover(__module_name__)
        # runner = unittest.runner.TextTestRunner()
        # runner.run(tests)
        pytest.main([])
        cov.save()
        cov.html_report()


setup(
    cmdclass=create_cmdclass(),
)
