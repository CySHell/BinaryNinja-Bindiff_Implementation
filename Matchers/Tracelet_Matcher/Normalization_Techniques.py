from bitstring import BitArray

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
    #print("IM IN MLIL_INSTRUCTION: ", mlil_instruction)
#    instruction_bit_rep = {
#        'Operations': operations,
#        'Operands': operands
#    }

    # a variable to track which field in the instruction_bit_rep we are currently populating
    parsing_stack = [mlil_instruction]

    def push_stack(obj_list):
        # add a list of objects to the stack for further parsing
        nonlocal parsing_stack
        #print("im in push_stack with: ", obj_list)
        for sub_obj in obj_list:
            parsing_stack.append(sub_obj)

    def add_operation(oper):
        # found an MLIL oper, add it to the bit representation.
        #nonlocal instruction_bit_rep
        nonlocal operations
        #print("im in add_operation with: ", oper)

        # < MediumLevelILOperation.MLIL_UNIMPL: 81 > unimplemented
        if oper.operation.value is not 81:
        #    instruction_bit_rep['Operations'].append(f'0b{oper.oper.value:07b}')
            operations.append(f'0b{oper.operation.value:07b}')

    def add_operand(var):
        # found an MLIL Operand, add its source type enum (register, stack var, flag etc) to bit repr.
        nonlocal operands
        #nonlocal instruction_bit_rep
        #print("im in add_operand with: ", var)
        #instruction_bit_rep['Operands'].append(f'0b{var.source_type.value:02b}')
        operands.append(f'0b{var.source_type.value:02b}')

    def unpack_il_instruction(instruction):
        nonlocal parsing_stack
        #print("im in unpack_il_instruction with: ", instruction)
        for sub_obj in instruction.prefix_operands:
            parsing_stack.append(sub_obj)

    def add_literal(_):
        nonlocal operands
        #nonlocal instruction_bit_rep
        #print("im in add_literal")
        #instruction_bit_rep['Operands'].append(f'0b{3:02b}')
        operands.append(f'0b{3:02b}')


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
        #print("Parsing stack: ")
        #print(parsing_stack)
        #print("to_parse: ")
        #print(to_parse, " ", type(to_parse))
        #print("bit_rep: ")
        #print(operations)
        parse_functions[str(type(to_parse))](to_parse)

    return operations, operands

########################################################################################################################
#                           list of normalization functions per IL_OPERATION                                           #
########################################################################################################################
