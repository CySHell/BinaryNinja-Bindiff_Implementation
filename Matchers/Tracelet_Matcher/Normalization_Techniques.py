from bitstring import BitArray
from .Data_Types_and_Constants import *
from binaryninja import *

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
    symbols = BitArray()

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
        # undesired mlil operations mean the whole instruction is bad, do not parse the instruction.
        if op_enum in UNDESIRED_MLIL_OPERATIONS:
            un_parse_instruction()
        else:
            # calling a function from the import table
            # <MediumLevelILOperation.MLIL_IMPORT: 17>
            if op_enum is 17:
                if isinstance(mlil_instruction.dest, binaryninja.mediumlevelil.MediumLevelILInstruction):
                    import_addr = mlil_instruction.dest.value.value
                    add_symbol(mlil_instruction.function.source_function.view.get_symbol_at(import_addr))
                else:
                    if isinstance(mlil_instruction.dest, binaryninja.function.Variable):
                        add_operand(mlil_instruction.dest)
            else:
                operations.append(f'0b{op_enum:07b}')

    def add_operand(var):
        # found an MLIL Operand, add its source type enum to bit repr.
        nonlocal operands
        # StackVariableSourceType = 0
        # RegisterVariableSourceType = 1
        # FlagVariableSourceType = 2
        operands.append(f'0b{var.source_type.value:02b}')

    def unpack_il_instruction(instruction):
        nonlocal parsing_stack
        for sub_obj in instruction.prefix_operands:
            parsing_stack.append(sub_obj)

    def add_literal(_):
        nonlocal operands
        # Literal is encoded as enum 3 (binary 0b11)
        operands.append(f'0b11')

    def add_symbol(Symbol):
        """
        Receive a symbol and pack it into a bitstream
        :param Symbol: (Symbol) a binary ninja Symbol object
        """
        nonlocal symbols
        for char in Symbol.raw_name:
            symbols.append(BitArray(uint=int(ord(char)), length=7))

    def un_parse_instruction():
        nonlocal parsing_stack
        parsing_stack = []
        symbols.clear()
        operands.clear()
        operations.clear()

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

    return operations, operands, symbols

########################################################################################################################
#                           list of normalization functions per IL_OPERATION                                           #
########################################################################################################################
