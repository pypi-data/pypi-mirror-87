#!/usr/bin/env python
# -*- coding: latin-1 -*-

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

"""
"""

import antlr4
from antlr4.BufferedTokenStream import BufferedTokenStream
from antlr4.error.ErrorListener import ErrorListener

from pya2l import a2llg
from pya2l import logger


SEGMENT = """
/begin SEGMENT
    0x0 0x2 0x0 0x0 0x0
    /begin PAGE
        0x0 ECU_ACCESS_DONT_CARE XCP_READ_ACCESS_WITH_ECU_ONLY XCP_WRITE_ACCESS_NOT_ALLOWED
    /end PAGE
    /begin PAGE
        0x1 ECU_ACCESS_DONT_CARE XCP_READ_ACCESS_WITH_ECU_ONLY XCP_WRITE_ACCESS_WITH_ECU_ONLY
    /end PAGE
/end SEGMENT
"""

EOF = -1


class EOFReached(Exception):
    """Signals end of token stream.
    """


def token_to_int(token):
    """
    """
    text = token.text
    if text.startswith(("0x", "0X")):
        return int(text, 16)
    else:
        return int(text, 10)

def token_to_float(token):
    """
    """
    return float(token.text)

class IfDataParser:
    """
    """

    def __init__(self, syntax):
        self.syntax = syntax

    def parse(self, buffer):
        """
        """
        input_stream = antlr4.InputStream(buffer)
        #input_stream = BufferedTokenStream(buffer)
        self.lexer = a2llg.a2llg(input_stream)
        self.tokens = self.lexer.getAllTokens()
        self.num_tokens = len(self.tokens)
        self.token_idx = 0
        while True:
            try:
                token = self.current_token()
            except EOFReached:
                break
            self.consume()
            if token.channel == token.HIDDEN_CHANNEL:
                continue

            if token.type == self.lexer.INT:
                res = token_to_int(token)
            print("{0:55s}{1}".format(str(token), self.type_as_str(token.type)))    # TODO: log/DEBUG

    def current_token(self):
        """Get the token at the current stream position.
        """
        if self.token_idx < self.num_tokens:
            return self.tokens[self.token_idx]
        else:
            raise EOFReached()

    def match(self, token_type):
        pass

    def consume(self):
        """Increment token stream position by one.
        """
        self.token_idx += 1

    def lookahead(self, n = 1):
        pass

    def block(self):
        pass

    def enum(self):
        pass

    def struct(self):
        pass

    def tagged_struct(self):
        pass

    def tagged_union(self):
        pass

    def type_as_str(self, type_):
        TYPE_MAP = {
            self.lexer.IDENT:     "IDENT",
            self.lexer.FLOAT:     "FLOAT",
            self.lexer.INT:       "INT",
            self.lexer.COMMENT:   "COMMENT",
            self.lexer.WS:        "WS",
            self.lexer.STRING:    "STRING",
            self.lexer.BEGIN:     "BEGIN",
            self.lexer.END:       "END",
        }
        return TYPE_MAP.get(type_)

    """
    // assign : ID '=' expr ';' ;
    void assign() { // method generated from rule assign
       match(ID); // compare ID to current input symbol then consume
        match('=');
        expr(); // match an expression by calling expr()
        match(';');
    }
    ///
    ///
    ///
    /** Match any kind of statement starting at the current input position */
    stat: assign // First alternative ('|' is alternative separator)
    | ifstat // Second alternative
    | whilestat
    ...
    ;
    A parsing rule for stat looks like a switch .
    void stat() {
       switch ( « current input token » ) {
            CASE ID : assign(); break;
            CASE IF : ifstat(); break; // IF is token type for keyword 'if'
            CASE WHILE : whilestat(); break;
        ...
            default : « raise no viable alternative exception »
       }
    }
    ///
    ///
    ///
    / ** To parse a statement, call stat();
    * /
    void stat() { returnstat(); }
    void returnstat() { match( "return" ); expr(); match( ";" ); }
    void expr() { match( "x" ); match( "+" ); match( "1" ); }

    void stat() {
        if ( « lookahead token is return » ) returnstat();
        else if ( « lookahead token is identifier » ) assign();
        else if ( « lookahead token is if » ) ifstat();
        else « parse error »
    }
    """


ip = IfDataParser(None)
res = ip.parse(SEGMENT)

"""
['BEGIN', 'COMMENT', 'DEFAULT_MODE', 'DEFAULT_TOKEN_CHANNEL', 'END', 'FLOAT', 'HEX', 'HIDDEN', 'IDENT', 'INT',
'MAX_CHAR_VALUE', 'MIN_CHAR_VALUE', 'MORE', 'SKIP', 'STRING', 'WS', '_actions', '_channel', '_factory',
'_hitEOF', '_input', '_interp', '_listeners', '_mode', '_modeStack', '_output', '_predicates', '_stateNumber',
'_text', '_token', '_tokenFactorySourcePair', '_tokenStartCharIndex', '_tokenStartColumn', '_tokenStartLine',
'_type', 'addErrorListener', 'atn', 'channelNames', 'checkVersion', 'column', 'decisionsToDFA', 'emit',
'emitEOF', 'emitToken', 'extractVersion', 'getAllTokens', 'getCharErrorDisplay', 'getCharIndex',
'getErrorDisplay', 'getErrorDisplayForChar', 'getErrorHeader', 'getErrorListenerDispatch', 'getRuleIndexMap',
'getTokenErrorDisplay', 'getTokenType', 'getTokenTypeMap', 'grammarFileName', 'inputStream', 'line',
'literalNames', 'mode', 'modeNames', 'more', 'nextToken', 'notifyListeners', 'popMode', 'precpred',
'pushMode', 'recover', 'removeErrorListener', 'removeErrorListeners', 'reset', 'ruleIndexMapCache',
'ruleNames', 'sempred', 'skip', 'sourceName', 'state', 'symbolicNames'
"""


"""
['DEFAULT_CHANNEL', 'EMPTY_SOURCE', 'EOF', 'EPSILON', 'HIDDEN_CHANNEL', 'INVALID_TYPE', 'MIN_USER_TOKEN_TYPE',
'_text', 'channel', 'clone', 'column', 'getInputStream', 'getTokenSource', 'line', 'source', 'start',
'stop', 'text', 'tokenIndex', 'type']
"""

