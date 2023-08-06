"""utility.py

Utility submodule for pybioprox

Contains logger

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
import inspect
import logging
import coloredlogs


def get_logger(name=None):
    """
    Returns a logger for the current module
    """
    if name is None:
        name = inspect.getmodule(inspect.currentframe().f_back).__name__
    logger = logging.getLogger(name)
    # Default format for coloredlogs is
    # "%(asctime)s %(hostname)s %(name)s[%(process)d]
    # ... %(levelname)s %(message)s"
    coloredlogs.install(
        fmt="%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s",
        level='DEBUG', logger=logger
    )
    return logger
