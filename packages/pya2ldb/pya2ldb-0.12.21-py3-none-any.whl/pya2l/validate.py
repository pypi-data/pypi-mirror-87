#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__="""
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2020 by Christoph Schueler <cpu12.gems@googlemail.com>

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

"""Validate A2L database according to ASAP2 rules (and more...).
"""

from collections import Counter, namedtuple
import enum
from itertools import combinations, filterfalse

from pya2l import DB
import pya2l.model as model


# *** Validator generated no diagnostic messages ***

Message = namedtuple("Message", "type category diag_code text")


class Type:
    INFORMATION = 1
    WARNING     = 2
    ERROR       = 3


class Category:
    DUPLICATE   = 1
    MISSING     = 2
    OBSOLETE    = 3


class Diagnostics:
    MULTIPLE_DEFINITIONS_IN_NAMESPACE   = 1
    DEFINITION_IN_MULTIPLE_NAMESPACES   = 2
    INVALID_C_IDENTIFIER                = 3


MAX_C_IDENTIFIER_LEN    = 32    # ISO C90.

# any(len(e) > MAX_C_IDENTIFIER_LEN for e in 'CM.VTAB_RANGE.DEFAULT_VALUE.REF'.split("."))
# Some part of '{}' are longer than 32 chars (ISO C90 limit).

def names(objs):
    """
    """
    return [o.name for o in objs]


class Validator:
    """
    Paramaters
    ----------
    session: Sqlite3 database session object.
    """

    def __init__(self, session):
        self.session = session
        self._diagnostics = []
        self._identifier = {}

    def __call__(self):
        """Run validation.
        """
        self.check_namespaces()

    def duplicate_ids(self, objs):
        """
        """
        cnt = Counter(names(objs))
        #cnt["CM.TAB_NOINTP.NO_DEFAULT_VALUE.REF"] = 3
        dups = filterfalse(lambda x: x[1] == 1, cnt.items())
        print(list(names(objs)), end = "\n\n")
        return list(dups)

    def add_diagnostic(self, type_, category, diag_code, text):
        pass

    def _load_module_identifiers(self):
        TABLES = ("axis_pts", "characteristic", "compu_method", "compu_tab", "compu_vtab", "compu_vtab_range",
            "frame", "function", "group", "measurement", "mod_common", "mod_par", "record_layout", "unit",
            "user_rights", "variant_coding",
        )

    def check_uniqueness(self, module, tables):
        table_combinations = combinations(tables,2 )    # Pairwise.
        print("TC:", list(table_combinations))

    def check_namespaces(self):
        """
        """
        modules = self.session.query(model.Module).all()
        for module in modules:
            print(module)
            self.check_uniqueness(module, ("compu_vtab", "compu_vtab_range", "compu_tab"))
            self.check_uniqueness(module, ("axis_pts", "characteristic", "measurement"))
            dups = self.duplicate_ids(module.compu_tab)
            if dups:
                for dup, cnt in dups:
                    print("COMPU_TAB: multiple occurrences of identifier '{}'.".format(dup))
            print("TAB:", names(module.compu_tab), end = "\n\n")
            print("VTAB:", names(module.compu_vtab), end = "\n\n")
            print("VTAB-RANGE:", names(module.compu_vtab_range), end = "\n\n")

    @property
    def diagnostics(self):
        return self._diagnostics
