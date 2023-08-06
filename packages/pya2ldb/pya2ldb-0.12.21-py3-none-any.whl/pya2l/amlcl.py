#!/usr/bin/env python
# -*- coding: utf-8 -*-

import enum
import antlr4
from pprint import pprint
from pya2l import aml
from a2l import a2l
#from pya2l.a2l_lexer import Tokenizer, TokenType
#from pya2l.a2l_parser import A2LParser
#import pya2l.ifdata as ifdata

import sqlite3


class PredefinedType(enum.IntEnum):
    CHAR = 0
    INT = 1
    LONG = 2
    UCHAR = 3
    UINT = 4
    ULONG = 5
    DOUBLE = 6
    FLOAT = 7


class ParentType(enum.IntEnum):
    NONE = 0
    DECLARATION = 1
    BLOCK_DEFINITION = 2
    TYPE_DEFINITION = 3
    TAGGED_UNION = 4
    TAGGED_STRUCT = 5
    STRUCT = 6
    TAGGED_UNION_MEMBER = 7
    MEMBER = 8
    TAGGED_STRUCT_MEMBER = 9
    ENUMERATION = 10
    TYPENAME = 11


class Parent:

    def __init__(self, parentType, parentId):
        self.parentType = parentType
        self.parentId = parentId



SCHEMA = '''

''', '''
    CREATE TABLE Enumeration (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        UNIQUE(parent_type, parent_id),
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE Enumerator (
        id INTEGER NOT NULL DEFAULT 0,
        tag TEXT NOT NULL,
        constant INTEGER NOT NULL,
        enumeration INTEGER NOT NULL,
        FOREIGN KEY(enumeration) REFERENCES Enumeration(id),
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TaggedUnion (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        UNIQUE(parent_type, parent_id),
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TaggedUnionMember (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE Member (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TypeName (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        type CHAR(64),
        tag CHAR(256),
        name CHAR(256),
        PRIMARY KEY(id)
    );
''',  '''
    CREATE TABLE PredefinedType (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        type INT NOT NULL,
        PRIMARY KEY(id)
    );
''','''
    CREATE TABLE StructType (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        UNIQUE(parent_type, parent_id),
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TaggedStructType (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TaggedStructDefinition (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TaggedStructMember (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE Declaration (
        id INTEGER NOT NULL DEFAULT 0,
        dtype CHAR(256),
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE BlockDefinition (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        tag CHAR(256),
        UNIQUE(parent_type, parent_id),
        PRIMARY KEY(id)
    );
''', '''
    CREATE TABLE TypeDefinition (
        id INTEGER NOT NULL DEFAULT 0,
        parent_type INTEGER NOT NULL,
        parent_id INTEGER NOT NULL,
        UNIQUE(parent_type, parent_id),
        PRIMARY KEY(id)
    );
''', '''
    CREATE VIEW schema AS SELECT * FROM sqlite_master;
'''

class Database(object):

    def __init__(self, filename = ":memory:"):
        self.conn = sqlite3.connect(filename, isolation_level = None)
        self.conn.isolation_level = None
        self.cur = self.conn.cursor()
        self.filename = filename
        self.createSchema()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def createSchema(self):
        self.cur.execute("PRAGMA foreign_keys = ON;")

        self.cur.execute('PRAGMA synchronous = OFF')
        self.cur.execute('PRAGMA LOCKING_MODE = EXCLUSIVE')
        self.cur.execute("BEGIN TRANSACTION;")
        for item in SCHEMA:
            print(item)
            res = self.cur.execute(item)
        self.conn.commit()

    def lastInsertedRowId(self, cur, table):
        rowid = cur.lastrowid
        result = cur.execute("SELECT id FROM {} WHERE rowid = ?".format(table), [rowid]).fetchone()
        return result[0]

    def getCursor(self):
        return self.conn.cursor()

    def beginTransaction(self):
        self.conn.execute("BEGIN TRANSACTION")

    def commitTransaction(self):
        self.conn.commit()

    def rollbackTransaction(self):
        self.conn.rollback()

    def createDictFromRow(self, row, description):
        names = [d[0] for d in description]
        di = dict(zip(names, row))
        return di

    def fetchSingleRow(self, tname, column, where):
        cur = self.getCursor()
        cur.execute("""SELECT {} FROM {} WHERE {}""".format(column, tname, where))
        row = cur.fetchone()
        if row is None:
            return []
        return self.createDictFromRow(row, cur.description)

    def fetchSingleValue(self, tname, column, where):
        cur = self.getCursor()
        cur.execute("""SELECT {} FROM {} WHERE {}""".format(column, tname, where))
        result = cur.fetchone()
        if result is None:
            return []
        return result[0]

    def queryStatement(self, tname, columns = None, where = None, orderBy = None):
        pass

    def insertOrReplaceStatement(self, insert, cur, tname, columns, *values):
        verb = "INSERT OR FAIL" if insert else "REPLACE"
        try:
            placeholder = ','.join("?" * len(values))
            stmt = "{} INTO {}({}) VALUES({})".format(verb, tname, columns, placeholder)
            cur.execute(stmt, [*values])
        except sqlite3.DatabaseError as e:
            msg = "{} - Data: {}".format(str(e), values)
            #self.logger.error(msg)
            print(msg)
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


class Builder(object):

    def __init__(self, db):
        self.db = db

    def execFunc(self, fn, tree):
        print("eF", tree.keys())
        func = self.FUNCS.get(fn)
        print(func)
        return func(self, tree)

    def blockDefinition(self, tree, parent):
        print("blockDefinition", tree.tag, tree.keys())
        rid = self.db.insertStatement(self.db.cur, "BlockDefinition", "parent_type, parent_id, tag", parent.parentType, parent.parentId, tree.tag)
        par = Parent(ParentType.BLOCK_DEFINITION, rid)
        member = tree['member']
        typename = tree['typename']
        if member:
            self.member(member, par)
        if typename:
            self.typename(typename, par)

    def typeDefinition(self, tree, parent):
        print("typeDefinition", tree.keys())
        rid = self.db.insertStatement(self.db.cur, "TypeDefinition", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.TYPE_DEFINITION, rid)
        typename = tree['typename']
        if typename:
            self.typename(typename, par)

    def declaration(self, tree):
        print("declaration", tree.classname)
        rid = self.db.insertStatement(self.db.cur, "Declaration", "dtype", "xXx")
        par = Parent(ParentType.DECLARATION, rid)
        print("\t\tROWID:", rid)
        bd = tree['blockDefinition']
        td = tree['typeDefinition']
        if bd:
            self.blockDefinition(bd, par)
        if td:
            self.typeDefinition(td, par)

    def taggedUnionMember(self, tree, parent):
        print("taggedUnionMember", tree.tag)
        rid = self.db.insertStatement(self.db.cur, "TaggedUnionMember", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.TAGGED_UNION_MEMBER, rid)
        member = tree['member']
        bd = tree['blockDefinition']
        if member:
            self.member(member, par)
        if bd:
            self.blockDefinition(bd, par)

    def taggedUnion(self, tree, parent):
        print("taggedUnion", tree.name)
        rid = self.db.insertStatement(self.db.cur, "TaggedUnion", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.TAGGED_UNION, rid)
        for member in tree['members']:
            self.taggedUnionMember(member, par)

    def structType(self, tree, parent):
        print("structType", tree.name)
        rid = self.db.insertStatement(self.db.cur, "StructType", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.STRUCT, rid)
        for member in tree['members']:
            self.member(member, par)

    def taggedStructDefinition(self, tree, parent):
        print("\ttaggedStructDefinition", tree.tag, tree.mult, tree.keys())
        rid = self.db.insertStatement(self.db.cur, "TaggedStructDefinition", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.TAGGED_STRUCT, rid)
        member = tree['member']
        if member:
            self.member(member, par)

    def taggedStructMember(self, tree, parent):
        print("taggedStructMember", tree.mult)
        rid = self.db.insertStatement(self.db.cur, "TaggedStructMember", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.TAGGED_STRUCT_MEMBER, rid)
        td = tree['taggedstructDefinition']
        bd = tree['blockDefinition']
        if bd:
            self.blockDefinition(bd, par)
        if td:
            self.taggedStructDefinition(td, par)

    def taggedStructType(self, tree, parent):
        print("taggedStructType", tree.name)
        rid = self.db.insertStatement(self.db.cur, "TaggedStructType", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.TAGGED_STRUCT, rid)
        for member in tree['members']:
            self.taggedStructMember(member, par)

    def predefinedType(self, tree, parent):
        print("PredefinedType", tree.name)
        typeName = tree.name
        if typeName == 'char':
            typeCode = PredefinedType.CHAR
        elif typeName == 'int':
            typeCode = PredefinedType.INT
        elif typeName == 'long':
            typeCode = PredefinedType.LONG
        elif typeName == 'uchar':
            typeCode = PredefinedType.UCHAR
        elif typeName == 'uint':
            typeCode = PredefinedType.UINT
        elif typeName == 'ulong':
            typeCode = PredefinedType.ULONG
        elif typeName == 'double':
            typeCode = PredefinedType.DOUBLE
        elif typeName == 'float':
            typeCode = PredefinedType.FLOAT
        rid = self.db.insertStatement(self.db.cur, "PredefinedType", "parent_type, parent_id, type", parent.parentType, parent.parentId, typeCode)

    def enumerator(self, tree, parent):
        print("Enumerator", tree.tag, tree.constant)
        rid = self.db.insertStatement(self.db.cur, "Enumerator", "enumeration, tag, constant", parent.parentId, tree.tag, tree.constant)

    def enumeration(self, tree, parent):
        print("Enumeration", tree.name)
        rid = self.db.insertStatement(self.db.cur, "Enumeration", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.ENUMERATION, rid)
        for en in tree['enumerators']:
            self.enumerator(en, par)

    def typeProcessor(self, tree, parent):
        cn = tree.classname
        if cn == "TaggedUnion":
            self.taggedUnion(tree, parent)
        elif cn == 'StructType':
            self.structType(tree, parent)
        elif cn == 'TaggedStructType':
            self.taggedStructType(tree, parent)
        elif cn == 'PredefinedType':
            self.predefinedType(tree, parent)
        elif cn == 'Enumeration':
            self.enumeration(tree, parent)
        else:
            print("TYPE???", cn)

    def typename(self, tree, parent):
        print("typename", tree.tag, tree.name)
        rid = self.db.insertStatement(self.db.cur, "Typename", "parent_type, parent_id, type, tag, name", parent.parentType, parent.parentId, tree.type.classname, tree.tag, tree.name)
        par = Parent(ParentType.TYPENAME, rid)
        self.typeProcessor(tree['type'], par)

    def member(self, tree, parent):
        print("member", tree.arraySpecifier)
        rid = self.db.insertStatement(self.db.cur, "Member", "parent_type, parent_id", parent.parentType, parent.parentId)
        par = Parent(ParentType.MEMBER, rid)
        typename = tree['typename']
        if typename:
            self.typename(typename, par)

    def traverseTree(self, tree):
        self.db.beginTransaction()
        for item in tree:
            print("ITEM:", item.keys())
            self.execFunc(item['classname'], item)
        self.db.commitTransaction()

    FUNCS = {
        'Declaration': declaration,
        'BlockDefinition': blockDefinition,
        'TypeDefinition': typeDefinition,
    }

class Opcode: pass


class Seq(Opcode): pass


class Alt(Opcode): pass


class Rep(Opcode): pass


class Opt(Opcode): pass


class BlockDefinition(object):

    def __init__(self, db, rid, par, tag):
        self.db = db
        self.parent = par
        self.rid = rid
        self.tag = tag
        print("TAG:", self.tag)

    @property
    def member(self):
        return self.db.fetchFromTable("Member", where = "parent_type = {} AND parent_id = {}".format(ParentType.BLOCK_DEFINITION, self.rid))

    @property
    def typename(self):
        return self.db.fetchFromTable("Typename", where = "parent_type = {} AND parent_id = {}".format(ParentType.BLOCK_DEFINITION, self.rid))

class Parser(object):

    def __init__(self, db):
        self.db = db

    def toplevel(self):
        result = []
        print(list(self.db.fetchFromTable("BlockDefinition", where = "parent_type = {}".format(ParentType.DECLARATION), orderBy = "rowid")))
        print(list(self.db.fetchFromTable("TypeDefinition", where = "parent_type = {}".format(ParentType.DECLARATION), orderBy = "rowid")))
        for row in self.db.fetchFromTable("BlockDefinition", where = "parent_type = {}".format(ParentType.DECLARATION), orderBy = "rowid"):
            parent = Parent(row['parent_type'], row['parent_id'])
            res = BlockDefinition(self.db, row['id'], parent, row['tag'])
            print(list(res.typename))
            print(list(res.member))
        return self.db.fetchFromTable("Declaration", orderBy = "rowid")


FNAME = r'../examples/ASAP2_Demo_V161_ifdata_section.a2l'

def main():
    pa = aml.ParserWrapper('aml', 'amlFile')

    #db = Database("asap.sq3")
    db = Database()

    #tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\cr6eus.aml")
    #tree = pa.parseFromFile(r"c:\projekte\csProjects\pySART\pySART\fibex\CANape_Module_200.aml")
    #tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\crmin1.aml")

    tree = pa.parseFromFile(r"C:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.aml")

    #tree = pa.parseFromFile(r"c:/projekte/csProjects/XCP/pyxcp/aml/XCPonUSB.aml", encoding = "latin-1")
    #"/c/projekte/csProjects/XCP/pyxcp/aml/ifdata_usb.a2l"

    print("Finished ANTLR parsing.")
    #pprint(tree.value, indent = 4)
    #ppp = ifdata.Parser(tree)
    #parser = ppp.build()

    builder = Builder(db)
    builder.traverseTree(tree.value)

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

