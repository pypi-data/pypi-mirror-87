#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint
from pya2l import aml
from pya2l.a2l_lexer import Tokenizer, TokenType
from pya2l.a2l_parser import A2LParser
import pya2l.ifdata as ifdata

import jsonpickle as jsp

def main():
    pa = aml.ParserWrapper('aml', 'amlFile')


#    data = open(r"C:\projekte\csProjects\k-A2L\examples\cr6eus.aml").read()

    #tree = pa.parseFromFile(r"c:\projekte\csProjects\pySART\pySART\fibex\CANape_Module_200.aml")
    #tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\crmin1.aml")

    data = "/begin A2ML {} /end A2ML".format(open(r"C:\projekte\csProjects\XCP\pyxcp\aml\XCPonEth.aml").read())
    tree = pa.parseFromString(data)
    print("Finished ANTLR parsing.")
#    for child in tree.children:
#        if hasattr(child, "value"):
#            print(jsp.dumps(child.value))
    #ppp = ifdata.Parser(tree)
    ##parser = ppp.build()

main()
