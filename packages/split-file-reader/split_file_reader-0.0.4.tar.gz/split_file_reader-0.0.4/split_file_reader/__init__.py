# -*- coding: utf-8 -*-
"""
    A module for the manipulation of disparate data streams as single, coherent data streams.
"""
"""
    split_file_reader
    Copyright (C) 2020  Xavier Halloran, United States

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


__version__ = '0.0.4'

import logging

# Squelch warnings about missing log handlers.
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .split_file_reader import SplitFileReader

__all__ = ["SplitFileReader"]
