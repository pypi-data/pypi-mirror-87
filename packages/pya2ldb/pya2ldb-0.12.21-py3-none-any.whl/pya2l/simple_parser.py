#!/usr/bin/env python
# -*- coding: utf-8 -*-

from a2l import a2l
import antlr4

#FNAME = r"C:\projekte\csProjects\k-A2L\examples\ifdata_USB.a2l"
FNAME = r"C:\projekte\csProjects\XCP\pyxcp\aml\ifdata_USB.a2l"

ips = antlr4.InputStream(open(FNAME).read())
lexer = a2l(ips)
cts = antlr4.CommonTokenStream(lexer)


from pprint import pprint
from pya2l import aml
from pya2l.a2l_lexer import Tokenizer, TokenType
from pya2l.a2l_parser import A2LParser
import pya2l.ifdata as ifdata

import json

pa = aml.ParserWrapper('aml', 'amlFile')

#    data = open(r"C:\projekte\csProjects\k-A2L\examples\cr6eus.aml").read()

#tree = pa.parseFromFile(r"c:\projekte\csProjects\pySART\pySART\fibex\CANape_Module_200.aml")
#tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\crmin1.aml")

tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\full.aml")

#data = """
#/begin A2ML
#{}
#    "XCP" struct {{
#        block "XCP_ON_USB" struct {{
#            struct USB_Parameters;  /* specific for USB      */
#            //taggedstruct Common_Parameters;  /* overruling of default */
#        }};
#    }};
#/end A2ML
#""".format(open(r"C:\projekte\csProjects\XCP\pyxcp\aml\XCPonEth.aml").read())

#pprint(data)

#data = "/begin A2ML {} /end A2ML".format(open(r"C:\projekte\csProjects\XCP\pyxcp\aml\XCPonEth.aml").read())
#tree = pa.parseFromString(data)
print("Finished ANTLR parsing.")

#json.dump(tree.value, open("amlfull.json", "w"))

#pprint(tree.value)


#for child in tree.children:
#    if hasattr(child, "value"):
#        pprint(child.value)
    #ppp = ifdata.Parser(tree)
    ##parser = ppp.build()

"""
['DEFAULT_CHANNEL', 'EMPTY_SOURCE', 'EOF', 'EPSILON', 'HIDDEN_CHANNEL', 'INVALID_TYPE', 'MIN_USER_TOKEN_TYPE',

'__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__',
'__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
'__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_text',

'channel', 'clone', 'column', 'getInputStream', 'getTokenSource', 'line', 'source', 'start', 'stop', 'text', 'tokenIndex', 'type']

"""
#print(dir(a2l))
TOKENS = (
    'COMMENT', 'DEFAULT_MODE', 'HIDDEN', 'DEFAULT_TOKEN_CHANNEL',
    'MAX_CHAR_VALUE', 'MIN_CHAR_VALUE', 'MORE', 'SKIP', 'WS',

    'BEGIN', 'END', 'FLOAT', 'HEX', 'IDENT', 'INT', 'STRING'
)

class Parser(object):

    def __init__(self, lexer, ctx):
        self.lexer = lexer
        self.ctx = ctx

    def nextToken(self):
        return self.lexer.nextToken()

    def parse(self):
        self.lookahead, self.token = self.nextToken(), None

        while True:
            if self.token.type == token.EOF:
                break
            if self.token.channel == token.DEFAULT_CHANNEL:
                print("type: {} - text: {}".format(self.token.type, self.token.text))
            self.accept([])

    def accept(*toktypes):
        if self.lookahead and self.lookahead.type in toktypes:
            self.token, self.lookahead = self.nextToken(), None
            return True
        else:
            return False

    def declaration(self):
        pass

    def block(self):
        pass

    def primitive(self):
        pass

    def enum(self):
        pass

    def struct(self):
        pass

    def taggedStruct(self):
        pass

    def taggedUnion(self):
        pass

ctx = tree.value

##
## pyXCP: Unterscheiden zw. user- und lolovel (NAME[base])- API!
##

class FrontEnd(object):

    def __init__(self, ctx):
        self.types = dict()
        self.blocks = dict()
        self.decls = dict()
        for idx in range(len(ctx)):
            df = ctx[idx]
            if df.blockDefinition:
                print("BLOCK", df.blockDefinition.typename.name)
                self.blocks[df.blockDefinition.typename.name] = df.blockDefinition.typename.type.members
                entry = ((df.blockDefinition.classname, df.blockDefinition.typename.name), df.blockDefinition.typename.type.members) # df.blockDefinition.typename.type.classname,
            elif df.typeDefinition:
                # df.typeDefinition.typename.type.classname, i.e. TaggedUnion
                # df.typeDefinition.typename.type.members -> list /w types.
                print("TYPE", df.typeDefinition.typename.type.classname, df.typeDefinition.typename.name)
                if df.typeDefinition.typename.type.classname != 'Enumeration':
                    self.types[df.typeDefinition.typename.name] = df.typeDefinition.typename.type.members
                    entry = ((df.typeDefinition.typename.type.classname, df.typeDefinition.typename.name), df.typeDefinition.typename.type.members)
                else:
                    self.types[df.typeDefinition.typename.name] = df.typeDefinition.typename.type.enumerators
                    entry = ((df.typeDefinition.typename.type.classname, df.typeDefinition.typename.name), df.typeDefinition.typename.type.enumerators)
            key, value = entry
            self.decls[key] = value
        pprint(self.decls.keys())

fe = FrontEnd(ctx)

parser = Parser(lexer, fe)
parser.parse()


import re
import types
from collections import namedtuple

tokens = [
    r'(?P<NUMBER>\d+)',
    r'(?P<PLUS>\+)',
    r'(?P<MINUS>-)',
    r'(?P<TIMES>\*)',
    r'(?P<DIVIDE>/)',
    r'(?P<WS>\s+)'
]

Token = namedtuple('Token', ['type', 'value'])
lex = re.compile('|'.join(tokens))

def tokenize(text):
    scan = lex.scanner(text)
    gen = (Token(m.lastgroup, m.group())
    for m in iter(scan.match, None) if m.lastgroup != 'WS')
        return gen

class Node:
    _fields = []

    def __init__(self, *args):
        for attr, value in zip(self._fields, args):
            setattr(self, attr, value)

class Number(Node):
    _fields = ['value']

class BinOp(Node):
    _fields = ['op', 'left', 'right']

    def parse(toks):
        lookahead, current = next(toks, None), None

        def accept(*toktypes):
            nonlocal lookahead, current

            if lookahead and lookahead.type in toktypes:
                current, lookahead = lookahead, next(toks, None)
            return True

        def expr():
            left = term()
            while accept('PLUS', 'MINUS'):
                left = BinOp(current.value, left)
                left.right = term()
            return left

        def term():
            left = factor()
            while accept('TIMES', 'DIVIDE'):
                left = BinOp(current.value, left)
                left.right = factor()
        return left

        def factor():
            if accept('NUMBER'):
                return Number(int(current.value))
            else:
                raise SyntaxError()
        return expr()

class NodeVisitor:

    def visit(self, node):
        stack = [self.genvisit(node)]
        ret = None
        while stack:
            try:
                node = stack[-1].send(ret)
                stack.append(self.genvisit(node))
                ret = None
            except StopIteration as e:
                stack.pop()
                ret = e.value
            return ret

    def genvisit(self, node):
        ret = getattr(self, 'visit_' + type(node).__name__)(node)
        if isinstance(ret, types.GeneratorType):
            ret = yield from ret
        return ret

class Evaluator(NodeVisitor):

    def visit_Number(self, node):
    return node.value

    def visit_BinOp(self, node):
        leftval = yield node.left
        rightval = yield node.right

        if node.op == '+':
            return leftval + rightval
        elif node.op == '-':
            return leftval - rightval
        elif node.op == '*':
            return leftval * rightval
        elif node.op == '/':
            return leftval / rightval

    def evaluate(exp):
        toks = tokenize(exp)
        tree = parse(toks)
        return Evaluator().visit(tree)

exp = '2 * 3 + 5 / 2'
print(evaluate(exp))
exp = '+'.join([str(x) for x in range(10000)])
print(evaluate(exp))

