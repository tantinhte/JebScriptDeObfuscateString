# -*- coding: utf-8 -*-

from com.pnfsoftware.jeb.client.api import IScript, IGraphicalClientContext
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.actions import Actions, ActionContext, ActionCommentData, ActionXrefsData
from com.pnfsoftware.jeb.core.events import JebEvent, J
from com.pnfsoftware.jeb.core.output import AbstractUnitRepresentation, UnitRepresentationAdapter
from com.pnfsoftware.jeb.core.units.code import ICodeUnit, ICodeItem
from com.pnfsoftware.jeb.core.units.code.java import IJavaSourceUnit, IJavaStaticField, IJavaNewArray, IJavaConstant, \
    IJavaCall, IJavaField, IJavaMethod, IJavaClass, IJavaConstantFactory, IJavaAssignment


class tandd3(IScript):
    method_sig = "Lcom/tracer/l/a;->a(Ljava/lang/String;)Ljava/lang/String;"

    def run(self, ctx):

        engctx = ctx.getEnginesContext()
        if not engctx:
            print('Back-end engines not initialized')
            return

        projects = engctx.getProjects()
        if not projects:
            print('There is no opened project')
            return

        project = projects[0]  # Get current project(IRuntimeProject)
        print('Decompiling code units of %s...' % project)

        units = RuntimeProjectUtil.findUnitsByType(project, IJavaSourceUnit, False)
        total = 0
        change = 0
        for unit in units:
            self.cstbuilder = unit.getFactories().getConstantFactory()
            class_data = unit.getClassElement()
            total += 1
            if isinstance(class_data, IJavaClass):
                for method_data in class_data.getMethods():
                    if class_data.getName() == "Lcom/tracer/k/z;":
                        print(method_data.getName())
                    if method_data.getName() == "<init>":
                        body = method_data.getBody()
                        for instruction in body:
                            if isinstance(instruction, IJavaAssignment):
                                if isinstance(instruction.getLeft(), IJavaField) or isinstance(instruction.getLeft(),
                                                                                               IJavaStaticField):
                                    call_instruction = instruction.getRight()
                                    if isinstance(call_instruction, IJavaCall):
                                        if call_instruction.getMethod().getSignature() == self.method_sig:
                                            args = call_instruction.getArguments()
                                            if len(args) > 0:
                                                encoded = args[0].getString()
                                                decode = self.decode_string(encoded)
                                                # call_instruction.removeArgument(0)
                                                # call_instruction.insertArgument(0, self.cstbuilder.createString(decode))
                                                # instruction.setRight(self.cstbuilder.createString(decode))
                                                # print(
                                                #     "change in class: " + class_data.getName() + "->" + method_data.getName() + ": " + encoded)
                                                change += 1
                    else:
                        body = method_data.getBody()
                        for instruction in body:
                            if isinstance(instruction, IJavaCall):
                                if instruction.getMethod().getSignature() == self.method_sig:
                                    args = instruction.getArguments()
                                    if len(args) > 0:
                                        encoded = args[0].getString()
                                        decode = self.decode_string(encoded)
                                        # instruction.removeArgument(0)
                                        # instruction.insertArgument(0, self.cstbuilder.createString(decode))
                                        # print(
                                        #     "change in class: " + class_data.getName() + "->" + method_data.getName() + ": " + encoded)
                                        change += 1

                            if isinstance(instruction, IJavaAssignment):
                                call_instruction = instruction.getRight()
                                if isinstance(call_instruction, IJavaCall):
                                    if call_instruction.getMethod().getSignature() == self.method_sig:
                                        args = call_instruction.getArguments()
                                        if len(args) > 0:
                                            encoded = args[0].getString()
                                            decode = self.decode_string(encoded)
                                            # call_instruction.removeArgument(0)
                                            # call_instruction.insertArgument(0, self.cstbuilder.createString(decode))
                                            # # instruction.setRight(self.cstbuilder.createString(decode))
                                            # print(
                                            #     "change in class: " + class_data.getName() + "->" + method_data.getName() + ": " + encoded)
                                            change += 1

        print("total: " + str(total))
        print("change: " + str(change))

    def decode_string(self, encoded_string):
        # return encoded_string.replace("tanndd3", "")
        return encoded_string + "tandd3"
