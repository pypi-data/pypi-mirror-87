#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Test pyA2L database interface.
"""

from unittest.mock import patch

import pytest

from pya2l import DB

from io import BytesIO

A2L_TEXT = b"""
ASAP2_VERSION 1 61
/begin PROJECT ASAP2_Example ""

  /begin HEADER "ASAP2 Example File"
    VERSION "V1.61"
    PROJECT_NO MCD_P12_08
  /end HEADER

  /begin MODULE Example ""
  /end MODULE
/end PROJECT
"""

@pytest.fixture(scope = "function")
def a2l_file():
    res = BytesIO(A2L_TEXT)
    return res

def test_import_file():
    with patch("open") as session:
        db = DB()
        session = db.import_a2l("my_test_file.a2l")
        print(session)



