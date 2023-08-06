#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
## xXx Vehicle Network Editor -- CAN Bus Edition.
## zZz A2L Architect.
## yYy Calibration Engineer Professional Starter Edition.
##

from operator import attrgetter, itemgetter
from decimal import Decimal as D
from pprint import pprint
import re

f0 = (1.9, 4.0) # 2.1x + 1.9
f1 = (3.3, 4.5) # 1.2x + 3.3

def fn0(x):
    return 0.018876828692779613 * x + 1.9

def fn1(x):
    return 1.2 * x + 3.3

print(fn0(0), fn0(100))

mids = (
    2566839038,
    2566768126,
    2566835966,
    2566835710,
    2566764542,
    2566764286,
    2566835198,
    2566834942,
    2565799678,
    2565406462,
)

print(mids)
print(sorted(mids))

"""
1 start bit to start a new frame
18 bits for the header
0 - 8 bytes of data
15 bit CRC
1 bit CRC delimiter
1 bit ACK slot
1 bit ACK delimiter
7 bit end of frame delimiter
3 bits must separate data frames. This is the interframe spacing 
"""

def camelCaseToUnder(name):
    return name[0].lower() + re.sub(r'([A-Z])', lambda m:"_" + m.group(0).lower(), name[1:])

print(camelCaseToUnder("camelCaseToUnder"))

def frameSize(nbytes, extended = False):
    nbits = (nbytes * 8)
    nbits += 1  # SOF
    nbits += 18 # Header / 11bit identifier.
    if extended:
        nbits += 20
    nbits += 16 # CRC
    nbits += 2  # ACK
    nbits += 7  # End of Frame
    nbits += 3  # Interframe spacing
    return nbits

MINIMUM_FRAME_SIZES = { # No stuff bits.
    (0, "11"): frameSize(0, False),
    (1, "11"): frameSize(1, False),
    (2, "11"): frameSize(2, False),
    (3, "11"): frameSize(3, False),
    (4, "11"): frameSize(4, False),
    (5, "11"): frameSize(5, False),
    (6, "11"): frameSize(6, False),
    (7, "11"): frameSize(7, False),
    (8, "11"): frameSize(8, False),
    (0, "29"): frameSize(0, True),
    (1, "29"): frameSize(1, True),
    (2, "29"): frameSize(2, True),
    (3, "29"): frameSize(3, True),
    (4, "29"): frameSize(4, True),
    (5, "29"): frameSize(5, True),
    (6, "29"): frameSize(6, True),
    (7, "29"): frameSize(7, True),
    (8, "29"): frameSize(8, True),    
}

#pprint(MINIMUM_FRAME_SIZES)

MAXIMUM_STUFF_BITS = {}
MAXIMUM_FRAME_SIZES = {}

for key, value in MINIMUM_FRAME_SIZES.items():
    nBits = int((value - 14) / 4)
    MAXIMUM_STUFF_BITS[key] = nBits
    MAXIMUM_FRAME_SIZES[key] = value + nBits


#pprint(MAXIMUM_STUFF_BITS)
#pprint(MAXIMUM_FRAME_SIZES)

BAUDRATES_AUTOMOTIVE = (
    #10.0,
    #20.0,
    33.3,
    50.0,

    83.3,
    100.0,
    125.0,
    250.0,
    500.0,
    #800.0,
    1000.0,
)

def maxFrameLength(dlc, ext = False):
    offset = 20 if ext else 0
    res = 8 * dlc + 47 + offset + int((34 + offset + 8 * dlc - 1) / 4)
    return res

"""
Theoretisches Maximum / Stuffbits:
----------------------------------
8s + 47 + ((34 + 8s - 1) / 4)

Worstcase Transmission-Time:
----------------------------

Ci = (8s + 47 + ((34 + 8s - 1) / 4)) * tbit
"""

"""
[4] K. Tindell, A. Burns, A. Wellings: Calculating CAN Message Response Times. Control Enginee-
ring Practice, Heft 8, 1995, S. 1163-1169
[5] A. Burns, R. Davis, R. Bril, J. Lukkien: CAN Schedulability Analysis: Refuted, Revised and Revi-
sited. Real-Time Systems Journal, Springer Verlag, Heft 3, 2007, S. 239-272
[6] T. Nolte, H. Hansson, C. Norström, S. Punnekkat: Using Bit-stuffing Distributions in CAN Ana-
lysis. IEEE Real-time Embedded Systems Workshop, London, Dez. 2001
[7] S. Punnekkat, H. Hansson, C. Norström: Response Time Analysis under Errors for CAN. IEEE
Real-Time Technology and Applications Symposium, Juni 2000, S. 258-265
"""

"""
Note: The number of stuff bits inserted depends on the data transmitted. A conservative estimate is, that in average,
the number of stuff bits will be below the following values:

    For 11-bit IDs: 3 + number of data bytes
    For 29-bit IDs: 5 + number of data bytes

"""

"""
TFrame = n Frame x T bit = (n Header + n Trailer + n Idle + n Data + n Stuff ) x T bit

nHeader + nTrailer + nIdle = 47 bit (67 bit)

Buslänge ≤ 40..50 m x   Mbit
                        -------
                        Bitrate
_________________________________________________________________________________________________________________
                        Länge ohne Stuffing             Länge mit Stuffing
_________________________________________________________________________________________________________________
CAN ID      n Data      n Frame, min    T Frame, min    n Frame, max    T Frame, max    f Data = n Data / T Frame
11 bit
            1 byte      55 bit          110 μs          65 bit          130 μs          7,5 KB/s
            8 byte      111 bit         222 μs          135 bit         270 μs          28,9 KB/s
29 bit
            1 byte      75 bit          150 μs          90 bit          180 μs          5,4 KB/s
            8 byte      131 bit         262 μs          160 bit         320 μs          24,4 KB/s
"""

#print(maxFrameLength(1, False))
#print(maxFrameLength(1, True))
#print(maxFrameLength(8, False))
#print(maxFrameLength(8, True))


"""
CANID   nData   PeriodT     TLatency,min = TFrame   TLatency, max = TWarte,max + TFrame
1       1 byte  50 ms       0,5 ms                  1,4 ms
2       2 byte  5 ms        0,6 ms                  2,0 ms
3       1 byte  5 ms        0,5 ms                  2,6 ms
4       2 byte  5 ms        0,6 ms                  3,2 ms
5       1 byte  5 ms        0,5 ms                  3,7 ms
6       2 byte  5 ms        0,6 ms                  4,3 ms
7       6 byte  10 ms       0,9 ms                  5,0 ms
8       1 byte  10 ms       0,5 ms                  8,6 ms
9       2 byte  10 ms       0,6 ms                  9,2 ms
10      3 byte  10 ms       0,7 ms                  9,9 ms
"""

MSGS = (
    (1,     1,  50,   0.5,    1.4),
    (2,     2,  5,    0.6,    2.0),
    (3,     1,  5,    0.5,    2.6),
    (4,     2,  5,    0.6,    3.2),
    (5,     1,  5,    0.5,    3.7),
    (6,     2,  5,    0.6,    4.3),
    (7,     6,  10,   0.9,    5.0),
    (8,     1,  10,   0.5,    8.6),
    (9,     2,  10,   0.6,    9.2),
    (10,    3,  10,   0.7,    9.9),
)

class Latency(object):

    def __init__(self, msgs, speed):
        self.msgs = msgs
        self.speed = speed
        self.fBit = D(speed * 1000)
        self.tBit =  D(1) / D(self.fBit)
        
    def calcLatency(self, pos, speed):
        canID, nData, period, latMin, latMax = self.msgs[pos]
        nFrame = maxFrameLength(nData, False)
        tFrame = D(nFrame) * D(self.tBit)
        print(self.longestFrame(pos))
        print(nFrame, D(tFrame) * D(1000 * 1000))
        print(item)

    def longestFrame(self, startPos):
        maxLen = 0
        pos = None
        for idx, item in enumerate(x for x in self.msgs[startPos : ]):
            if item[1] > maxLen:
                maxLen = item[1]
                pos = idx
        return (maxLen, D(maxFrameLength(maxLen, False)) * D(self.tBit))

lat = Latency(MSGS, 125)
lat.calcLatency(1, 125)

def calcLatencies(speed):
    fBit = D(speed * 1000)
    tBit =  D(1) / D(fBit)

    for canID, nData, period, latMin, latMax in MSGS:
        nFrame = maxFrameLength(nData, False)
        tFrame = D(nFrame) * D(tBit)
        print(nFrame, D(tFrame) * D(1000 * 1000))
        print(item)

calcLatencies(125)