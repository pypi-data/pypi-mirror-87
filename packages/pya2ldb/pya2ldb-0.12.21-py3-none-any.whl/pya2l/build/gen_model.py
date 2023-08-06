#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__="""
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2020 by Christoph Schueler <github.com/Christoph2,
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

import pya2l.classes as classes
from pya2l.build import parse_classes
from pya2l import templates

HEADER = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__="""
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2020 by Christoph Schueler <github.com/Christoph2,
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

import datetime
from functools import partial
import mmap
import re
import sqlite3

from sqlalchemy import (MetaData, schema, types, orm, event,
    create_engine, Column, ForeignKey, ForeignKeyConstraint, func,
    PassiveDefault, UniqueConstraint, CheckConstraint
)
from sqlalchemy.ext.declarative import declared_attr, as_declarative
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import relationship, backref
from sqlalchemy.engine import Engine
from sqlalchemy.sql import exists

from pya2l.utils import SingletonBase
from pya2l.model.mixins import CompareByPositionMixIn, AxisDescrMixIn

DB_EXTENSION    = "a2ldb"

CURRENT_SCHEMA_VERSION = 10

CACHE_SIZE      = 4 # MB
PAGE_SIZE       = mmap.PAGESIZE


class MULTIPLE(SingletonBase): pass
class Uint(SingletonBase): pass
class Int(SingletonBase): pass
class Ulong(SingletonBase): pass
class Long(SingletonBase): pass
class Float(SingletonBase): pass
class String(SingletonBase): pass
class Enum(SingletonBase): pass
class Ident(SingletonBase): pass

class Datatype(SingletonBase):
    enum_values = ('UBYTE', 'SBYTE', 'UWORD', 'SWORD', 'ULONG', 'SLONG',
        'A_UINT64', 'A_INT64', 'FLOAT32_IEEE' ,'FLOAT64_IEEE'
    )

class Datasize(SingletonBase):
    enum_values = ('BYTE', 'WORD', 'LONG')

class Addrtype(SingletonBase):
    enum_values = ('PBYTE', 'PWORD', 'PLONG', 'DIRECT')

class Byteorder(SingletonBase):
    enum_values = ('LITTLE_ENDIAN', 'BIG_ENDIAN', 'MSB_LAST', 'MSB_FIRST')

class Indexorder(SingletonBase):
    enum_values = ('INDEX_INCR', 'INDEX_DECR')

class Parameter(object):
    """
    """
    def __init__(self, name, type_, multiple):
        self._name = name
        self._type = type_
        self._multiple = multiple

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def multiple(self):
        return self._multiple

    def __repr__(self):
        return "{}('{}' {} {})".format(self.__class__.__name__, self.name, self.type, "MULTIPLE" if self.multiple else "")

    __str__ = __repr__


class Element(object):
    """
    """
    def __init__(self, name, keyword_name, multiple):
        self._name = name
        self._keyword_name = keyword_name
        self._multiple = multiple

    @property
    def name(self):
        return self._name

    @property
    def keyword_name(self):
        return self._keyword_name

    @property
    def multiple(self):
        return self._multiple

    def __repr__(self):
        return "{}('{}' {} {})".format(self.__class__.__name__, self.name, self.keyword_name, "MULTIPLE" if self.multiple else "")

    __str__ = __repr__


def calculateCacheSize(value):
    return -(value // PAGE_SIZE)

REGEXER_CACHE = {}

def regexer(value, expr):
    if not REGEXER_CACHE.get(expr):
        REGEXER_CACHE[expr] = re.compile(expr, re.UNICODE)
    re_expr = REGEXER_CACHE[expr]
    return re_expr.match(value) is not None

@event.listens_for(Engine, "connect")
def set_sqlite3_pragmas(dbapi_connection, connection_record):
    dbapi_connection.create_function("REGEXP", 2, regexer)
    cursor = dbapi_connection.cursor()
    #cursor.execute("PRAGMA jornal_mode=WAL")
    cursor.execute("PRAGMA FOREIGN_KEYS=ON")
    cursor.execute("PRAGMA PAGE_SIZE={}".format(PAGE_SIZE))
    cursor.execute("PRAGMA CACHE_SIZE={}".format(calculateCacheSize(CACHE_SIZE * 1024 * 1024)))
    cursor.execute("PRAGMA SYNCHRONOUS=OFF") # FULL
    cursor.execute("PRAGMA LOCKING_MODE=EXCLUSIVE") # NORMAL
    cursor.execute("PRAGMA TEMP_STORE=MEMORY")  # FILE
    cursor.close()

@as_declarative()
class Base(object):

    rid = Column("rid", types.Integer, primary_key = True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        columns = [c.name for c in self.__class__.__table__.c]
        result = []
        for name, value in [(n, getattr(self, n)) for n in columns if not n.startswith("_")]:
            if isinstance(value, str):
                result.append("{} = '{}'".format(name, value))
            else:
                result.append("{} = {}".format(name, value))
        return "{}({})".format(self.__class__.__name__, ", ".join(result))

def StdFloat(default = 0.0):
    return Column(types.Float, default = default, nullable = False)

def StdShort(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (-32768, 32767)')
    )

def StdUShort(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (0, 65535)')
    )

def StdLong(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (-2147483648, 2147483647)')
    )

def StdULong(default = 0, primary_key = False, unique = False):
    return Column(types.Integer, default = default, nullable = False,
        primary_key = primary_key, unique = unique,
        #CheckClause('BETWEEN (0, 4294967295)')
    )

def StdString(default = 0, primary_key = False, unique = False):
    return Column(types.VARCHAR(256), default = default, nullable = False,
        primary_key = primary_key, unique = unique,
    )

def StdIdent(default = 0, primary_key = False, unique = False):
    return Column(types.VARCHAR(1025), default = default, nullable = False,
        primary_key = primary_key, unique = unique,
    )


class DefCharacteristicIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "def_characteristic_identifiers"

    dci_rid = Column(types.Integer, ForeignKey("def_characteristic.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class OutMeasurementIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "out_measurement_identifiers"

    om_rid = Column(types.Integer, ForeignKey("out_measurement.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class InMeasurementIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "in_measurement_identifiers"

    im_rid = Column(types.Integer, ForeignKey("in_measurement.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class LocMeasurementIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "loc_measurement_identifiers"

    lm_rid = Column(types.Integer, ForeignKey("loc_measurement.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class RefMeasurementIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "ref_measurement_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("ref_measurement.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class FrameMeasurementIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "frame_measurement_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("frame_measurement.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class SubGroupIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "sub_group_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("sub_group.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class SubFunctionIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "sub_function_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("sub_function.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class RefGroupIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "ref_group_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("ref_group.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class MapListIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "map_list_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("map_list.rid"))
    name = StdIdent()
    position = StdLong()

    def __init__(self, name):
        self.name = name

class VarCharacteristicIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "var_characteristic_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("var_characteristic.rid"))
    criterionName = StdIdent()
    position = StdLong()

    def __init__(self, criterionName):
        self.criterionName = criterionName

class VarCriterionIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "var_criterion_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("var_criterion.rid"))
    value = StdIdent()
    position = StdLong()

    def __init__(self, value):
        self.value = value

class FunctionListIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "function_list_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("function_list.rid"))
    name = StdIdent()
    position = StdLong()

    def __init__(self, name):
        self.name = name

class RefCharacteristicIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "ref_characteristic_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("ref_characteristic.rid"))
    identifier = StdIdent()
    position = StdLong()

    def __init__(self, identifier):
        self.identifier = identifier

class DependentCharacteristicIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "dependent_characteristic_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("dependent_characteristic.rid"))
    characteristic = StdIdent()
    position = StdLong()

    def __init__(self, characteristic):
        self.characteristic = characteristic

class VirtualCharacteristicIdentifiers(Base, CompareByPositionMixIn):

    __tablename__ = "virtual_characteristic_identifiers"

    rm_rid = Column(types.Integer, ForeignKey("virtual_characteristic.rid"))
    characteristic = StdIdent()
    position = StdLong()

    def __init__(self, characteristic):
        self.characteristic = characteristic


class CompuTabPair(Base, CompareByPositionMixIn):

    __tablename__ = "compu_tab_pair"

    ct_rid = Column(types.Integer, ForeignKey("compu_tab.rid"))
    position = StdLong()

    inVal = StdFloat()
    outVal = StdFloat()

class CompuVtabPair(Base, CompareByPositionMixIn):

    __tablename__ = "compu_vtab_pair"

    ct_rid = Column(types.Integer, ForeignKey("compu_vtab.rid"))
    position = StdLong()

    inVal = StdFloat()
    outVal = StdString()

class CompuVtabRangeTriple(Base, CompareByPositionMixIn):

    __tablename__ = "compu_vtab_range_triple"

    ct_rid = Column(types.Integer, ForeignKey("compu_vtab_range.rid"))
    position = StdLong()

    inValMin = StdFloat()
    inValMax = StdFloat()
    outVal   = StdString()

class CalHandles(Base, CompareByPositionMixIn):

    __tablename__ = "calhandles"

    ch_rid = Column(types.Integer, ForeignKey("calibration_handle.rid"))
    handle = StdLong()
    position = StdLong()

    def __init__(self, handle):
        self.handle = handle

class VirtualMeasuringChannels(Base, CompareByPositionMixIn):

    __tablename__ = "virtual_measuring_channel"

    vmc_rid = Column(types.Integer, ForeignKey("virtual.rid"))
    measuringChannel = StdIdent()
    position = StdLong()

    def __init__(self, measuringChannel):
        self.measuringChannel = measuringChannel

class FixAxisParListValues(Base, CompareByPositionMixIn):

    __tablename__ = "fix_axis_par_list_value"

    faplv_rid = Column(types.Integer, ForeignKey("fix_axis_par_list.rid"))
    axisPts_Value = StdFloat()
    position = StdLong()

    def __init__(self, axisPts_Value):
        self.axisPts_Value = axisPts_Value


class VarAddressValues(Base, CompareByPositionMixIn):

    __tablename__ = "var_address_values"

    va_rid = Column(types.Integer, ForeignKey("var_address.rid"))
    address = StdULong()
    position = StdLong()

    def __init__(self, address):
        self.address = address

class AnnotationTextValues(Base, CompareByPositionMixIn):

    __tablename__ = "annotation_text_values"

    at_rid = Column(types.Integer, ForeignKey("annotation_text.rid"))
    text = StdString()
    position = StdLong()

    def __init__(self, text):
        self.text = text

class FunctionListValues(Base, CompareByPositionMixIn):

    __tablename__ = "function_list_values"

    flv_rid = Column(types.Integer, ForeignKey("function_list.rid"))
    name = StdString()
    position = StdLong()

    def __init__(self, name):
        self.name = name


class VarForbiddedCombPair(Base, CompareByPositionMixIn):

    __tablename__ = "var_forbidden_comb_pair"

    vfc_rid = Column(types.Integer, ForeignKey("var_forbidden_comb.rid"))
    criterionName = StdIdent()
    criterionValue = StdIdent()
    position = StdLong()


class MetaData(Base):

    schema_version = StdShort()
    created = Column(types.DateTime, default = datetime.datetime.now)
'''

FOOTER = '''
class A2LDatabase(object):

    def __init__(self, filename, debug = False, logLevel = 'INFO'):
        if filename == ':memory:':
            self.dbname = ""
        else:
            if not filename.lower().endswith(DB_EXTENSION):
               self.dbname = "{}.{}".format(filename, DB_EXTENSION)
            else:
               self.dbname = filename
            ##try:
            ##    os.unlink(self.dbname)
            ##except:
            ##    pass
        self._engine = create_engine("sqlite:///{}".format(self.dbname), echo = debug,
            connect_args={'detect_types': sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES},
        native_datetime = True)

        self._session = orm.Session(self._engine, autoflush = False, autocommit = False)
        self._metadata = Base.metadata
        #loadInitialData(Node)
        Base.metadata.create_all(self.engine)
        meta = MetaData(schema_version = CURRENT_SCHEMA_VERSION)
        self.session.add(meta)
        self.session.flush()
        self.session.commit()
        self._closed = False

    def __del__(self):
        pass
        #if not self._closed:
        #    self.close()

    def close(self):
        """

        """
        self.session.close()
        self.engine.dispose()
        self._closed = True

    @property
    def engine(self):
        return self._engine

    @property
    def metadata(self):
        return self._metadata

    @property
    def session(self):
        return self._session

    def begin_transaction(self):
        """
        """

    def commit_transaction(self):
        """
        """

    def rollback_transaction(self):
        """
        """

KEYWORD_MAP = {
    "A2ML" : A2ml,
    "A2ML_VERSION" : A2mlVersion,
    "ADDR_EPK" : AddrEpk,
    "ALIGNMENT_BYTE" : AlignmentByte,
    "ALIGNMENT_FLOAT32_IEEE" : AlignmentFloat32Ieee,
    "ALIGNMENT_FLOAT64_IEEE" : AlignmentFloat64Ieee,
    "ALIGNMENT_INT64" : AlignmentInt64,
    "ALIGNMENT_LONG" : AlignmentLong,
    "ALIGNMENT_WORD" : AlignmentWord,
    "ANNOTATION" : Annotation,
    "ANNOTATION_LABEL" : AnnotationLabel,
    "ANNOTATION_ORIGIN" : AnnotationOrigin,
    "ANNOTATION_TEXT" : AnnotationText,
    "ARRAY_SIZE" : ArraySize,
    "ASAP2_VERSION" : Asap2Version,
    "AXIS_DESCR" : AxisDescr,
    "AXIS_PTS" : AxisPts,
    "AXIS_PTS_REF" : AxisPtsRef,
    "AXIS_PTS_X" : AxisPtsX,
    "AXIS_PTS_Y" : AxisPtsY,
    "AXIS_PTS_Z" : AxisPtsZ,
    "AXIS_PTS_4" : AxisPts4,
    "AXIS_PTS_5" : AxisPts5,
    "AXIS_RESCALE_X" : AxisRescaleX,
    "AXIS_RESCALE_Y" : AxisRescaleY,
    "AXIS_RESCALE_Z" : AxisRescaleZ,
    "AXIS_RESCALE_4" : AxisRescale4,
    "AXIS_RESCALE_5" : AxisRescale5,
    "BIT_MASK" : BitMask,
    "BIT_OPERATION" : BitOperation,
    "BYTE_ORDER" : ByteOrder,
    "CALIBRATION_ACCESS" : CalibrationAccess,
    "CALIBRATION_HANDLE" : CalibrationHandle,
    "CALIBRATION_HANDLE_TEXT" : CalibrationHandleText,
    "CALIBRATION_METHOD" : CalibrationMethod,
    "CHARACTERISTIC" : Characteristic,
    "COEFFS" : Coeffs,
    "COEFFS_LINEAR" : CoeffsLinear,
    "COMPARISON_QUANTITY" : ComparisonQuantity,
    "COMPU_METHOD" : CompuMethod,
    "COMPU_TAB" : CompuTab,
    "COMPU_TAB_REF" : CompuTabRef,
    "COMPU_VTAB" : CompuVtab,
    "COMPU_VTAB_RANGE" : CompuVtabRange,
    "CPU_TYPE" : CpuType,
    "CURVE_AXIS_REF" : CurveAxisRef,
    "CUSTOMER" : Customer,
    "CUSTOMER_NO" : CustomerNo,
    "DATA_SIZE" : DataSize,
    "DEF_CHARACTERISTIC" : DefCharacteristic,
    "DEFAULT_VALUE" : DefaultValue,
    "DEFAULT_VALUE_NUMERIC" : DefaultValueNumeric,
    "DEPENDENT_CHARACTERISTIC" : DependentCharacteristic,
    "DEPOSIT" : Deposit,
    "DISCRETE" : Discrete,
    "DISPLAY_IDENTIFIER" : DisplayIdentifier,
    "DIST_OP_X" : DistOpX,
    "DIST_OP_Y" : DistOpY,
    "DIST_OP_Z" : DistOpZ,
    "DIST_OP_4" : DistOp4,
    "DIST_OP_5" : DistOp5,
    "ECU" : Ecu,
    "ECU_ADDRESS" : EcuAddress,
    "ECU_ADDRESS_EXTENSION" : EcuAddressExtension,
    "ECU_CALIBRATION_OFFSET" : EcuCalibrationOffset,
    "EPK" : Epk,
    "ERROR_MASK" : ErrorMask,
    "EXTENDED_LIMITS" : ExtendedLimits,
    "FIX_AXIS_PAR" : FixAxisPar,
    "FIX_AXIS_PAR_DIST" : FixAxisParDist,
    "FIX_AXIS_PAR_LIST" : FixAxisParList,
    "FIX_NO_AXIS_PTS_X" : FixNoAxisPtsX,
    "FIX_NO_AXIS_PTS_Y" : FixNoAxisPtsY,
    "FIX_NO_AXIS_PTS_Z" : FixNoAxisPtsZ,
    "FIX_NO_AXIS_PTS_4" : FixNoAxisPts4,
    "FIX_NO_AXIS_PTS_5" : FixNoAxisPts5,
    "FNC_VALUES" : FncValues,
    "FORMAT" : Format,
    "FORMULA" : Formula,
    "FORMULA_INV" : FormulaInv,
    "FRAME" : Frame,
    "FRAME_MEASUREMENT" : FrameMeasurement,
    "FUNCTION" : Function,
    "FUNCTION_LIST" : FunctionList,
    "FUNCTION_VERSION" : FunctionVersion,
    "GROUP" : Group,
    "GUARD_RAILS" : GuardRails,
    "HEADER" : Header,
    "IDENTIFICATION" : Identification,
    "IF_DATA" : IfData,
    "IN_MEASUREMENT" : InMeasurement,
    "LAYOUT" : Layout,
    "LEFT_SHIFT" : LeftShift,
    "LOC_MEASUREMENT" : LocMeasurement,
    "MAP_LIST" : MapList,
    "MATRIX_DIM" : MatrixDim,
    "MAX_GRAD" : MaxGrad,
    "MAX_REFRESH" : MaxRefresh,
    "MEASUREMENT" : Measurement,
    "MEMORY_LAYOUT" : MemoryLayout,
    "MEMORY_SEGMENT" : MemorySegment,
    "MOD_COMMON" : ModCommon,
    "MOD_PAR" : ModPar,
    "MODULE" : Module,
    "MONOTONY" : Monotony,
    "NO_AXIS_PTS_X" : NoAxisPtsX,
    "NO_AXIS_PTS_Y" : NoAxisPtsY,
    "NO_AXIS_PTS_Z" : NoAxisPtsZ,
    "NO_AXIS_PTS_4" : NoAxisPts4,
    "NO_AXIS_PTS_5" : NoAxisPts5,
    "NO_OF_INTERFACES" : NoOfInterfaces,
    "NO_RESCALE_X" : NoRescaleX,
    "NO_RESCALE_Y" : NoRescaleY,
    "NO_RESCALE_Z" : NoRescaleZ,
    "NO_RESCALE_4" : NoRescale4,
    "NO_RESCALE_5" : NoRescale5,
    "NUMBER" : Number,
    "OFFSET_X" : OffsetX,
    "OFFSET_Y" : OffsetY,
    "OFFSET_Z" : OffsetZ,
    "OFFSET_4" : Offset4,
    "OFFSET_5" : Offset5,
    "OUT_MEASUREMENT" : OutMeasurement,
    "PHONE_NO" : PhoneNo,
    "PHYS_UNIT" : PhysUnit,
    "PROJECT" : Project,
    "PROJECT_NO" : ProjectNo,
    "READ_ONLY" : ReadOnly,
    "READ_WRITE" : ReadWrite,
    "RECORD_LAYOUT" : RecordLayout,
    "REF_CHARACTERISTIC" : RefCharacteristic,
    "REF_GROUP" : RefGroup,
    "REF_MEASUREMENT" : RefMeasurement,
    "REF_MEMORY_SEGMENT" : RefMemorySegment,
    "REF_UNIT" : RefUnit,
    "RESERVED" : Reserved,
    "RIGHT_SHIFT" : RightShift,
    "RIP_ADDR_W" : RipAddrW,
    "RIP_ADDR_X" : RipAddrX,
    "RIP_ADDR_Y" : RipAddrY,
    "RIP_ADDR_Z" : RipAddrZ,
    "RIP_ADDR_4" : RipAddr4,
    "RIP_ADDR_5" : RipAddr5,
    "ROOT" : Root,
    "SHIFT_OP_X" : ShiftOpX,
    "SHIFT_OP_Y" : ShiftOpY,
    "SHIFT_OP_Z" : ShiftOpZ,
    "SHIFT_OP_4" : ShiftOp4,
    "SHIFT_OP_5" : ShiftOp5,
    "SIGN_EXTEND" : SignExtend,
    "SI_EXPONENTS" : SiExponents,
    "SRC_ADDR_X" : SrcAddrX,
    "SRC_ADDR_Y" : SrcAddrY,
    "SRC_ADDR_Z" : SrcAddrZ,
    "SRC_ADDR_4" : SrcAddr4,
    "SRC_ADDR_5" : SrcAddr5,
    "STATIC_RECORD_LAYOUT" : StaticRecordLayout,
    "STATUS_STRING_REF" : StatusStringRef,
    "STEP_SIZE" : StepSize,
    "SUB_FUNCTION" : SubFunction,
    "SUB_GROUP" : SubGroup,
    "SUPPLIER" : Supplier,
    "SYMBOL_LINK" : SymbolLink,
    "SYSTEM_CONSTANT" : SystemConstant,
    "S_REC_LAYOUT" : SRecLayout,
    "UNIT" : Unit,
    "UNIT_CONVERSION" : UnitConversion,
    "USER" : User,
    "USER_RIGHTS" : UserRights,
    "VAR_ADDRESS" : VarAddress,
    "VAR_CHARACTERISTIC" : VarCharacteristic,
    "VAR_CRITERION" : VarCriterion,
    "VAR_FORBIDDEN_COMB" : VarForbiddenComb,
    "VAR_MEASUREMENT" : VarMeasurement,
    "VAR_NAMING" : VarNaming,
    "VAR_SELECTION_CHARACTERISTIC" : VarSelectionCharacteristic,
    "VAR_SEPARATOR" : VarSeparator,
    "VARIANT_CODING" : VariantCoding,
    "VERSION" : Version,
    "VIRTUAL" : Virtual,
    "VIRTUAL_CHARACTERISTIC" : VirtualCharacteristic,
}

def instanceFactory(className, **kws):
    """Create an instance of a given class.
    """
    klass = KEYWORD_MAP.get(className)
    inst = klass()
    inst.attrs = []
    for k, v in kws.items():
        k = "{}{}".format(k[0].lower(), k[1 : ])
        setattr(inst, k, v.value)
        inst.attrs.append(k)
    inst.children = []
    return inst
'''

parser = parse_classes.ClassParser()
parser.run()

print(templates.doTemplateFromText(HEADER, {}, 0))

#for item in [x[0] for x in parser.polymorphic_classes]:
#    match = TYPE_NAME.match(str(item))
#    tag = match.group(1)
#    print(structure(tag, utils, 1))

#for child in classes.RootElement.children:
#    print(structure(child, utils, 1))

def map_type_to_sqa(attr):
    TYPES = {
        classes.Uint:   "StdUShort()", # TODO: check!!!
        classes.Int:    "StdShort()", # TODO: check!!!
        classes.Ulong:  "StdULong()", # TODO: check!!!
        classes.Long:   "StdLong()", # TODO: check!!!
        classes.Float:  "StdFloat()",
        classes.String: "StdString()",
        classes.Ident:  "StdIdent()",
        classes.Enum:   "StdString()",
        classes.Datatype: "StdIdent()",   # enum datatype
        classes.Indexorder: "StdIdent()", # enum indexorder
        classes.Addrtype: "StdIdent()",   # enum addrtype
        classes.Datasize: "StdIdent()",   # enum datasize
        classes.Byteorder: "StdString()",
    }
    if attr in TYPES:
        mappedType = TYPES[attr]
        return mappedType
    else:
        return None

def map_type_to_a2l(attr):
    TYPES = {
        classes.Uint:   "Uint",
        classes.Int:    "Int",
        classes.Ulong:  "Ulong",
        classes.Long:   "Long",
        classes.Float:  "Float",
        classes.String: "String",
        classes.Ident:  "Ident",
        classes.Enum:   "Enum",
        classes.Datatype: "Datatype",
        classes.Indexorder: "Indexorder",
        classes.Addrtype: "Addrtype",
        classes.Datasize: "Datasize",
        classes.Byteorder: "Byteorder",
    }
    if attr in TYPES:
        mappedType = TYPES[attr]
        return mappedType
    else:
        return None
##
##
##

##
##
##
REQUIRED_PARAMETERS = '''<%

%>
%if required_parameters:
    __required_parameters__ = (
%for param in required_parameters:
        Parameter("${utils.lower_first(param[1])}", ${utils.map_type_to_a2l(param[0])}, ${True if len(param) == 3 and param[2] == utils.classes.MULTIPLE else False}),
%endfor
    )
%else:
    __required_parameters__ = ( )
%endif
'''

OPTIONAL_ELEMENTS = '''<%
optional_elements = []
for kl in utils.parser.references[klass]:
    optional_elements.append(kl)
%>
%if optional_elements:
    __optional_elements__ = (
%for elem in optional_elements:
        Element("${elem.camel_case_name()}", "${elem.class_name()}", ${True if elem.multiple else False}),
%endfor
    )
%else:
    __optional_elements__ = ( )
%endif
'''

ASSOCIATION_ITEM = '''<% klass = utils.parser.class_from_name(tag)
import pya2l.classes as classes
required_parameters = []
no_attrs = True if not item.attrs else False
%>
%if klass.multiple == True:
class ${klass.camel_case_name()}Association(Base):

    __tablename__ = "${klass.lower_name()}_association"

    position = StdLong()

    discriminator = Column(types.String)
    __mapper_args__ = {"polymorphic_on": discriminator}


class ${klass.camel_case_name()}(Base):
    """
    """
    _association_id = Column(types.Integer, ForeignKey("${klass.lower_name()}_association.rid"))
    association = relationship("${klass.camel_case_name()}Association", backref="${klass.lower_name()}", uselist = ${True if klass.multiple else False})
    parent = association_proxy("association", "parent")
%if klass.lower_name() == 'function_list':
    _name = relationship("FunctionListValues", backref = "parent", collection_class = ordering_list('position'))
    name = association_proxy("_name", "name")
%else:
%for attr in item.attrs:
<% required_parameters.append(attr) %>
%if utils.is_multiple_attribute(klass.lower_name(), utils.lower_first(attr[1])):
    %if klass.lower_name() == 'virtual_characteristic':
    _characteristic_id = relationship("VirtualCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    characteristic_id = association_proxy("_characteristic_id", "characteristic")
    %elif klass.lower_name() == 'frame_measurement':
    _identifier = relationship("FrameMeasurementIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'ref_characteristic':
    _identifier = relationship("RefCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %endif
%else:
    ${utils.lower_first(attr[1])} = ${utils.map_type_to_sqa(attr[0])}
%endif
%endfor
%endif
${utils.required_parameters(utils, required_parameters)}
${utils.optional_elements(utils, klass)}
%for fk in utils.parser.references[klass]:
%if fk not in utils.parser.polymorphic_classes_set:
    ${fk.assoc_name()} = relationship("${fk.camel_case_name()}", back_populates = "${klass.lower_name()}", uselist = ${True if fk.multiple else False})
%endif
%endfor
%if klass not in utils.parser.polymorphic_classes_set:
%for fk in utils.parser.referenced_by[klass]:
    _${fk.lower_name()}_rid = Column(types.Integer, ForeignKey("${fk.lower_name()}.rid"))
    ${fk.lower_name()} = relationship("${fk.camel_case_name()}", back_populates = "${klass.assoc_name()}")
%endfor
%endif
%for child in item.children:
%if not utils.parser.polymorphic(child):
${utils.line_item(child, utils, level)}
%endif
%endfor

class Has${klass.camel_case_plural_name()}(object):

    @declared_attr
    def _${klass.lower_name()}_association_id(cls):
        return Column(types.Integer, ForeignKey("${klass.lower_name()}_association.rid"))

    @declared_attr
    def ${klass.lower_name()}_association(cls):
        name = cls.__name__
        discriminator = name.lower()

        assoc_cls = type(
            "%s${klass.camel_case_name()}Association" % name, (${klass.camel_case_name()}Association,),
            dict(
                __tablename__ = None,
                __mapper_args__ = {"polymorphic_identity": discriminator},
            ),
        )

        cls.${klass.lower_name()} = association_proxy(
            "${klass.lower_name()}_association",
            "${klass.lower_name()}",
            creator = lambda ${klass.lower_name()}: assoc_cls(${klass.lower_name()} = ${klass.lower_name()}),
        )
        return relationship(
            assoc_cls, backref = backref("parent", uselist = False, collection_class = ordering_list('position'))
        )
%else:
%if no_attrs:
class ${klass.camel_case_name()}(object):
    pass

class Has${klass.camel_case_plural_name()}(object):

    @declared_attr
    def ${klass.lower_name()}(cls):
        return Column(types.Boolean, default = False)

%else:
class ${klass.camel_case_name()}(Base):
    """
    """
    ##rid = Column(types.Integer, primary_key = True)
    __tablename__ = "${klass.lower_name()}"

%if klass.lower_name() == 'function_list':
    _name = relationship("FunctionListValues", backref = "parent", collection_class = ordering_list('position'))
    name = association_proxy("_name", "name")
%elif klass.lower_name() == 'ref_characteristic':
    _identifier = relationship("RefCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
%else:
%for attr in item.attrs:
<% required_parameters.append(attr) %>\
    ${utils.lower_first(attr[1])} = ${utils.map_type_to_sqa(attr[0])}
%endfor
%endif
${utils.required_parameters(utils, required_parameters)}

class Has${klass.camel_case_plural_name()}(object):

    @declared_attr
    def ${klass.lower_name()}_id(cls):
        return Column(types.Integer,
            ForeignKey("${klass.lower_name()}.rid"),
            nullable = True
        )

    @declared_attr
    def ${klass.lower_name()}(cls):
        ##return relationship("${klass.camel_case_name()}", backref = "parent")
        return relationship("${klass.camel_case_name()}")
%endif
%endif
'''

LINE_ITEM = '''<% klass = utils.parser.class_from_name(tag) %>
<%
import pya2l.classes as classes
from pya2l.model.mixins import MIXIN_MAP
required_parameters = []
mixins = []
for child in item.children:
    if utils.parser.polymorphic(child):
        mixins.append(child)
mixins = ["Has{}".format(utils.parser.class_from_name(x).camel_case_plural_name()) for x in mixins]
if klass.class_name() in MIXIN_MAP:
    mixins.insert(0, "{}".format(MIXIN_MAP[klass.class_name()]))
mixins.insert(0, "Base")
%>
class ${utils.camel_case(tag, True)}(${", ".join(mixins)}):
    """
    """
    __tablename__ = "${klass.lower_name()}"
%if klass.lower_name() == 'calibration_handle':
    _handle = relationship("CalHandles", backref = "parent")
    handle = association_proxy("_handle", "handle")
%elif klass.lower_name() == 'virtual':
    _measuringChannel = relationship("VirtualMeasuringChannels", backref = "parent", collection_class = ordering_list('position'))
    measuringChannel = association_proxy("_measuringChannel", "measuringChannel")
%elif klass.lower_name() == 'fix_axis_par_list':
    _axisPts_Value = relationship("FixAxisParListValues", backref = "parent", collection_class = ordering_list('position'))
    axisPts_Value = association_proxy("_axisPts_Value", "axisPts_Value")
%elif klass.lower_name() == 'var_address_values':
    _address = relationship("VarAddressValues", backref = "parent", collection_class = ordering_list('position'))
    address = association_proxy("_address", "address")
%elif klass.lower_name() == 'annotation_text':
    _text = relationship("AnnotationTextValues", backref = "parent", collection_class = ordering_list('position'))
    text = association_proxy("_text", "text")
%else:
%for attr in item.attrs:
<% required_parameters.append(attr) %>
%if utils.is_multiple_attribute(klass.lower_name(), utils.lower_first(attr[1])):
    %if klass.lower_name() == 'def_characteristic':
    _identifier = relationship("DefCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'out_measurement':
    _identifier = relationship("OutMeasurementIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'in_measurement':
    _identifier = relationship("InMeasurementIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'frame_measurement':
    _identifier = relationship("FrameMeasurementIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'loc_measurement':
    _identifier = relationship("LocMeasurementIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'ref_measurement':
    _identifier = relationship("RefMeasurementIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'ref_group':
    _identifier = relationship("RefGroupIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'ref_characteristic':
    _identifier = relationship("RefCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'sub_group':
    _identifier = relationship("SubGroupIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'sub_function':
    _identifier = relationship("SubFunctionIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    identifier = association_proxy("_identifier", "identifier")
    %elif klass.lower_name() == 'dependent_characteristic':
    _characteristic_id = relationship("DependentCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    characteristic_id = association_proxy("_characteristic_id", "characteristic")
    %elif klass.lower_name() == 'virtual_characteristic':
    _characteristic_id = relationship("VirtualCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    characteristic_id = association_proxy("_characteristic_id", "characteristic")
    %elif klass.lower_name() == 'map_list':
    _name = relationship("MapListIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    name = association_proxy("_name", "name")
    %elif klass.lower_name() == 'function_list':
    _name = relationship("FunctionListIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    name = association_proxy("_name", "name")
    %elif klass.lower_name() == "var_characteristic":
    _criterionName = relationship("VarCharacteristicIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    criterionName = association_proxy("_criterionName", "criterionName")
    %elif klass.lower_name() == "var_criterion":
    _value = relationship("VarCriterionIdentifiers", backref = "parent", collection_class = ordering_list('position'))
    value = association_proxy("_value", "value")
    %elif klass.lower_name() == 'var_address':
    _address = relationship("VarAddressValues", backref = "parent", collection_class = ordering_list('position'))
    address = association_proxy("_address", "address")
    %endif
%else:
    ${utils.lower_first(attr[1])} = ${utils.map_type_to_sqa(attr[0])}
%endif
%endfor
%endif
${utils.required_parameters(utils, required_parameters)}
%if klass.lower_name() == 'compu_tab':
    pairs = relationship("CompuTabPair", backref = "parent", collection_class = ordering_list('position'))
%elif klass.lower_name() == 'compu_vtab':
    pairs = relationship("CompuVtabPair", backref = "parent", collection_class = ordering_list('position'))
%elif klass.lower_name() == 'compu_vtab_range':
    triples = relationship("CompuVtabRangeTriple", backref = "parent", collection_class = ordering_list('position'))
%elif klass.lower_name() == 'var_forbidden_comb':
    pairs = relationship("VarForbiddedCombPair", backref = "parent", collection_class = ordering_list('position'))
%endif
${utils.optional_elements(utils, klass)}
%for fk in utils.parser.references[klass]:
%if fk not in utils.parser.polymorphic_classes_set:
##    ${fk.assoc_name()} = relationship("${fk.camel_case_name()}", back_populates = "${klass.lower_name()}", uselist = ${True if fk.multiple else False})
    ${fk.lower_name()} = relationship("${fk.camel_case_name()}", back_populates = "${klass.lower_name()}", uselist = ${True if fk.multiple else False})
%endif
%endfor
%if klass not in utils.parser.polymorphic_classes_set:
%for fk in utils.parser.referenced_by[klass]:
    _${fk.lower_name()}_rid = Column(types.Integer, ForeignKey("${fk.lower_name()}.rid"))
    ##${fk.lower_name()} = relationship("${fk.camel_case_name()}", back_populates = "${klass.assoc_name()}", uselist = ${True if klass.multiple else False})
    ${fk.lower_name()} = relationship("${fk.camel_case_name()}", back_populates = "${klass.lower_name()}", uselist = ${True if klass.multiple else False})
%endfor
%endif
%for child in item.children:
%if not utils.parser.polymorphic(child):
${utils.line_item(child, utils, level)}
%endif
%endfor
'''

def camel_case(name, upper_first = False):
    splitty = [n.lower() for n in name.split('_')]
    result = []
    result.append(splitty[0])
    if len(splitty) > 1:
        for part in splitty[1 : ]:
            xxx = "{0}{1}".format(part[0].upper(), part[1: ])
            result.append(xxx)
    result = ''.join(result)
    if upper_first:
        result = "{}{}".format(result[0].upper(), result[1 : ])
    return result

def lower_first(value):
    return "{}{}".format(value[0].lower(), value[1 : ])

def line_item(name, utils, level = 1):
    item = classes.KEYWORD_MAP[name]
    namespace = {"item": item, "level": level, "tag": name, "utils": utils,
    }
    return templates.doTemplateFromText(LINE_ITEM, namespace, level * 4, formatExceptions = False)

def required_parameters(utils, required_parameters):
    namespace = {"utils": utils, "required_parameters": required_parameters}
    return templates.doTemplateFromText(REQUIRED_PARAMETERS, namespace, formatExceptions = False)

def optional_elements(utils, klass):
    namespace = {"utils": utils, "klass": klass}
    return templates.doTemplateFromText(OPTIONAL_ELEMENTS, namespace, formatExceptions = False)

def association_item(name, utils, level = 1):
    item = classes.KEYWORD_MAP[name]
    namespace = {"item": item, "level": level, "tag": name, "utils": utils,
    }
    return templates.doTemplateFromText(ASSOCIATION_ITEM, namespace, level * 4, formatExceptions = False)

def is_multiple_attribute(name, attr):
    KLASSES0 = (
        'def_characteristic',
        'in_measurement',
        'loc_measurement',
        'out_measurement',
        'frame_measurement',
        'ref_measurement',
        'ref_group',
        'ref_characteristic',
        'sub_group',
        'sub_function',
    )
    KLASSES1 = (
        'dependent_characteristic',
        'virtual_characteristic',
    )
    KLASSES2 = (
        "map_list",
        "function_list"
    )
    KLASSES3 = (
        "var_characteristic"
    )
    KLASSES4 = (
        "var_criterion"
    )
    KLASSES5 = (
        "var_address"
    )

    if (name in KLASSES0 and attr == "identifier") or (name in KLASSES1 and attr == "characteristic") \
        or (name in KLASSES2 and attr == "name") or (name in KLASSES3 and attr == "criterionName") \
        or (name in KLASSES4 and attr == "value") or (name in KLASSES5 and attr == "address"):
        return True

def has_multiple_identifiers(name):
    KLASSES = (
        'def_characteristic',
        'in_measurement',
        'loc_measurement',
        'out_measurement',
        'ref_measurement',
        'ref_group',
        'ref_characteristic',
        'sub_group'
    )
    return name in KLASSES

class Dummy(object): pass

utils = Dummy()
utils.classes = classes
utils.parser = parser
utils.line_item = line_item
utils.camel_case = camel_case
utils.map_type_to_sqa = map_type_to_sqa
utils.map_type_to_a2l = map_type_to_a2l
utils.lower_first = lower_first
utils.required_parameters = required_parameters
utils.optional_elements = optional_elements
utils.is_multiple_attribute = is_multiple_attribute
utils.has_multiple_identifiers = has_multiple_identifiers

#for item in [x[0] for x in parser.polymorphic_classes]:
#    for attr in item.attrs:
#        if 'Enum' in str(attr[0]):
#            print("{}::{}".format(item, attr))

for item in [x[0] for x in parser.polymorphic_classes]:
    match = parse_classes.TYPE_NAME.match(str(item))
    tag = match.group(1)
    print(association_item(tag, utils, level = 0))

for child in classes.RootElement.children:
    print(line_item(child, utils, level = 0))

print(templates.doTemplateFromText(FOOTER, {}, 0))


