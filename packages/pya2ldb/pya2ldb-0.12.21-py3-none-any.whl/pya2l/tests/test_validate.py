#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

import pya2l.model as model
from pya2l.a2l_listener import ParserWrapper, A2LListener
from pya2l.api.inspect import Measurement
from pya2l.validate import Validator


def test_measurement_basic():
    parser = ParserWrapper('a2l', 'measurement', A2LListener, debug = False)
    DATA = """
    /begin MEASUREMENT
        N /* name */
        "Engine speed" /* long identifier */
        UWORD /* datatype */
        NO_COMPU_METHOD /* conversion */
        2 /* resolution */
        2.5 /* accuracy */
        120.0 /* lower limit */
        8400.0 /* upper limit */
    /end MEASUREMENT
    """
    session = parser.parseFromString(DATA)
    meas = Measurement(session, "N")


def test_compus_no_duplicates():
    parser = ParserWrapper('a2l', 'module', A2LListener, debug = False)
    DATA = """
    /begin MODULE testModule ""
        /begin COMPU_VTAB TT /* name */ "engine status conversion"
            TAB_VERB /* convers_type */
            4 /* number_value_pairs */
            0 "engine off" /* value pairs */
            1 "idling"
            2 "partial load"
            3 "full load"
        /end COMPU_VTAB
        /begin COMPU_TAB TT /* name */
            "conversion table for oil temperatures"
            TAB_NOINTP  /* convers_type */
            7           /* number_value_pairs */
            1 4.3 2 4.7 3 5.8 4 14.2 5 16.8 6 17.2 7 19.4 /* value pairs */
            DEFAULT_VALUE_NUMERIC 99.0
        /end COMPU_TAB
        /begin COMPU_VTAB_RANGE TT /* name */
            "engine status conversion"
            5
            0   0   "ONE"
            1   2   "first_section"
            3   3   "THIRD"
            4   5   "second_section"
            6   500 "usual_case"
            DEFAULT_VALUE "Value_out_of_Range"
        /end COMPU_VTAB_RANGE
    /end MODULE
    """
    session = parser.parseFromString(DATA)
    val = Validator(session)
    val()

