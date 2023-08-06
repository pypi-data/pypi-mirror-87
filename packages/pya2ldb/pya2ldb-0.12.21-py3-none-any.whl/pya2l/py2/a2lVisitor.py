# Generated from a2l.g4 by ANTLR 4.7
from antlr4 import *

# This class defines a complete generic visitor for a parse tree produced by a2lParser.

class a2lVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by a2lParser#a2lFile.
    def visitA2lFile(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#alignmentByte.
    def visitAlignmentByte(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#alignmentFloat32Ieee.
    def visitAlignmentFloat32Ieee(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#alignmentFloat64Ieee.
    def visitAlignmentFloat64Ieee(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#alignmentInt64.
    def visitAlignmentInt64(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#alignmentLong.
    def visitAlignmentLong(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#alignmentWord.
    def visitAlignmentWord(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#annotation.
    def visitAnnotation(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#annotationLabel.
    def visitAnnotationLabel(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#annotationOrigin.
    def visitAnnotationOrigin(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#annotationText.
    def visitAnnotationText(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#bitMask.
    def visitBitMask(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#byteOrder.
    def visitByteOrder(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#calibrationAccess.
    def visitCalibrationAccess(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#defaultValue.
    def visitDefaultValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#deposit.
    def visitDeposit(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#discrete.
    def visitDiscrete(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#displayIdentifier.
    def visitDisplayIdentifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ecuAddressExtension.
    def visitEcuAddressExtension(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#extendedLimits.
    def visitExtendedLimits(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#format_.
    def visitFormat_(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#functionList.
    def visitFunctionList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#guardRails.
    def visitGuardRails(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ifData.
    def visitIfData(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#matrixDim.
    def visitMatrixDim(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#maxRefresh.
    def visitMaxRefresh(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#monotony.
    def visitMonotony(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#physUnit.
    def visitPhysUnit(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#readOnly.
    def visitReadOnly(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#refCharacteristic.
    def visitRefCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#refMemorySegment.
    def visitRefMemorySegment(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#refUnit.
    def visitRefUnit(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#stepSize.
    def visitStepSize(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#symbolLink.
    def visitSymbolLink(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#version.
    def visitVersion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#asap2Version.
    def visitAsap2Version(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#a2mlVersion.
    def visitA2mlVersion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#project.
    def visitProject(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#header.
    def visitHeader(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#projectNo.
    def visitProjectNo(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#module.
    def visitModule(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#a2ml.
    def visitA2ml(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPts.
    def visitAxisPts(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#characteristic.
    def visitCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisDescr.
    def visitAxisDescr(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPtsRef.
    def visitAxisPtsRef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#curveAxisRef.
    def visitCurveAxisRef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixAxisPar.
    def visitFixAxisPar(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixAxisParDist.
    def visitFixAxisParDist(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixAxisParList.
    def visitFixAxisParList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#maxGrad.
    def visitMaxGrad(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#comparisonQuantity.
    def visitComparisonQuantity(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#dependentCharacteristic.
    def visitDependentCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#mapList.
    def visitMapList(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#number.
    def visitNumber(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#virtualCharacteristic.
    def visitVirtualCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#compuMethod.
    def visitCompuMethod(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#coeffs.
    def visitCoeffs(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#coeffsLinear.
    def visitCoeffsLinear(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#compuTabRef.
    def visitCompuTabRef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#formula.
    def visitFormula(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#formulaInv.
    def visitFormulaInv(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#statusStringRef.
    def visitStatusStringRef(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#compuTab.
    def visitCompuTab(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#defaultValueNumeric.
    def visitDefaultValueNumeric(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#compuVtab.
    def visitCompuVtab(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#compuVtabRange.
    def visitCompuVtabRange(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#frame.
    def visitFrame(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#frameMeasurement.
    def visitFrameMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#function.
    def visitFunction(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#defCharacteristic.
    def visitDefCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#functionVersion.
    def visitFunctionVersion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#inMeasurement.
    def visitInMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#locMeasurement.
    def visitLocMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#outMeasurement.
    def visitOutMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#subFunction.
    def visitSubFunction(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#group.
    def visitGroup(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#refMeasurement.
    def visitRefMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#root.
    def visitRoot(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#subGroup.
    def visitSubGroup(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#measurement.
    def visitMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#arraySize.
    def visitArraySize(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#bitOperation.
    def visitBitOperation(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#leftShift.
    def visitLeftShift(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#rightShift.
    def visitRightShift(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#signExtend.
    def visitSignExtend(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ecuAddress.
    def visitEcuAddress(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#errorMask.
    def visitErrorMask(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#layout.
    def visitLayout(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#readWrite.
    def visitReadWrite(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#virtual.
    def visitVirtual(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#modCommon.
    def visitModCommon(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#dataSize.
    def visitDataSize(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#sRecLayout.
    def visitSRecLayout(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#modPar.
    def visitModPar(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#addrEpk.
    def visitAddrEpk(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#calibrationMethod.
    def visitCalibrationMethod(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#calibrationHandle.
    def visitCalibrationHandle(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#calibrationHandleText.
    def visitCalibrationHandleText(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#cpuType.
    def visitCpuType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#customer.
    def visitCustomer(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#customerNo.
    def visitCustomerNo(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ecu.
    def visitEcu(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ecuCalibrationOffset.
    def visitEcuCalibrationOffset(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#epk.
    def visitEpk(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#memoryLayout.
    def visitMemoryLayout(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#memorySegment.
    def visitMemorySegment(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noOfInterfaces.
    def visitNoOfInterfaces(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#phoneNo.
    def visitPhoneNo(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#supplier.
    def visitSupplier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#systemConstant.
    def visitSystemConstant(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#user.
    def visitUser(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#recordLayout.
    def visitRecordLayout(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPtsX.
    def visitAxisPtsX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPtsY.
    def visitAxisPtsY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPtsZ.
    def visitAxisPtsZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPts4.
    def visitAxisPts4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisPts5.
    def visitAxisPts5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisRescaleX.
    def visitAxisRescaleX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisRescaleY.
    def visitAxisRescaleY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisRescaleZ.
    def visitAxisRescaleZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisRescale4.
    def visitAxisRescale4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#axisRescale5.
    def visitAxisRescale5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#distOpX.
    def visitDistOpX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#distOpY.
    def visitDistOpY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#distOpZ.
    def visitDistOpZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#distOp4.
    def visitDistOp4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#distOp5.
    def visitDistOp5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixNoAxisPtsX.
    def visitFixNoAxisPtsX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixNoAxisPtsY.
    def visitFixNoAxisPtsY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixNoAxisPtsZ.
    def visitFixNoAxisPtsZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixNoAxisPts4.
    def visitFixNoAxisPts4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fixNoAxisPts5.
    def visitFixNoAxisPts5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#fncValues.
    def visitFncValues(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#identification.
    def visitIdentification(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noAxisPtsX.
    def visitNoAxisPtsX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noAxisPtsY.
    def visitNoAxisPtsY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noAxisPtsZ.
    def visitNoAxisPtsZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noAxisPts4.
    def visitNoAxisPts4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noAxisPts5.
    def visitNoAxisPts5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#staticRecordLayout.
    def visitStaticRecordLayout(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noRescaleX.
    def visitNoRescaleX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noRescaleY.
    def visitNoRescaleY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noRescaleZ.
    def visitNoRescaleZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noRescale4.
    def visitNoRescale4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#noRescale5.
    def visitNoRescale5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#offsetX.
    def visitOffsetX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#offsetY.
    def visitOffsetY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#offsetZ.
    def visitOffsetZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#offset4.
    def visitOffset4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#offset5.
    def visitOffset5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#reserved.
    def visitReserved(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ripAddrW.
    def visitRipAddrW(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ripAddrX.
    def visitRipAddrX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ripAddrY.
    def visitRipAddrY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ripAddrZ.
    def visitRipAddrZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ripAddr4.
    def visitRipAddr4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#ripAddr5.
    def visitRipAddr5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#shiftOpX.
    def visitShiftOpX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#shiftOpY.
    def visitShiftOpY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#shiftOpZ.
    def visitShiftOpZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#shiftOp4.
    def visitShiftOp4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#shiftOp5.
    def visitShiftOp5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#srcAddrX.
    def visitSrcAddrX(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#srcAddrY.
    def visitSrcAddrY(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#srcAddrZ.
    def visitSrcAddrZ(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#srcAddr4.
    def visitSrcAddr4(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#srcAddr5.
    def visitSrcAddr5(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#unit.
    def visitUnit(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#siExponents.
    def visitSiExponents(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#unitConversion.
    def visitUnitConversion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#userRights.
    def visitUserRights(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#refGroup.
    def visitRefGroup(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#variantCoding.
    def visitVariantCoding(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varCharacteristic.
    def visitVarCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varAddress.
    def visitVarAddress(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varCriterion.
    def visitVarCriterion(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varMeasurement.
    def visitVarMeasurement(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varSelectionCharacteristic.
    def visitVarSelectionCharacteristic(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varForbiddenComb.
    def visitVarForbiddenComb(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varNaming.
    def visitVarNaming(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#varSeparator.
    def visitVarSeparator(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#integerValue.
    def visitIntegerValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#floatValue.
    def visitFloatValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#stringValue.
    def visitStringValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#identifierValue.
    def visitIdentifierValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#partialIdentifier.
    def visitPartialIdentifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#arraySpecifier.
    def visitArraySpecifier(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#dataType.
    def visitDataType(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#datasize.
    def visitDatasize(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#addrtype.
    def visitAddrtype(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#byteOrderValue.
    def visitByteOrderValue(self, ctx):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by a2lParser#indexorder.
    def visitIndexorder(self, ctx):
        return self.visitChildren(ctx)


