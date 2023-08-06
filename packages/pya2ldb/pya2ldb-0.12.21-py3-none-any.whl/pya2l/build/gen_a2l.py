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

from pya2l.build import parse_classes
from pya2l import templates
import pya2l.classes as classes

HEADER = """
/begin A2ML

    enum datatype {
        "UBYTE"         = 0,
        "SBYTE"         = 1,
        "UWORD"         = 2,
        "SWORD"         = 3,
        "ULONG"         = 4,
        "SLONG"         = 5,
        "A_UINT64"      = 6,
        "A_INT64"       = 7,
        "FLOAT32_IEEE"  = 8,
        "FLOAT64_IEEE"  = 9
    };

    enum datasize {
        "BYTE"          = 0,
        "WORD"          = 1,
        "LONG"          = 2
    };

    enum addrtype {
        "PBYTE"         = 0,
        "PWORD"         = 1,
        "PLONG"         = 2,
        "DIRECT"        = 3
    };

    enum byteorder {
        "LITTLE_ENDIAN" = 0,
        "BIG_ENDIAN"    = 1,
        "MSB_LAST"      = 2,
        "MSB_FIRST"     = 3
    };

    enum indexorder {
        "INDEX_INCR"    = 0,
        "INDEX_DECR"    = 1
    };

"""

FOOTER = """

/end A2ML"""


def camel_case(name):
    splitty = [n.lower() for n in name.split('_')]
    result = []
    result.append(splitty[0])
    if len(splitty) > 1:
        for part in splitty[1 : ]:
            xxx = "{0}{1}".format(part[0].upper(), part[1: ])
            result.append(xxx)
    return ''.join(result)

def map_type(attr):
    TYPES = {
        classes.Uint:   "uint",
        classes.Int:    "int",
        classes.Ulong:  "ulong",
        classes.Long:   "long",
        classes.Float:  "float",
        classes.String: "char[256]",
        classes.Ident:  "char[1025]",
        classes.Datatype: "enum datatype",
        classes.Indexorder: "enum indexorder",
        classes.Addrtype: "enum addrtype",
        classes.Datasize: "enum datasize",
        classes.Byteorder: "enum byteorder",
    }
    if attr in TYPES:
        mappedType = TYPES[attr]
        return mappedType
    else:
        return None

LINE_ITEM = """<% import pya2l.classes as classes %>
${"(" if item.multiple else ""}${"block " if item.block else ""}"${tag}" struct ${utils.camel_case(tag)} {
%if item.attrs:
    /* mandatory part */
%endif
%for attr in item.attrs:
    %if 'Enum' in str(attr[0]):
    enum {  /* ${attr[1]} */
    %for idx, en in enumerate(attr[2]):
        %if idx < len(attr[2]) - 1:
        "${en}" = ${idx},
        %else:
        "${en}" = ${idx}
        %endif
    %endfor
    };
    %else:
%if len(attr) == 3 and attr[2] == classes.MULTIPLE:
    (${utils.map_type(attr[0])})*; /* ${attr[1]} ==> MULTIPLE */
%else:
    ${utils.map_type(attr[0])}; /* ${attr[1]}*/
%endif
    %endif
%endfor
%if item.children:
    /* optional part */
    taggedstruct {
%endif
%for child in item.children:
%if utils.parser.polymorphic(child):
            struct ${utils.parser.class_from_name(child).camel_case_name(False)};
%else:
${utils.line_item(child, utils, level + 1)}
%endif
%endfor
%if item.children:
    };
%endif
${"})*;" if item.multiple else "};"}
"""

parser = parse_classes.ClassParser()
parser.run()

def line_item(name, utils, level = 1):
    item = classes.KEYWORD_MAP[name]
    namespace = {"item": item, "level": level, "tag": name, "utils": utils,
    }
    return templates.doTemplateFromText(LINE_ITEM, namespace, level * 4, formatExceptions = False)

class Dummy(object): pass

utils = Dummy()
utils.parser = parser
utils.line_item = line_item
utils.camel_case = camel_case
utils.map_type = map_type

print(templates.doTemplateFromText(HEADER, {}, 0))

for item in [x[0] for x in parser.polymorphic_classes]:
    match = parse_classes.TYPE_NAME.match(str(item))
    tag = match.group(1)
    print(line_item(tag, utils, 1))

for child in classes.RootElement.children:
    print(line_item(child, utils, 1))

print(templates.doTemplateFromText(FOOTER, {}, 0))

#print(parser.enums)
