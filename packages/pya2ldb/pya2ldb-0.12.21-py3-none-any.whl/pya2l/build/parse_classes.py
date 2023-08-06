#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__="""
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2019 by Christoph Schueler <github.com/Christoph2,
                                        cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

from sortedcontainers import SortedSet

from collections import defaultdict
from io import StringIO
from pprint import pprint
from operator import attrgetter, itemgetter
import re

from pya2l import templates
import pya2l.classes as classes


TYPE_NAME = re.compile(r"^<class\s'pya2l\.classes\.(?P<klass>.*?)(?:Type)?'>$", re.DOTALL)

class ClassParser(object):

    def __init__(self):
        self.values = [c for c in classes.KEYWORD_MAP.values()]
        self.positions = {}
        self.enums = defaultdict(list)
        self.referenced_by = defaultdict(SortedSet)
        self.references = defaultdict(SortedSet)
        for idx, val in enumerate(self.values):
            self.positions[idx] = val
        self.inv()

    def inv(self):
        self.positions_inv = {v:k for k, v in self.positions.items()}

    def swap(self, l, r):
        tmp = self.positions[self.positions_inv[l]]
        self.positions[self.positions_inv[l]] = self.positions[self.positions_inv[r]]
        self.positions[self.positions_inv[r]] = tmp
        self.inv()

    def _filter_enums(self, klass):
        for attr in klass.attrs:
            if issubclass(attr[0], classes.Enum):
                self.enums[klass].append((attr[1], attr[2]))

    def run(self):
        iterations = 0
        swaps = None
        while swaps != 0:
            swaps = 0
            for k, v in self.positions.items():
                for c in v.children:
                    child = classes.KEYWORD_MAP[c]
                    self._filter_enums(child)
                    self.referenced_by[child].add(v)
                    self.references[v].add(child)
                    childPos = self.positions_inv[child]
                    elemPos = self.positions_inv[v]
                    if elemPos < childPos:
                        self.swap(v, child)
                        swaps += 1
            iterations += 1
        self.polymorphic_classes = sorted(list(x for x in self.referenced_by.items() if len(x[1]) > 1), key = lambda o: repr(o))
        self.polymorphic_classes_set = {k for k, v in self.polymorphic_classes}

    def class_from_name(self, name):
        return classes.KEYWORD_MAP[name]

    def polymorphic(self, child):
        return classes.KEYWORD_MAP[child] in self.polymorphic_classes_set

