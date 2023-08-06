#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__="""
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2020 by Christoph Schueler <github.com/Christoph2,
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

from collections import defaultdict
from pprint import pprint
from operator import attrgetter, itemgetter
import re

from pya2l import templates
import pya2l.classes as classes
import pya2l.utils


TYPE_NAME = re.compile(r"^<class\s'pya2l\.classes\.(?P<klass>.*?)(?:Type)?'>$", re.DOTALL)

HEADER = """
<%
asap2_version = session.query(model.Asap2Version).first()
a2ml_version = session.query(model.A2mlVersion).first()
project = session.query(model.Project).first()
%>
"""

FOOTER = """
"""
## \\\\n
STRUCTURE = """<% from pya2l import classes %>\
${"%if"} ${tag.lower()}:
%if item.multiple:
${"%for"} ${"entry{}".format(level)} in ${tag.lower()}:
    ${"/begin " if item.block else ""}${tag}
    %for attr in item.attrs:
%if len(attr) == 3 and attr[2] == classes.MULTIPLE:
MULTIPLE
%endif
        ${'"' if attr[0] == classes.String else ''}${"${"}${"entry{}".format(level)}.${utils.lower_first(attr[1])}}${'"' if attr[0] == classes.String else ''}  /* ${utils.lower_first(attr[1])} */
    %endfor
    %for child in item.children:
        ${"<%"} ${child.lower()} = ${"entry{}".format(level)}.${child.lower()} ${"%>\"}
        ${utils.structure(child, utils, level + 1)}
    %endfor
    %if item.block:
    /end ${tag}
    %endif
${"%endfor"}
%else:
${"/begin " if item.block else ""}${tag}
%for attr in item.attrs:
%if len(attr) == 3 and attr[2] == classes.MULTIPLE:
    ##MULTIPLE
    ##${"${"}${tag.lower()}.${utils.lower_first(attr[1])}${"}"}
%if tag in ("VAR_CHARACTERISTIC", "DEPENDENT_CHARACTERISTIC", "VIRTUAL_CHARACTERISTIC"):
    ${'${" ".join([str(x) for x in'} ${tag.lower()}.${utils.lower_first(attr[1])}.name ${'])}'}
%else:
    ${'''${" ".join(["{1:}{0:}{1:}".format(str(x),'''} ${''' '"' ''' if attr[0] == classes.String else '""'}) for x in ${tag.lower()}.${utils.lower_first(attr[1])} ${'])}'}
%endif
%else:
    ${'"' if attr[0] == classes.String else ''}${"$"}{${tag.lower()}.${utils.lower_first(attr[1])}}${'"' if attr[0] == classes.String else ''}  /* ${utils.lower_first(attr[1])} */
%endif
%endfor
%for child in item.children:
${"<%"} ${child.lower()} = ${tag.lower()}.${child.lower()} ${"%>\"}
${utils.structure(child, utils, level + 1)}
%endfor
%if item.block:
/end ${tag}
%endif
%endif
${"%endif\"}"""

class Builder(object):

    def __init__(self):
        self.values = [c for c in classes.KEYWORD_MAP.values()]
        self.positions = {}
        self.referencedBy = defaultdict(set)
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

    def run(self):
        iterations = 0
        swaps = None
        while swaps != 0:
            swaps = 0
            for k, v in self.positions.items():
                for c in v.children:
                    child = classes.KEYWORD_MAP[c]
                    self.referencedBy[child].add(v)
                    childPos = self.positions_inv[child]
                    elemPos = self.positions_inv[v]
                    if elemPos < childPos:
                        self.swap(v, child)
                        swaps += 1
            iterations += 1

ab = Builder()
ab.run()
toFactorOut = sorted(list(x for x in ab.referencedBy.items() if len(x[1]) > 1), key = lambda o: repr(o))
restOfUs = list(x for x in ab.referencedBy.items() if len(x[1]) <= 1)
toFactorOutClasses = {k for k, v in toFactorOut}

toProcess = [x[1] for x in ab.positions.items() if x[1] not in toFactorOutClasses]

def structure(name, utils, level):
    item = classes.KEYWORD_MAP[name]
    namespace = {"item": item, "level": level, "tag": name, "utils": utils}
    return templates.doTemplateFromText(STRUCTURE, namespace, level * 2, formatExceptions = False)

def lower_first(value):
    return "{}{}".format(value[0].lower(), value[1 : ])

#def escape(attr):
#    result = '"' if attr[0] == classes.String else ''}${"$"}
#        {${tag.lower()}.${utils.lower_first(attr[1])}}
#       ${'"' if attr[0] == classes.String else ''}

class Dummy(object): pass

utils = Dummy()
utils.structure = structure
utils.lower_first = lower_first

#for item in [x[0] for x in toFactorOut]:
#    match = TYPE_NAME.match(str(item))
#    tag = match.group(1)
#    print(structure(tag, utils, 1))
    #print("//", "-" * 60)
print(HEADER)

for child in classes.RootElement.children:
    print(structure(child, utils, 1))
    previous = child

print(templates.doTemplateFromText(FOOTER, {}, 0, formatExceptions = False))

