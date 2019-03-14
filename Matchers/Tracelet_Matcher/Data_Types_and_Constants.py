from bitstring import BitArray
from . import Tracelet_Matching
import pprint
import hashlib


########################################################################################################################
#                                              DATA TYPES                                                              #
########################################################################################################################

class Tracelet:
    """
    Describes a single Tracelet (tuple of normalized MLIL basic blocks) as a series of mlil operations and
    operand types, represented as a bit stream.
    """
    def __init__(self):
        self.operations: BitArray = BitArray()
        self.operands: BitArray = BitArray()

    def add_operation(self, operation):
        print("Adding Operation: ", operation)
        self.operations.append(operation)

    def add_operands(self, operand):
        print("Adding Operands: ", operand)
        self.operands.append(operand)

    def add_string(self, string):
        # receive a python string and pack it into the operands bit stream.
        # This is useful for things like imported functions that have a symbol
        print("Adding string: ", string)
        for char in string:
            self.operands.append(BitArray(uint=int(ord(char)), length=7))


class TracedFunction:
    """
    Describes a single function
    """

    def __init__(self, mlil_function, tracelet_length = 3):
        """
        receives a mlil_function object and populates it with all Tracelet information.
        Returns the object
        :param mlil_function: (MLIL_FUNCTION) function to parse
        :param tracelet_length: (INT) how many basic blocks in a tracelet
        :return: sucess: (BOOLEAN) True if successful and False if failed to populate
        """
        self.tracelet_length: int = tracelet_length
        self.mlil_function = mlil_function
        self.bv = mlil_function.source_function.view
        # the name of the containing file
        self.filename: str = self.bv.file.filename
        # raw offset of the function in the containing file
        self.raw_file_offset: int = self.mlil_function.source_function.start - self.bv.start
        # md5 hash of the filename and raw_file_offset
        self.name = hashlib.md5((self.filename + str(self.raw_file_offset)).encode()).hexdigest()
        # a list of all Tracelet objects within the function
        self.tracelets: list = []
        # extract all tracelets from the function
        trace_list = Tracelet_Matching.extract_tracelets(self.mlil_function, tracelet_length)

        # populate the tracelets list with the normalized tracelets
        for TL in trace_list:
            tracelet = Tracelet_Matching.normalize_tracelet(TL)
            self.tracelets.append(tracelet)

        print("FINISHED DEFINING FUNCTION \n")

    def pretty_print(self):
        print("FUNCTION NAME: ", self.name)
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
