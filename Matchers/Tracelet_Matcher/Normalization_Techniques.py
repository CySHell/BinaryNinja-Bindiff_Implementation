from bitstring import BitArray
from .Data_Types_and_Constants import *

########################################################################################################################
#                           SINGLE INSTRUCTION NORMALIZATION TECHNIQUES                                                #
########################################################################################################################
"""
Create a variable length BitArray representing the current insutrction's normalized state.
a normalized state strips away variable names, and only leaves operation enum and var source type enum.
"""


def normalize_single_instruction(mlil_instruction):
    operations = BitArray()
    operands = BitArray()

    parsing_stack = [mlil_instruction]

    def push_stack(obj_list):
        # add a list of objects to the stack for further parsing
        nonlocal parsing_stack
        for sub_obj in obj_list:
            parsing_stack.append(sub_obj)

    def add_operation(oper):
        # found an MLIL oper, add it to the bit representation.
        nonlocal operations

        op_enum = oper.operation.value
        #if op_enum in UNDESIRED_MLIL_OPERATIONS:
        #    return None, None
        # calling a function from the import table
        # <MediumLevelILOperation.MLIL_IMPORT: 17>
        #if op_enum is 17:
        #    oper.tokens[0]
        print("add operation: ", oper, " ",op_enum)
        operations.append(f'0b{op_enum:07b}')

    def add_operand(var):
        # found an MLIL Operand, add its source type enum to bit repr.
        nonlocal operands
        # StackVariableSourceType = 0
        # RegisterVariableSourceType = 1
        # FlagVariableSourceType = 2
        print("add operand: ", var, " ", var.source_type.value)
        operands.append(f'0b{var.source_type.value:02b}')

    def unpack_il_instruction(instruction):
        nonlocal parsing_stack
        for sub_obj in instruction.prefix_operands:
            parsing_stack.append(sub_obj)

    def add_literal(_):
        nonlocal operands
        # Literal is encoded as enum 3 (binary 0b11)
        print("Adding LITERAL")
        operands.append(f'0b11')


    parse_functions = {
        "<class 'binaryninja.mediumlevelil.MediumLevelILInstruction'>": unpack_il_instruction,
        "<class 'binaryninja.mediumlevelil.MediumLevelILOperationAndSize'>": add_operation,
        "<type 'list'>": push_stack,
        "<class 'list'>": push_stack,
        "<class 'binaryninja.function.Variable'>": add_operand,
        "<type 'long'>": add_literal,
        "<class 'int'>": add_literal,
    }

    while parsing_stack:
        to_parse = parsing_stack.pop()
        parse_functions[str(type(to_parse))](to_parse)

    return operations, operands

########################################################################################################################
#                           list of normalization functions per IL_OPERATION                                           #
########################################################################################################################
