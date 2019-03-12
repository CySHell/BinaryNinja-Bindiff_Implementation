from recordclass import RecordClass
from bitstring import BitArray
import pprint


########################################################################################################################
#                                              DATA TYPES                                                              #
########################################################################################################################

class Tracelet(RecordClass):
    """
    Describes a single Tracelet (tuple of normalized MLIL basic blocks) as a series of mlil operations and
    operand types, represented as a bit stream.
    """
    operations: BitArray = BitArray()
    operands: BitArray = BitArray()

    def add_operation(self, operation):
        self.operations.append(operation)

    def add_operands(self, operand):
        self.operands.append(operand)

    def add_string(self, string):
        # receive a python string and pack it into the operands bit stream.
        # This is useful for things like imported functions that have a symbol
        for char in string:
            self.operands.append(BitArray(uint=int(ord(char)), length=7))


class TracedFunction(RecordClass):
    """
    Describes a single function
    """
    raw_file_offset: int = None  # raw offset of the function in the containing file
    filename: str = ''  # the name of the containing file
    name: str = ''  # hash of the filename and raw_file_offset
    tracelets: list = []  # a list of all Tracelet objects within the function

    def pretty_print(self):
        for tracelet in self.tracelets:
            print("OPERATIONS: ")
            pprint.pprint(tracelet.operations)
            print("OPERANDS: ")
            pprint.pprint(tracelet.operands)


########################################################################################################################
#                                              CONSTANTS                                                               #
########################################################################################################################
REGISTER_NAMES = set()

X86_REGISTER_NAMES = {'eax', 'ebx', 'ecx', 'edx', 'edi', 'esi', 'ebp', 'esp', 'eip'}
REGISTER_NAMES.update(X86_REGISTER_NAMES)

# MLIL_IF = 57 , MLIL_UNIMPL: 81, MLIL_UNIMPL_MEM = 82, MLIL_JUMP = 48, MLIL_JUMP_TO = 49
UNDESIRED_MLIL_OPERATIONS = {81, 57, 82, 48, 49}
