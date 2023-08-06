#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pprint import pprint
import re
import string
import sys

from pya2l.a2l_listener import ParserWrapper, A2LListener, cut_a2ml

from pya2l.allocprof import allocprof

#@allocprof
def main():
    #data = open(r"f:\projekte\csProjects\k-A2L\examples\cr6eus.aml").read()
    #data = open(r"f:\projekte\csProjects\pySART\pySART\fibex\CANape_Module_200.aml").read()
    #data = open(r"f:\projekte\csProjects\k-A2L\examples\crmin1.aml").read()

#    FNAME = r"f:\projekte\csProjects\k-A2L\examples\CCP_Examp_001.a2l"

#    FNAME = r"f:\projekte\csProjects\k-A2L\examples\engine_ecu.a2l"
#    FNAME = r"f:\projekte\csProjects\k-A2L\examples\ASAP2_Chris.a2l"

#################
#################
#################

    #FNAME = r"f:\projekte\csProjects\k-A2L\examples\CR6EU5-642-49D1.a2l"
    #DBFN = "CR6EU5-642-49D1.a2ldb"

    FNAME = r"f:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.a2l"
    DBFN = "ASAP2_Demo_V161.a2ldb"

    #FNAME = r"f:\projekte\csProjects\k-A2L\examples\example-a2l-file.a2l"
    #DBFN = "example-a2l-file.a2ldb"

    parser = ParserWrapper('a2l', 'a2lFile', A2LListener, debug = False)    #True False

    if len(sys.argv) < 2:
        sys.exit(1)
    fname = sys.argv[1]
    _, base = os.path.split(fname)
    fbase, _ = os.path.splitext(base)
    dbfn = "{}.a2ldb".format(fbase)

    try:
        os.unlink(dbfn)
    except Exception:
        pass
    data = open(fname).read()
    data, a2ml = cut_a2ml(data)

    tree = parser.parseFromString(data, dbname = dbfn)

if __name__ == '__main__':
    main()

