#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import textwrap

PAGE = """Format of the description file  3.5.141 VIRTUAL_CHARACTERISTIC Prototype: /begin
 VIRTUAL_CHARACTERISTIC string Formula     (ident Characteristic)* /end VIRTUAL_
CHARACTERISTIC Parameters: string Formula Formula to be used for the calculation
 of the initial physical value of the characteristic from the physical value of
other characteristics. ident Characteristic Identifier of those adjustable objec
ts that are used for the calculation of this characteristic. Description: This k
eyword allows to define characteristics that are not deposited in the memory of
the control unit, but can be used to indirectly calibrate other characteristic v
alues in the control unit, if these are declared to be dependent on this charact
eristic. The introduction of virtual characteristic is therefore useful for savi
ng memory in the case the calibration with dependent characteristics is used. 1A
BBB_AREA Figure 7 VIRTUAL_CHARACTERISTIC For the initial value of the virtual ch
aracteristic must be derived from the values of other characteristics. The mecha
nism to implement this is the same as for dependent characteristics by a list of
 characteristics and a formula, e.g.  = asin(B). Also B might be virtual, i.e. i
ts value has to be derived from B_AREA. The following example makes clear how th
e calibration process takes place. When the virtual characteristic  is initializ
ed, the value of  is calculated from the value of B. Therefore BInt is read from
 the ECU and Bphys = BInt/100 is computed. Assuming the value BInt = 80, Bphys =
 0.8 and phys = asin(Bphys ) = 53.13. Since virtual characteristics are not in t
he memory of an ECU, Int and phys may coincide if the datatype for Int is chosen
 an float datatype and the conversion formula is the identity (one to one formul
a).  The references used in the virtual dependency formula are named X1, X2, X3,
 <96> . The reference X1 references the first parameter of the attached paramete
r list, X2 the second, X3 the third, <96>. If there is only one reference used i
t is allowed to use X instead of X1. 216 ASAM MCD-2MC Version 1.6"""

FOLLOWUP_PAGE = """ Format of the description file curve or map in the emulation memory and must be
 described by a special AXIS_PTS data record.  The reference to this record occu
rs with the keyword 'AXIS_PTS_REF'. STD_AXIS Standard axis ident  InputQuantity
Reference to the data record for description of the input quantity (see MEASUREM
ENT). If there is no input quantity assigned, parameter 'InputQuantity' should b
e set to "NO_INPUT_QUANTITY" (measurement and calibration systems must be capabl
e to treat this case). ident  Conversion Reference to the relevant record of the
 description of the conversion method (see COMPU_METHOD). If there is no convers
ion method, as in the case of CURVE_AXIS, the parameter ‚Conversion™ should be s
et to ﬁNO_COMPU_METHOD" (measurement and calibration systems must be able to han
dle this case). uint  MaxAxisPoints Maximum number of axis points Note:  The mea
surement and calibration system can change the dimensions of a characteristic (i
ncrease or decrease the number of axis points).  The number of axis points may n
ot be increased at random as the address range reserved for each characteristic
in the ECU program by the measurement and calibration system cannot be changed.
float  LowerLimit Plausible range of axis point values, lower limit float  Upper
Limit Plausible range of axis point values, upper limit Note: Depending on the t
ype of conversion, the limit values are interpreted as physical or internal valu
es.  For conversions of type COMPU_VTAB and COMPU_VTAB_RANGE, the limit values a
re interpreted as internal values. For all other conversion types, the limit val
ues are interpreted as physical values. Optional parameters: -> ANNOTATION Set o
f notes (represented as multi-line ASCII description texts) which are related. C
an serve e.g. as application note. When a COM_AXIS is referenced it is sufficien
t to place the ANNOTATION with its AXIS_PTS in order to avoid redundant informat
ion. -> AXIS_PTS_REF Reference to the AXIS_PTS record for description of the axi
s points distribution. -> BYTE_ORDER Where the standard value does not apply thi
s parameter can be used to specify the byte order (Intel format, Motorola format
) of the axis point value. -> CURVE_AXIS_REF When the axis type is CURVE_AXIS, t
his keyword must be used to specify the CURVE CHARACTERISTIC that is used to nor
malize or scale this axis. ASAM MCD-2MC Version 1.6 45 """

FP0 = """ Format of the description file 3.5.4 ADDR_EPK Prototype:  ADDR_EPK  ulong Address Parameters:
ulong  Address Address of the EPROM identifier Description: Address of the EPROM identifier Example: ADDR_EPK 0x145678  ASAM MCD-2MC Version 1.6 31 
"""

FIRST_PAGE_FRAMING = re.compile(r"""^\s*Format\sof\sthe\sdescription\sfile\s+(?:\d\.\d\.\d+)\s+?
(?P<content>.*)\s*
(?P<page_num_even>\d+)?\s+ASAM\sMCD\-2MC\sVersion\s(?:\d.\d+)\s+(?P<page_num_odd>\d+)?\s*
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)

match = FIRST_PAGE_FRAMING.match(FP0)
print(match)

FOLLOWUP_PAGE_FRAMING = re.compile(r"""^\s*Format\sof\sthe\sdescription\sfile\s*
(?P<content>.*)\s*
(?P<page_num_even>\d+)?\s+ASAM\sMCD\-2MC\sVersion\s(?:\d.\d+)\s?(?P<page_num_odd>\d+)?\s*
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)


CONTENT = re.compile(r"""(?P<tag>.*)\s+
Prototype:(?P<prototype>.*?)
Parameters:(?P<parameters>.*?)
(?:Optional Parameters:(?P<options>.*?))?
Description:(?P<description>.*)
(?:Example:(?P<example>.*?))?
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)

match = FIRST_PAGE_FRAMING.search(PAGE)
content = match.group("content")

match = CONTENT.search(content)
print(match.groupdict())
txt = '\n'.join(textwrap.wrap(''.join(match.group("content").splitlines())))

# I can't change the object model, otherwise the resulting API would be useless for
# people knowing the specification.
