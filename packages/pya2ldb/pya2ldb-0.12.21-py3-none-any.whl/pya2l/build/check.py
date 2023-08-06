
import enum
import sys

import antlr4
from pprint import pprint
from pya2l import aml


def main():
    pa = aml.ParserWrapper('aml', 'amlFile')

    tree = pa.parseFromFile(sys.argv[1])
    print("Finished ANTLR parsing.")
    pprint(tree.value, indent = 4)

if __name__ == '__main__':
    main()
