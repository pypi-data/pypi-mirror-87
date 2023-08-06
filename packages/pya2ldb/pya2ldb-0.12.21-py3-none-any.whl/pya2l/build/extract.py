#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import defaultdict
import enum
import re
import textwrap

import PyPDF2
import toml

class StateType(enum.IntEnum):
    FIRST_PAGE  = 1
    COLLECTING  = 2
    DONE        = 3


class EventType(enum.IntEnum):
    NONE    = 0
    FP      = 1
    CP      = 2


FIRST_PAGE_FRAMING = re.compile(r"""^\s*Format\sof\sthe\sdescription\sfile\s+(?:\d\.\d\.\d+)\s+?
(?P<content>.*)\s*
(?P<page_num_even>\d+)?\s+ASAM\sMCD\-2MC\sVersion\s(?:\d.\d+)\s+(?P<page_num_odd>\d+)?\s*
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)

FOLLOWUP_PAGE_FRAMING = re.compile(r"""^\s*Format\sof\sthe\sdescription\sfile\s*
(?P<content>.*)\s*
(?P<page_num_even>\d+)?\s*ASAM\sMCD\-2MC\sVersion\s(?:\d.\d+)\s?(?P<page_num_odd>\d+)?\s*
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)


CONTENT = re.compile(r"""(?P<tag>.*)\s+
Prototype:(?P<prototype>.*?)
Parameters:(?P<parameters>.*?)
(?:Optional Parameters:(?P<options>.*?))?
Description:(?P<description>.*)
(?:Example:(?P<example>.*?))?
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)

##ADDR_EPK Prototype:

STRIPPY = re.compile(r"""(?P<tag>[A-Z_0-9 ]+)Prototype:(?P<proto>.*)
(Parameters:(?P<params>.*))?
Description:(?P<descr>.*)
(?P<data>.*)
""", re.MULTILINE | re.VERBOSE | re.DOTALL | re.UNICODE)

PDF_FILE = open(r"F:\projekte\csProjects\k-A2L\pya2l\ASAM_MCD-2MC_DataSpecifcation_V1.6.pdf", "rb")

def convert(data):
    "Prototype:"
    "Parameters:"
    "Description:"
    "Example:"
    pos = data.find("Prototype:")
    if pos != -1:
        tag = data[: pos ].strip()
    else:
        tag = ""
    print("***{}***".format(tag))
    rem = data[pos + len("Prototype:") : ]
    pos = data.find("Parameters:")
    if pos != -1:
        params = data[: pos  + len("Parameters:")].strip()
    else:
        params = []
    rem = data[pos : ]
    pos = data.find("Description:")
    if pos != -1:
        descr = data[: pos ].strip()
    else:
        print("NO DESCR!!!")
        descr = ""
    rem = data[pos + len("Description:") : ]
    xxx = dict(tag = tag, params = params, descr = descr)
    #print(xxx, end = "\n\n")
    return data

pdf_reader = PyPDF2.PdfFileReader(PDF_FILE)
print(pdf_reader)
num_pages = pdf_reader.getNumPages()
#for idx in range(num_pages):

result_pages = defaultdict(str)
current_tag = None

state = StateType.FIRST_PAGE
event = EventType.NONE
previousEvent = EventType.NONE
result = ""
with open("asam.txt", "wt", encoding = "utf8") as of:
    for idx in range(28, 217):
        try:
            page = pdf_reader.getPage(idx)
            page_content = page.extractText()

            match = FIRST_PAGE_FRAMING.search(page_content)
            if match is None:
                match = FOLLOWUP_PAGE_FRAMING.search(page_content)
                event = EventType.CP
            else:
                event = EventType.FP
                #current_tag = match.group("tag")
                #print("*** TAG:", current_tag)
            content = match.group("content")
            if "AXIS_DESCR" in content:
                pass
            #print("{}".format(content))
            if state == StateType.FIRST_PAGE:
                result = content
                if event == EventType.FP and previousEvent == EventType.FP:
                    state = StateType.DONE
                elif event == EventType.CP:
                    state = StateType.COLLECTING
            elif state == StateType.COLLECTING:
                result += content
                if event == EventType.FP:
                    state = StateType.DONE
                elif event == EventType.CP:
                    pass
            #print("=== State: {} Event: {}".format(str(state), str(event)))
            assert match is not None
            if state == StateType.DONE:
                result = convert(result)
                of.write(result)
                of.write("\n\n")
                print("{}".format(result), end = "\n\n\n")
                result = ""
            if state == StateType.DONE:
                state = StateType.FIRST_PAGE
            previousEvent = event
        except Exception as e:
            print("{} on page #{}".format(str(e), idx))
