#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__="""
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2017 by Christoph Schueler <github.com/Christoph2,
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

from collections import OrderedDict
import codecs
from pprint import pprint

from pya2l import aml
import pya2l.classes as classes
import pya2l import model
from pya2l.a2l_lexer import Tokenizer, TokenType
from pya2l.aml import ParserWrapper
from pya2l.utils import slicer, createStringBuffer
from pya2l.logger import Logger

VERSION = 'ASAM MCD-2MC V1.6'

MAX_IDENT           = 1024
MAX_PARTIAL_IDENT   = 128
MAX_STRING          = 255

IDENT_EXPR          = r'^(?:[a-zA-Z_][a-zA-Z_0-9]*\.?)+(?:\[(?:\d+ | [a-zA-Z_][a-zA-Z_0-9]*)\])?'

STATE_NORMAL        = 1
STATE_COLLECT       = 2
STATE_A2ML          = 3

from collections import namedtuple

Token = namedtuple('Token', 'lineNo tokenType lexem')

def dumpElement(element, level = 0):
    level += 1
    indent = " " * level
    if isinstance(element, (str, int, long, tuple)):
        print("{0}{1}".format(indent, element))
        return
    print("{0}<<{1}>>".format(indent, element.__class__.__name__))
    for attr in element.attrs:
        print("{0}{1} = {2}".format(indent, attr, getattr(element, attr)))
    for child in element.children:
        parseAml(getattr(element, child), level)
    level -= 1


def parseAml(element, level = 0):
    if isinstance(element, (list, tuple)):
        for el in element:
            dumpElement(el, level)
    elif isinstance(element, (str, int, long)):
        print("{0}".format(element))
    elif element is None:
        #print("<<NONE>>")
        pass
    else:
        dumpElement(element, level)


def dumpTree(tree):
    for child in tree.children:
        print(child)
        dumpTree(child)

class A2LParser(object):

    def __init__(self):
        self.logger = Logger(self, 'parser')

    def parseFromFileName(self, filename):
        #fp = codecs.open(filename, encoding = "utf8")
        fp = codecs.open(filename, encoding = "latin1")
        self.parse(fp)

    def parseFromString(self, stringObj):
        self.parse(stringObj)

    def parse(self, fp):
        keywords = classes.KEYWORD_MAP.keys()
        self.filename = fp.name if hasattr(fp, 'name') else "<<buffer>>"
        returnCode, source = self.uncomment(fp)
        #pprint(source)
        if not returnCode:
            return
        source = ''.join(source)
        tokenizer = Tokenizer(self.filename, source, keywords)

        classStack = []
        classStack.append(classes.RootElement)

        instanceStack = []
        #instanceStack.append(classes.instanceFactory("Root"))
        instanceStack.append(model.instanceFactory("Root"))
        pushToInstanceStack = False
        self.lineNo = None

        while tokenizer.tokenAvailable():
            self.lineNo, (tokenType, lexem) = tokenizer.getToken()
            spaces = "  " * len(classStack)
            print("%s[%s]%s:%s" % (spaces, tokenType, lexem, self.lineNo))
            #print("STACKS: {} {}".format(len(classStack), len(instanceStack)))
            if self.lineNo in (46, 3348):
                print("HALT")

            if lexem == 'DP_BLOB/begin':
                print(lexem)

            if tokenType == TokenType.AML:
                parserWrapper = aml.ParserWrapper('aml', 'amlFile')
                tree = parserWrapper.parseFromString(lexem)
                #parseAml(tree.value)
                continue
            else:
                pass

            if tokenType == TokenType.BEGIN:
                self.lineNo, (tokenType, lexem) = tokenizer.getToken()   # Move on.
                print("%s[%s]%s:%s" % (spaces, tokenType, lexem, self.lineNo))
                if lexem == 'IF_DATA':
                    print("IF_DATA section -- STOP!!!")
                    while True:
                        self.lineNo, (tokenType, lexem) = tokenizer.getToken()
                        #print("[%s]%s:%s" % (tokenType, lexem, self.lineNo))
                        if tokenType == TokenType.END:
                            self.lineNo, (tokenType, lexem) = tokenizer.getToken()
                            #print("[%s]%s:%s" % (tokenType, lexem, self.lineNo))
                            if lexem == 'IF_DATA':
                                break
                    continue
                else:
                    pushToInstanceStack = True
                    klass = classes.KEYWORD_MAP.get(lexem)
                    classStack.append(klass)
            elif tokenType == TokenType.END:
                self.lineNo, (tokenType, lexem) = tokenizer.getToken()   # Move on.
                print("%s[%s]%s:%s" % (spaces, tokenType, lexem, self.lineNo))
                closingClass = classStack.pop()
                if closingClass.__name__ != lexem:
                    self.logger.error("/end statement: expected '{}' got '{}'.".format(closingClass.__name__ , lexem))

                instanceStack.pop()
                continue
            elif tokenType == TokenType.KEYWORD:
                klass = classes.KEYWORD_MAP.get(lexem)
            if classStack:
                tos = classStack[-1]
            if tokenType in (TokenType.BEGIN, TokenType.KEYWORD):
                fixedAttributes =  klass.fixedAttributes
                variableAttribute =  klass.variableAttribute
                numParameters = len(fixedAttributes)

                parameters = [tokenizer.getToken() for _ in range(numParameters)]
                attributeValues = [x[1][1] for x in parameters]
                #inst = classes.instanceFactory(lexem.title(), **OrderedDict(zip(fixedAttributes, attributeValues)))
                inst = model.instanceFactory(lexem.title(), **OrderedDict(zip(fixedAttributes, attributeValues)))
                if variableAttribute:
                    attr = klass[variableAttribute]
                    result = []
                    while True:
                        self.lineNo, (tokenType, lexem) = tokenizer.getToken()
                        #print(tokenType, lexem)
                        if tokenType in (TokenType.KEYWORD, TokenType.END):
                            tokenizer.stepBack()
                            break
                        result.append(lexem)
                    setattr(inst, attr[1], result)
                    inst.attrs.append(attr[1])
                elif tokenType == TokenType.KEYWORD and lexem in ('COMPU_TAB', 'COMPU_VTAB', 'COMPU_VTAB_RANGE'):
                    #
                    # COMPU_TAB / COMPU_VTAB / COMPU_VTAB_RANGE require special attention.
                    #
                    attribute = "Items"
                    if lexem == 'COMPU_VTAB_RANGE':
                        sliceLength = 3
                        valueClass = classes.CompuTriplet
                        variablePart = [tokenizer.getToken() for _ in range(inst.NumberValueTriples * sliceLength)]
                    else:
                        valueClass = classes.CompuPair
                        sliceLength = 2
                        variablePart = [tokenizer.getToken() for _ in range(inst.NumberValuePairs * sliceLength)]
                    variablePartValues = [v[1][1] for v in variablePart]
                    result = slicer(variablePartValues, sliceLength, valueClass)
                    inst.attrs.append(attribute)
                    setattr(inst, attribute, result)
                #print inst
                instanceStack[-1].children.append(inst)
                if pushToInstanceStack:
                    instanceStack.append(inst)
                    pushToInstanceStack = False
        dumpTree(instanceStack[0])


    def uncomment(self, fp): # Nested comments are not supported!
        result = []
        multiLineComment = False
        inComment = False
        returnCode = True
        for lineNo, line in enumerate(fp):
            # Bad style state-machine...
            self.lineNo = lineNo
            if not multiLineComment:
                if '//' in line:
                    cmtPos = line.index('//')
                    line = line[ : cmtPos].strip()
                    if line:
                        result.append(line)
                elif '/*' in line:
                    cmtPos = line.index('/*')
                    startLineNo = lineNo
                    if not '*/' in line:
                        multiLineComment = True
                        inComment = True
                    line = line[ : cmtPos].strip()
                    if line:
                        result.append(line)
                else:
                    if line:
                        result.append(line)
            else:
                if '*/' in line:
                    cmtPos = line.index('*/')
                    result.append(line[cmtPos + 2: ].strip())
                    multiLineComment = False
                    inComment = False
                elif '/*' in line:
                    if inComment:
                        self.logger.error("Nested comments are not allowed.")
                        returnCode = False
        if multiLineComment:
            self.logger.error("Premature end-of-file while processing comment.")
            returnCode = False
        return (returnCode, result)

