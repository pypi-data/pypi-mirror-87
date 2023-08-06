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

HEADER = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2010-2020 by Christoph Schueler <cpu12.gems.googlemail.com>

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

   s. FLOSS-EXCEPTION.txt
"""
__author__  = 'Christoph Schueler'
__version__ = '0.1.0'

import codecs
from decimal import Decimal as D
import importlib
from pprint import pprint
import sys

import six
import antlr4
import antlr4.tree

from pydbc.logger import Logger


def indent(level):
    print(" " * level,)

def dump(tree, level = 0):
    indent(level)
    if isinstance(tree, antlr4.TerminalNode):
        print(tree.symbol.text)
    else:
        print("({}".format(tree.value))
        level += 1
        for child in tree.children:
            dump(child, level)
        level -= 1
    indent(level)
    print(")")


class BaseListener(antlr4.ParseTreeListener):
    """
    """

    value = []
    logger = Logger(__name__)

    def getList(self, attr):
        return [x.value for x in attr] if attr else []

    def getTerminal(self, attr):
        return attr().getText() if attr() else ''

    def exitIntegerValue(self, ctx):
        if ctx.i:
            ctx.value = int(ctx.i.text, 10)
        elif ctx.h:
            ctx.value = int(ctx.h.text, 16)
        else:
            ctx.value = None

    def exitFloatValue(self, ctx):
        if ctx.f:
            ctx.value = D(ctx.f.text)
        elif ctx.i:
            ctx.value = D(ctx.i.text)
        else:
            ctx.value = None

    def exitNumber(self, ctx):
        if ctx.i:
            value = ctx.i.value
        elif ctx.f:
            value = ctx.f.value
        else:
            value = None
        ctx.value = value
        #print("NUM", ctx.value)

    def exitStringValue(self, ctx):
        ctx.value = ctx.s.text.strip('"') if ctx.s else None
        #print("STR", ctx.value)

    def exitIdentifierValue(self, ctx):
        ctx.value = ctx.i.text if ctx.i else None
        #print("ID", ctx.value)

    def _formatMessage(self, msg, location):
        return "[{0}:{1}] {2}".format(location.start.line, location.start.column + 1, msg)

    def _log(self, method, msg, location = None):
        if location:
            method(self._formatMessage(msg, location))
        else:
            method(msg)

    def info(self, msg, location = None):
        self._log(self.info.warn, msg, location)

    def warn(self, msg, location = None):
        self._log(self.logger.warn, msg, location)

    def error(self, msg, location = None):
        self._log(self.logger.warn, msg, location)

    def debug(self, msg, location = None):
        self._log(self.logger.warn, msg, location)


class ParserWrapper(object):
    """
    """
    def __init__(self, grammarName, startSymbol, listener = None):
        self.grammarName = grammarName
        self.startSymbol = startSymbol
        self.lexerModule, self.lexerClass = self._load('Lexer')
        self.parserModule, self.parserClass = self._load('Parser')
        self.listener = listener

    def _load(self, name):
        className = '{0}{1}'.format(self.grammarName, name)
        moduleName = 'pya2l.py{0}.{1}'.format(2 if six.PY2 else 3, className)
        module = importlib.import_module(moduleName)
        klass = getattr(module, className)
        return (module, klass, )

    def parse(self, input, trace = False):
        lexer = self.lexerClass(input)
        tokenStream = antlr4.CommonTokenStream(lexer)
        parser = self.parserClass(tokenStream)
        parser.setTrace(trace)
        meth = getattr(parser, self.startSymbol)
        self._syntaxErrors = parser._syntaxErrors
        tree = meth()
        if self.listener:
            listener = self.listener()
            walker = antlr4.ParseTreeWalker()
            walker.walk(listener, tree)
            return listener.value
        else:
            return tree

    def parseFromFile(self, fileName, encoding = 'latin-1', trace = False):
        return self.parse(ParserWrapper.stringStream(fileName, encoding), trace)

    def parseFromString(self, buf, encoding = 'latin-1', trace = False):
        return self.parse(antlr4.InputStream(buf), trace)

    @staticmethod
    def stringStream(fname, encoding = 'latin-1'):
        return antlr4.InputStream(codecs.open(fname, encoding = encoding).read())

    def _getNumberOfSyntaxErrors(self):
        return self._syntaxErrors

    numberOfSyntaxErrors = property(_getNumberOfSyntaxErrors)


class A2LListener(BaseListener):

'''

"""

"""

FOOTER = """
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
        classes.Float:      "floatValue",
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
    def exit${klass.camel_case_name(True)}(self, ctx):
        pass

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

