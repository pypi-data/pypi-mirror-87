#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

from a2l import a2l
import antlr4

#FNAME = r"C:\projekte\csProjects\k-A2L\examples\ifdata_USB.a2l"

#FNAME = r"C:\projekte\csProjects\XCP\pyxcp\aml\ifdata_USB.a2l"

FNAME = r'../examples/ASAP2_Demo_V161_ifdata_section.a2l'

class Database(object):

    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.Connection(filename)
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def createDictFromRow(self, row, description):
        names = [d[0] for d in description]
        di = dict(zip(names, row))
        return di

    def getCursor(self):
        return self.conn.cursor()

    def beginTransaction(self):
        self.conn.execute("BEGIN TRANSACTION")

    def commitTransaction(self):
        self.conn.commit()

    def rollbackTransaction(self):
        self.conn.rollback()

    def insertOrReplaceStatement(self, insert, cur, tname, columns, *values):
        verb = "INSERT OR FAIL" if insert else "REPLACE"
        try:
            placeholder = ','.join("?" * len(values))
            stmt = "{} INTO {}({}) VALUES({})".format(verb, tname, columns, placeholder)
            cur.execute(stmt, [*values])
        except sqlite3.DatabaseError as e:
            msg = "{} - Data: {}".format(str(e), values)
            self.logger.error(msg)
            return None
        else:
            return self.lastInsertedRowId(cur, tname)

    def insertStatement(self, cur, tname, columns, *values):
        return self.insertOrReplaceStatement(True, cur, tname, columns, *values)

    def replaceStatement(self, cur, tname, columns, *values):
        return self.insertOrReplaceStatement(False, cur, tname, columns, *values)

    def fetchFromTable(self, tname, columns = None, where = None, orderBy = None):
        cur = self.getCursor()
        whereClause = "" if not where else "WHERE {}".format(where)
        orderByClause = "ORDER BY rowid" if not orderBy else "ORDER BY {}".format(orderBy)
        result = cur.execute("""SELECT * FROM {} {} {}""".format(tname, whereClause, orderByClause), [])
        while True:
            row = cur.fetchone()
            if row is None:
                return
            else:
                yield self.createDictFromRow(row, cur.description)


class Parser(object):

    def __init__(self, db):
        self.db = db

    def toplevel(self):
        return self.db.fetchFromTable("Declaration", orderBy = "rowid")

def main():
    db = Database("asap.sq3")
    parser = Parser(db)
    ips = antlr4.InputStream(open(FNAME).read())
    lexer = a2l(ips)
    cts = antlr4.CommonTokenStream(lexer)
    print(dir(cts))
    for token in lexer.getAllTokens():
        if token.channel == a2l.DEFAULT_TOKEN_CHANNEL:
            print(token)
    print(list(parser.toplevel()))

if __name__ == '__main__':
    main()


