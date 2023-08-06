#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

from pya2l.a2lparser import A2LParser
#reload(pya2l.a2lparser)

def main():
    #data = open(r"C:\projekte\csProjects\k-A2L\examples\engine_ecu.a2l").read()
    #tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\cr6eus.aml")
    #tree = pa.parseFromFile(r"c:\projekte\csProjects\pySART\pySART\fibex\CANape_Module_200.aml")
    #tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\crmin1.aml")
    #data = open(r"C:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.a2l").read()

    #parse(r"C:\projekte\csProjects\k-A2L\examples\CR6EU5-642-49D1.a2l")

    parser = A2LParser()
#    parser.parseFromFileName(r"f:\projekte\csProjects\k-A2L\examples\engine_ecu.a2l"
    #parser.parseFromFileName(r"C:\projekte\csProjects\k-A2L\examples\ASAP2_Chris.a2l")
    tree = parser.parseFromFileName(r"f:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.a2l")
    #parse(r"C:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.a2l")

if __name__ == '__main__':
    main()
