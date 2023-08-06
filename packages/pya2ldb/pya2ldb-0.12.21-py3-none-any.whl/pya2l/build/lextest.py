
import os

import six


from pya2l import aml


class A2LParser(object):

    def __init__(self):
        pass
#        self.logger = Logger(self, __name__)

    def parseFromFileName(self, filename, encoding = "latin1"):
        """
        """
        pth, fname = os.path.split(filename)
        self.fnbase = os.path.splitext(fname)[0]
        fp = six.io.open(filename, encoding = encoding)
        self.parse(fp)

    def parseFromString(self, stringObj):
        self.fnbase = ":memory:"
        self.parse(six.StringIO(stringObj))

    def parse(self, fp):
#        self.db = model.A2LDatabase(self.fnbase, debug = True)
        pa = aml.LexerWrapper('a2llg', 'a2lFile')
        data = fp.read()
#        match = AML.search(data)
#        if match:
#            header = data[0 : match.start()]
#            amlS = data[match.start() : match.end()]
#            lineCount = amlS.count('\n')
#            footer = data[match.end() : -1]
#            data = header + '\n' * lineCount + footer
        tokenStream = pa.lexFromString(data)
        print("Finished ANTLR lexing.")
        while True:
            tok =  tokenStream.LT(1)
            print("{:25}{}".format(tok.text, tok.type))
            if tok.type == -1:
                break;
            tokenStream.consume()
#        walker = A2LWalker(tokenStream, self.db)
#        walker.run()
        print("Finished walking.")
#        self.db.session.flush()
#        self.db.session.commit()

pa = A2LParser()

#pa.parseFromFileName(r"f:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.a2l")
pa.parseFromFileName(r"lex.a2l")


