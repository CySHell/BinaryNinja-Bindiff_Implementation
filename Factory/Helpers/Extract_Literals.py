# Ignores certain literals that are useless for similarity due to compiler
# dependence(e.g offset from register : [EAX + 0x8])
# TODO: determine the cases to avoid, avoiding all IF statements is not smart
# <MediumLevelILOperation.MLIL_LOAD: 4> <MediumLevelILOperation.MLIL_CMP_E: 59>
# <MediumLevelILOperation.MLIL_IF: 57>
operations_to_avoid = [4, 59, 57]

# <MediumLevelILOperation.MLIL_CONST: 13>
operations_indicating_literal = [13]

literals = {
    'int': [],
    'string': []
}


def extract_literals(mlil_instruction):
    """
    Recursively traverse the operands of the instruction and find any relevant literals.
    :param mlil_instruction: (MediumLevelILInstruction) the current instruction to scan
    :return: literals: (DICT) dictionary containing 2 keys: 'int' and 'string', each key's value is the corresponding list
    """

    recursive_search(mlil_instruction)
    return literals


def recursive_search(mlil_instruction):

    # first check if we received a valid mlil_instruction
    # TODO: find a better (more efficient) way to determine if the argument is indeed an mlil instruction
    try:
        op_val = mlil_instruction.operation.value
    except AttributeError:
        return None
    # some operations should be avoided for similarity search due to compiler differences
    if op_val in operations_to_avoid:
        return None
    else:
        if op_val in operations_indicating_literal:
            literal_val = mlil_instruction.value.value
            if type(literal_val) is int:
                literals['int'].append(literal_val)
            else:
                literals['string'].append(literal_val)
            return None
        else:
            # recursively check all operands of the current instruction
            for operand in mlil_instruction.operands:
                recursive_search(operand)
    return None
