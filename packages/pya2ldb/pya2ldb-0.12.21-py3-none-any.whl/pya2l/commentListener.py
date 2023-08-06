# Generated from comment.g4 by ANTLR 4.6
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .commentParser import commentParser
else:
    from commentParser import commentParser

# This class defines a complete listener for a parse tree produced by commentParser.
class commentListener(ParseTreeListener):

    # Enter a parse tree produced by commentParser#main.
    def enterMain(self, ctx:commentParser.MainContext):
        pass

    # Exit a parse tree produced by commentParser#main.
    def exitMain(self, ctx:commentParser.MainContext):
        pass


    # Enter a parse tree produced by commentParser#object_definition.
    def enterObject_definition(self, ctx:commentParser.Object_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#object_definition.
    def exitObject_definition(self, ctx:commentParser.Object_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#maingroup_definition.
    def enterMaingroup_definition(self, ctx:commentParser.Maingroup_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#maingroup_definition.
    def exitMaingroup_definition(self, ctx:commentParser.Maingroup_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#subgroup_definition.
    def enterSubgroup_definition(self, ctx:commentParser.Subgroup_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#subgroup_definition.
    def exitSubgroup_definition(self, ctx:commentParser.Subgroup_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#measure_definition.
    def enterMeasure_definition(self, ctx:commentParser.Measure_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#measure_definition.
    def exitMeasure_definition(self, ctx:commentParser.Measure_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#parameter_definition.
    def enterParameter_definition(self, ctx:commentParser.Parameter_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#parameter_definition.
    def exitParameter_definition(self, ctx:commentParser.Parameter_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#string_definition.
    def enterString_definition(self, ctx:commentParser.String_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#string_definition.
    def exitString_definition(self, ctx:commentParser.String_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#conversion_definition.
    def enterConversion_definition(self, ctx:commentParser.Conversion_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#conversion_definition.
    def exitConversion_definition(self, ctx:commentParser.Conversion_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#write_access.
    def enterWrite_access(self, ctx:commentParser.Write_accessContext):
        pass

    # Exit a parse tree produced by commentParser#write_access.
    def exitWrite_access(self, ctx:commentParser.Write_accessContext):
        pass


    # Enter a parse tree produced by commentParser#length.
    def enterLength(self, ctx:commentParser.LengthContext):
        pass

    # Exit a parse tree produced by commentParser#length.
    def exitLength(self, ctx:commentParser.LengthContext):
        pass


    # Enter a parse tree produced by commentParser#datatype.
    def enterDatatype(self, ctx:commentParser.DatatypeContext):
        pass

    # Exit a parse tree produced by commentParser#datatype.
    def exitDatatype(self, ctx:commentParser.DatatypeContext):
        pass


    # Enter a parse tree produced by commentParser#rng.
    def enterRng(self, ctx:commentParser.RngContext):
        pass

    # Exit a parse tree produced by commentParser#rng.
    def exitRng(self, ctx:commentParser.RngContext):
        pass


    # Enter a parse tree produced by commentParser#bitmask.
    def enterBitmask(self, ctx:commentParser.BitmaskContext):
        pass

    # Exit a parse tree produced by commentParser#bitmask.
    def exitBitmask(self, ctx:commentParser.BitmaskContext):
        pass


    # Enter a parse tree produced by commentParser#attribute.
    def enterAttribute(self, ctx:commentParser.AttributeContext):
        pass

    # Exit a parse tree produced by commentParser#attribute.
    def exitAttribute(self, ctx:commentParser.AttributeContext):
        pass


    # Enter a parse tree produced by commentParser#string_attribute.
    def enterString_attribute(self, ctx:commentParser.String_attributeContext):
        pass

    # Exit a parse tree produced by commentParser#string_attribute.
    def exitString_attribute(self, ctx:commentParser.String_attributeContext):
        pass


    # Enter a parse tree produced by commentParser#conversion.
    def enterConversion(self, ctx:commentParser.ConversionContext):
        pass

    # Exit a parse tree produced by commentParser#conversion.
    def exitConversion(self, ctx:commentParser.ConversionContext):
        pass


    # Enter a parse tree produced by commentParser#factor.
    def enterFactor(self, ctx:commentParser.FactorContext):
        pass

    # Exit a parse tree produced by commentParser#factor.
    def exitFactor(self, ctx:commentParser.FactorContext):
        pass


    # Enter a parse tree produced by commentParser#offset.
    def enterOffset(self, ctx:commentParser.OffsetContext):
        pass

    # Exit a parse tree produced by commentParser#offset.
    def exitOffset(self, ctx:commentParser.OffsetContext):
        pass


    # Enter a parse tree produced by commentParser#digits.
    def enterDigits(self, ctx:commentParser.DigitsContext):
        pass

    # Exit a parse tree produced by commentParser#digits.
    def exitDigits(self, ctx:commentParser.DigitsContext):
        pass


    # Enter a parse tree produced by commentParser#unit.
    def enterUnit(self, ctx:commentParser.UnitContext):
        pass

    # Exit a parse tree produced by commentParser#unit.
    def exitUnit(self, ctx:commentParser.UnitContext):
        pass


    # Enter a parse tree produced by commentParser#description.
    def enterDescription(self, ctx:commentParser.DescriptionContext):
        pass

    # Exit a parse tree produced by commentParser#description.
    def exitDescription(self, ctx:commentParser.DescriptionContext):
        pass


    # Enter a parse tree produced by commentParser#alias.
    def enterAlias(self, ctx:commentParser.AliasContext):
        pass

    # Exit a parse tree produced by commentParser#alias.
    def exitAlias(self, ctx:commentParser.AliasContext):
        pass


    # Enter a parse tree produced by commentParser#base_offset.
    def enterBase_offset(self, ctx:commentParser.Base_offsetContext):
        pass

    # Exit a parse tree produced by commentParser#base_offset.
    def exitBase_offset(self, ctx:commentParser.Base_offsetContext):
        pass


    # Enter a parse tree produced by commentParser#group_assignment.
    def enterGroup_assignment(self, ctx:commentParser.Group_assignmentContext):
        pass

    # Exit a parse tree produced by commentParser#group_assignment.
    def exitGroup_assignment(self, ctx:commentParser.Group_assignmentContext):
        pass


    # Enter a parse tree produced by commentParser#dimension.
    def enterDimension(self, ctx:commentParser.DimensionContext):
        pass

    # Exit a parse tree produced by commentParser#dimension.
    def exitDimension(self, ctx:commentParser.DimensionContext):
        pass


    # Enter a parse tree produced by commentParser#split.
    def enterSplit(self, ctx:commentParser.SplitContext):
        pass

    # Exit a parse tree produced by commentParser#split.
    def exitSplit(self, ctx:commentParser.SplitContext):
        pass


    # Enter a parse tree produced by commentParser#address.
    def enterAddress(self, ctx:commentParser.AddressContext):
        pass

    # Exit a parse tree produced by commentParser#address.
    def exitAddress(self, ctx:commentParser.AddressContext):
        pass


    # Enter a parse tree produced by commentParser#address_extension.
    def enterAddress_extension(self, ctx:commentParser.Address_extensionContext):
        pass

    # Exit a parse tree produced by commentParser#address_extension.
    def exitAddress_extension(self, ctx:commentParser.Address_extensionContext):
        pass


    # Enter a parse tree produced by commentParser#color.
    def enterColor(self, ctx:commentParser.ColorContext):
        pass

    # Exit a parse tree produced by commentParser#color.
    def exitColor(self, ctx:commentParser.ColorContext):
        pass


    # Enter a parse tree produced by commentParser#event.
    def enterEvent(self, ctx:commentParser.EventContext):
        pass

    # Exit a parse tree produced by commentParser#event.
    def exitEvent(self, ctx:commentParser.EventContext):
        pass


    # Enter a parse tree produced by commentParser#structure_definition.
    def enterStructure_definition(self, ctx:commentParser.Structure_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#structure_definition.
    def exitStructure_definition(self, ctx:commentParser.Structure_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#structure_path.
    def enterStructure_path(self, ctx:commentParser.Structure_pathContext):
        pass

    # Exit a parse tree produced by commentParser#structure_path.
    def exitStructure_path(self, ctx:commentParser.Structure_pathContext):
        pass


    # Enter a parse tree produced by commentParser#element_path.
    def enterElement_path(self, ctx:commentParser.Element_pathContext):
        pass

    # Exit a parse tree produced by commentParser#element_path.
    def exitElement_path(self, ctx:commentParser.Element_pathContext):
        pass


    # Enter a parse tree produced by commentParser#structure_attribute.
    def enterStructure_attribute(self, ctx:commentParser.Structure_attributeContext):
        pass

    # Exit a parse tree produced by commentParser#structure_attribute.
    def exitStructure_attribute(self, ctx:commentParser.Structure_attributeContext):
        pass


    # Enter a parse tree produced by commentParser#instance_definition.
    def enterInstance_definition(self, ctx:commentParser.Instance_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#instance_definition.
    def exitInstance_definition(self, ctx:commentParser.Instance_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#overwrite_definition.
    def enterOverwrite_definition(self, ctx:commentParser.Overwrite_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#overwrite_definition.
    def exitOverwrite_definition(self, ctx:commentParser.Overwrite_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#overwrite.
    def enterOverwrite(self, ctx:commentParser.OverwriteContext):
        pass

    # Exit a parse tree produced by commentParser#overwrite.
    def exitOverwrite(self, ctx:commentParser.OverwriteContext):
        pass


    # Enter a parse tree produced by commentParser#curve_definition.
    def enterCurve_definition(self, ctx:commentParser.Curve_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#curve_definition.
    def exitCurve_definition(self, ctx:commentParser.Curve_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#map_definition.
    def enterMap_definition(self, ctx:commentParser.Map_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#map_definition.
    def exitMap_definition(self, ctx:commentParser.Map_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#axis_definition.
    def enterAxis_definition(self, ctx:commentParser.Axis_definitionContext):
        pass

    # Exit a parse tree produced by commentParser#axis_definition.
    def exitAxis_definition(self, ctx:commentParser.Axis_definitionContext):
        pass


    # Enter a parse tree produced by commentParser#map_attribute.
    def enterMap_attribute(self, ctx:commentParser.Map_attributeContext):
        pass

    # Exit a parse tree produced by commentParser#map_attribute.
    def exitMap_attribute(self, ctx:commentParser.Map_attributeContext):
        pass


    # Enter a parse tree produced by commentParser#byte_order.
    def enterByte_order(self, ctx:commentParser.Byte_orderContext):
        pass

    # Exit a parse tree produced by commentParser#byte_order.
    def exitByte_order(self, ctx:commentParser.Byte_orderContext):
        pass


    # Enter a parse tree produced by commentParser#axis.
    def enterAxis(self, ctx:commentParser.AxisContext):
        pass

    # Exit a parse tree produced by commentParser#axis.
    def exitAxis(self, ctx:commentParser.AxisContext):
        pass


    # Enter a parse tree produced by commentParser#input_signal.
    def enterInput_signal(self, ctx:commentParser.Input_signalContext):
        pass

    # Exit a parse tree produced by commentParser#input_signal.
    def exitInput_signal(self, ctx:commentParser.Input_signalContext):
        pass


    # Enter a parse tree produced by commentParser#list_of_axis_points.
    def enterList_of_axis_points(self, ctx:commentParser.List_of_axis_pointsContext):
        pass

    # Exit a parse tree produced by commentParser#list_of_axis_points.
    def exitList_of_axis_points(self, ctx:commentParser.List_of_axis_pointsContext):
        pass


    # Enter a parse tree produced by commentParser#variant_criterion.
    def enterVariant_criterion(self, ctx:commentParser.Variant_criterionContext):
        pass

    # Exit a parse tree produced by commentParser#variant_criterion.
    def exitVariant_criterion(self, ctx:commentParser.Variant_criterionContext):
        pass


    # Enter a parse tree produced by commentParser#variant.
    def enterVariant(self, ctx:commentParser.VariantContext):
        pass

    # Exit a parse tree produced by commentParser#variant.
    def exitVariant(self, ctx:commentParser.VariantContext):
        pass


    # Enter a parse tree produced by commentParser#constant.
    def enterConstant(self, ctx:commentParser.ConstantContext):
        pass

    # Exit a parse tree produced by commentParser#constant.
    def exitConstant(self, ctx:commentParser.ConstantContext):
        pass


    # Enter a parse tree produced by commentParser#value.
    def enterValue(self, ctx:commentParser.ValueContext):
        pass

    # Exit a parse tree produced by commentParser#value.
    def exitValue(self, ctx:commentParser.ValueContext):
        pass


    # Enter a parse tree produced by commentParser#name.
    def enterName(self, ctx:commentParser.NameContext):
        pass

    # Exit a parse tree produced by commentParser#name.
    def exitName(self, ctx:commentParser.NameContext):
        pass


    # Enter a parse tree produced by commentParser#group_name.
    def enterGroup_name(self, ctx:commentParser.Group_nameContext):
        pass

    # Exit a parse tree produced by commentParser#group_name.
    def exitGroup_name(self, ctx:commentParser.Group_nameContext):
        pass


    # Enter a parse tree produced by commentParser#symbol_name.
    def enterSymbol_name(self, ctx:commentParser.Symbol_nameContext):
        pass

    # Exit a parse tree produced by commentParser#symbol_name.
    def exitSymbol_name(self, ctx:commentParser.Symbol_nameContext):
        pass


    # Enter a parse tree produced by commentParser#element_name.
    def enterElement_name(self, ctx:commentParser.Element_nameContext):
        pass

    # Exit a parse tree produced by commentParser#element_name.
    def exitElement_name(self, ctx:commentParser.Element_nameContext):
        pass


    # Enter a parse tree produced by commentParser#layout_name.
    def enterLayout_name(self, ctx:commentParser.Layout_nameContext):
        pass

    # Exit a parse tree produced by commentParser#layout_name.
    def exitLayout_name(self, ctx:commentParser.Layout_nameContext):
        pass


    # Enter a parse tree produced by commentParser#structure_name.
    def enterStructure_name(self, ctx:commentParser.Structure_nameContext):
        pass

    # Exit a parse tree produced by commentParser#structure_name.
    def exitStructure_name(self, ctx:commentParser.Structure_nameContext):
        pass


    # Enter a parse tree produced by commentParser#alias_name.
    def enterAlias_name(self, ctx:commentParser.Alias_nameContext):
        pass

    # Exit a parse tree produced by commentParser#alias_name.
    def exitAlias_name(self, ctx:commentParser.Alias_nameContext):
        pass


    # Enter a parse tree produced by commentParser#conversion_name.
    def enterConversion_name(self, ctx:commentParser.Conversion_nameContext):
        pass

    # Exit a parse tree produced by commentParser#conversion_name.
    def exitConversion_name(self, ctx:commentParser.Conversion_nameContext):
        pass


    # Enter a parse tree produced by commentParser#a2l_name.
    def enterA2l_name(self, ctx:commentParser.A2l_nameContext):
        pass

    # Exit a parse tree produced by commentParser#a2l_name.
    def exitA2l_name(self, ctx:commentParser.A2l_nameContext):
        pass


    # Enter a parse tree produced by commentParser#string.
    def enterString(self, ctx:commentParser.StringContext):
        pass

    # Exit a parse tree produced by commentParser#string.
    def exitString(self, ctx:commentParser.StringContext):
        pass


    # Enter a parse tree produced by commentParser#common_axis_name.
    def enterCommon_axis_name(self, ctx:commentParser.Common_axis_nameContext):
        pass

    # Exit a parse tree produced by commentParser#common_axis_name.
    def exitCommon_axis_name(self, ctx:commentParser.Common_axis_nameContext):
        pass


    # Enter a parse tree produced by commentParser#input_signal_name.
    def enterInput_signal_name(self, ctx:commentParser.Input_signal_nameContext):
        pass

    # Exit a parse tree produced by commentParser#input_signal_name.
    def exitInput_signal_name(self, ctx:commentParser.Input_signal_nameContext):
        pass


    # Enter a parse tree produced by commentParser#min_value.
    def enterMin_value(self, ctx:commentParser.Min_valueContext):
        pass

    # Exit a parse tree produced by commentParser#min_value.
    def exitMin_value(self, ctx:commentParser.Min_valueContext):
        pass


    # Enter a parse tree produced by commentParser#max_value.
    def enterMax_value(self, ctx:commentParser.Max_valueContext):
        pass

    # Exit a parse tree produced by commentParser#max_value.
    def exitMax_value(self, ctx:commentParser.Max_valueContext):
        pass


    # Enter a parse tree produced by commentParser#selector_value.
    def enterSelector_value(self, ctx:commentParser.Selector_valueContext):
        pass

    # Exit a parse tree produced by commentParser#selector_value.
    def exitSelector_value(self, ctx:commentParser.Selector_valueContext):
        pass


    # Enter a parse tree produced by commentParser#distance.
    def enterDistance(self, ctx:commentParser.DistanceContext):
        pass

    # Exit a parse tree produced by commentParser#distance.
    def exitDistance(self, ctx:commentParser.DistanceContext):
        pass


