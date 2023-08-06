

from math import floor

import pytest
from sqlalchemy import sql
from sqlalchemy import select

from pya2l import model
#from pya2l.model import mixins
from pya2l import math

from scipy import interpolate

import numpy as np

debug = False

db = model.A2LDatabase(filename = ":memory:", debug = debug)
session = db.session

axisDescr = model.AxisDescr(
    attribute = "CURVE_AXIS",
    inputQuantity = "NO_INPUT_QUANTITY",
    conversion = "NO_COMPU_METHOD",
    maxAxisPoints = 14,
    lowerLimit = 0.0,
    upperLimit = 5800.0,
    read_only = False,
    )
session.add(axisDescr)
session.commit()

print(axisDescr)
axisDescr.check()

X_NORM = (
    (0.0,       2.0),
    (200.0,     2.7),
    (400.0,     3.0),
    (1000.0,    4.2),
    (5700,      4.9),
)

Y_NORM = (
    (0.0,       0.5),
    (50.0,      1.0),
    (70.0,      2.4),
    (100.0,     4.2),
)

Z_MAP = (
    (3.4, 4.5, 2.1, 5.4, 1.2, 3.4, 4.4),
    (2.3, 1.2, 1.2, 5.6, 3.2, 2.1, 7.8),
    (3.2, 1.5, 3.2, 2.2, 1.6, 1.7, 1.7),
    (2.1, 0.4, 1.0, 1.5, 1.8, 3.2, 1.5),
    (1.1, 4.3, 2.1, 4.6, 1.2, 1.4, 3.2),
    (1.2, 5.3, 3.2, 3.5, 2.1, 1.4, 4.2),
)

xn = np.array(X_NORM)
yn = np.array(Y_NORM)
zm = np.array(Z_MAP)

####
#### 11 Appendix C: Using Reference Curves as Normalization Axes for Maps
####
ip0 = math.Interpolate1D(xs = xn[:, 0], ys = xn[:, 1])
x_new = ip0(850.0)
print("x_new", x_new)

ip1 = math.Interpolate1D(xs = yn[:, 0], ys = yn[:, 1])
y_new = ip1(60.0)
print("y_new", y_new)

x_size, y_size = zm.shape
ip = interpolate.RegularGridInterpolator((np.arange(x_size), np.arange(y_size)), zm)
print("RESULT:", ip((1.7,3.9)))
####
####
####

stmt = select([model.AxisDescr])
for row in session.execute(stmt):
    print(row)

import bisect

Xs = (-3, -1, 0, 2, 4, 5, 6, 7, 8, 9, 10, 13)
Ys = (98, 99, 100, 102, 104, 105, 106, 107, 108, 109, 110, 111)

print("CS", bisect.bisect_right(Xs, 5.23423504) - 1)

#print(axisDescr.metadat