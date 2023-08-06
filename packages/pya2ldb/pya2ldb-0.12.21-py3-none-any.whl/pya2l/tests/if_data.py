

from pprint import pprint

from pya2l.aml_listener import AMLListener, AMLPredefinedTypes, map_predefined_type
from pya2l.parserlib import ParserWrapper



FNAME = r"F:\projekte\csProjects\k-A2L\examples\ASAP2_Demo_V161.aml"

parser = ParserWrapper("aml", "amlFile", AMLListener, useDatabase=False)

"""
F:\projekte\csProjects\k-A2L\pya2l\tests>py -3 if_data.py
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__form
at__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__',
 '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__
 repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref_
 _', 'block_definitions', 'declarations', 'enterBlock_definition', 'enterEveryRul
 e', 'enum_types', 'exitAmlFile', 'exitArray_specifier', 'exitBlock_definition',
 'exitDeclaration', 'exitEnum_type_name', 'exitEnumerator', 'exitEnumerator_list'
 , 'exitEveryRule', 'exitFloatValue', 'exitIdentifierValue', 'exitIntValue', 'exi
 tMember', 'exitNumber', 'exitNumericValue', 'exitPredefined_type_name', 'exitStr
 ingValue', 'exitStruct_member', 'exitStruct_type_name', 'exitTagValue', 'exitTag
 ged_union_member', 'exitTaggedstruct_definition', 'exitTaggedstruct_member', 'ex
 itTaggedstruct_type_name', 'exitTaggedunion_type_name', 'exitType_definition', '
 exitType_name', 'level', 'struct_types', 'tagged_struct_types', 'tagged_union_ty
 pes', 'type_definitions', 'value', 'visitErrorNode', 'visitTerminal']
"""

res = parser.parseFromString(open(FNAME, "rt").read())
#print(res.struct_types)
#print(res.value[0].to_json())
#print(type(res.value[0]))
for elem in res.value:
    print(type(elem))

parser = ParserWrapper("aml", "type_definition", AMLListener, useDatabase=False)
DATA = """struct {
                    char[101];  /* EVENT_CHANNEL_NAME       */
                            char[9];    /* EVENT_CHANNEL_SHORT_NAME */
                                    uint;       /* EVENT_CHANNEL_NUMBER     */
                                            enum {
                                                          "DAQ" = 1,
                                                                    "STIM" = 2,
                                                                              "DAQ_STIM" = 3
                                                                                      };
                                                                                              uchar;  /* MAX_DAQ_LIST */
                                                                                                      uchar;  /* TIME_CYCLE   */
                                                                                                              uchar;  /* TIME_UNIT    */
                                                                                                                      uchar;  /* PRIORITY     */
                                                                                                                          };
                                                                        """

res = parser.parseFromString(DATA)
#print(res.type_definitions)
