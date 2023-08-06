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

HEADER = """/*
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
*/


//
//  AUTOMATICALLY GENERATED FILE -- DO NOT MODIFY !!!
//

grammar a2l;

##options {
##   charVocabulary = '\\u0000' .. '\\u00ff';
##}

a2lFile:
    asap2Version?
    a2mlVersion?
    project
    ;
"""

"""

"""

FOOTER = """
integerValue:
    h = HEX | i = INT
    ;

numericValue:
    f = FLOAT | i = INT
    ;

stringValue:
    s = STRING
    ;

identifierValue:
    i += partialIdentifier ('.' i += partialIdentifier)*
    ;

partialIdentifier:
    i = IDENT (a += arraySpecifier)*
    ;

arraySpecifier:
    '[' (i = INT | n = IDENT) ']'
    ;

dataType:
    v = ('UBYTE' | 'SBYTE' | 'UWORD' | 'SWORD' | 'ULONG' | 'SLONG' |
    'A_UINT64' | 'A_INT64' | 'FLOAT32_IEEE' | 'FLOAT64_IEEE')
    ;

datasize:
    v = ('BYTE' | 'WORD' | 'LONG')
    ;

addrtype:
    v = ('PBYTE' | 'PWORD' | 'PLONG' | 'DIRECT')
    ;

byteOrderValue:
    v = ('LITTLE_ENDIAN' | 'BIG_ENDIAN' | 'MSB_LAST' | 'MSB_FIRST')
    ;

indexorder:
    v = ('INDEX_INCR' | 'INDEX_DECR')
    ;

BEGIN:
    '/begin'
    ;

END:
    '/end'
    ;

IDENT: [a-zA-Z_][a-zA-Z_0-9.]*;

fragment
EXPONENT : ('e'|'E') ('+'|'-')? ('0'..'9')+ ;

FLOAT:
   ('+' | '-')?
    (
        ('0'..'9')+ '.' ('0'..'9')* EXPONENT?
    |   '.' ('0'..'9')+ EXPONENT?
    |   ('0'..'9')+ EXPONENT
    )
    ;

INT: ('+' | '-')? '0'..'9'+
    ;

HEX:   '0'('x' | 'X') ('a' .. 'f' | 'A' .. 'F' | '0' .. '9')+
    ;

COMMENT:
    ('//' ~('\\n'|'\\r')* '\\r'? '\\n'
    |   '/*' .*? '*/')
        -> channel(HIDDEN)
    ;

WS  :   (' ' | '\\t' | '\\r' | '\\n') -> channel(HIDDEN)
    ;

STRING:
    '"' ( ESC_SEQ | ~('\\\\'|'"') )* '"'
    ;

fragment
HEX_DIGIT : ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
ESC_SEQ
    :   '\\\\'
        (   // The standard escaped character set such as tab, newline, etc.
            [btnfr"'\\\\]
        |   // A Java style Unicode escape sequence
            UNICODE_ESC
        |   // Invalid escape
            .
        |   // Invalid escape at end of file
            EOF
        )
    ;

fragment
UNICODE_ESC
    :   'u' (HEX_DIGIT (HEX_DIGIT (HEX_DIGIT HEX_DIGIT?)?)?)?
;

fragment
OCTAL_ESC:
    '\\\\' ('0'..'3') ('0'..'7') ('0'..'7')
    |   '\\\\' ('0'..'7') ('0'..'7')
    |   '\\\\' ('0'..'7')
    ;
"""


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
        classes.Uint:       "integerValue",
        classes.Int:        "integerValue",
        classes.Ulong:      "integerValue",
        classes.Long:       "integerValue",
        classes.Float:      "numericValue",
        classes.String:     "stringValue",
        classes.Ident:      "identifierValue",
        classes.Datatype:   "dataType",
        classes.Indexorder: "indexorder",
        classes.Addrtype:   "addrtype",
        classes.Datasize:   "datasize",
        classes.Byteorder:  "byteOrderValue",
    }
    if attr in TYPES:
        mappedType = TYPES[attr]
        return mappedType
    else:
        return None


def map_attribute_name(name):
    RESERVED = {
        "byteOrder",
        "monotony",
        "unit",
        "stepSize",
        "deposit",
        "formula",
        "characteristic",
        "format",
        "number",
        "version",
        "customer",
        "dataSize",
        "mode",
        "type",
        "value",
    }
    if name in RESERVED:
        if name == "format":
            return "format__"
        else:
            return "{}_".format(name)
    else:
        return name

def map_class_name(name):
    RESERVED = {
        "format",
    }
    if name in RESERVED:
        return "{}_".format(name)
    else:
        return name

LINE_ITEM = """<% import pya2l.classes as classes
klass = utils.parser.class_from_name(tag)
%>
${utils.map_class_name(utils.camel_case(tag))}:
    ${"BEGIN" if item.children or item.block else ""} '${tag}'
%for attr in item.attrs:
    %if 'Enum' in str(attr[0]):
    <% block = True if len(attr[2]) > 1 else False %>
    ${utils.map_attribute_name(utils.lower_first(attr[1]))} =
    %if block:
    (
    %endif
    %for idx, en in enumerate(attr[2]):
        %if idx < len(attr[2]) - 1:
        '${en}' |
        %else:
        '${en}'
        %endif
    %endfor
    %if block:
    )
    %endif

    %else:
%if len(attr) == 3 and attr[2] == classes.MULTIPLE:
    (${utils.map_attribute_name(utils.lower_first(attr[1]))} += ${utils.map_type(attr[0])})*
%else:
    ${utils.map_attribute_name(utils.lower_first(attr[1]))} = ${utils.map_type(attr[0])}
%endif
    %endif
%endfor
%if tag == 'COMPU_TAB':
    (inVal += numericValue outVal += numericValue)*
%elif tag == 'COMPU_VTAB':
    (inVal += numericValue outVal += stringValue)*
%elif tag == 'COMPU_VTAB_RANGE':
    (inValMin += numericValue inValMax += numericValue outVal += stringValue)*
%elif tag == 'VAR_FORBIDDEN_COMB':
    (criterionName += identifierValue criterionValue += identifierValue)*
%endif
%if item.children:
    /* optional part */
<% references = utils.parser.references[klass] %>
    (
%for idx, fk in enumerate(references):
%if idx < len(references) - 1:
        v_${utils.map_class_name(fk.camel_case_name(False))} += ${utils.map_class_name(fk.camel_case_name(False))} |
%else:
        v_${utils.map_class_name(fk.camel_case_name(False))} += ${utils.map_class_name(fk.camel_case_name(False))}
%endif
%endfor
    )*
%endif
%if item.children or item.block :
    END '${tag}'
%endif
    ;
%for child in item.children:
%if not utils.parser.polymorphic(child):
${utils.line_item(child, utils)}
%endif
%endfor
"""

parser = parse_classes.ClassParser()
parser.run()

def line_item(name, utils):
    item = classes.KEYWORD_MAP[name]
    namespace = {"item": item, "tag": name, "utils": utils,
    }
    return templates.doTemplateFromText(LINE_ITEM, namespace, formatExceptions = False)


def lower_first(value):
    return "{}{}".format(value[0].lower(), value[1 : ])

class Dummy(object): pass

utils = Dummy()
utils.parser = parser
utils.line_item = line_item
utils.camel_case = camel_case
utils.map_type = map_type
utils.lower_first = lower_first
utils.map_attribute_name = map_attribute_name
utils.map_class_name = map_class_name

print(templates.doTemplateFromText(HEADER, {}, 0))

for item in [x[0] for x in parser.polymorphic_classes]:
    match = parse_classes.TYPE_NAME.match(str(item))
    tag = match.group(1)
    print(line_item(tag, utils))

for child in classes.RootElement.children:
    print(line_item(child, utils))

print(templates.doTemplateFromText(FOOTER, {}, 0))

