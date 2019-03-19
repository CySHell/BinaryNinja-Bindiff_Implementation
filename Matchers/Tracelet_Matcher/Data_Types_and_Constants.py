from typing import Set
from bitstring import BitArray
from . import Tracelet_Matching, DB
import pprint
import xxhash


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
        self.symbols: BitArray = BitArray()
        self._hash = xxhash.xxh32()
        self.hash = 0

    def add_operation(self, operation):
        self.operations.append(operation)
        self._hash.update(operation.tobytes())
        self.hash = self._hash.intdigest()

    def add_operands(self, operand):
        self.operands.append(operand)
        self._hash.update(operand.tobytes())
        self.hash = self._hash.intdigest()

    def add_symbol(self, symbol):
        # receive a python string and pack it into the operands bit stream.
        # This is useful for things like imported functions that have a symbol
        self.symbols.append(symbol)
        self._hash.update(symbol.tobytes())
        self.hash = self._hash.intdigest()


class TracedFunction:
    """
    Describes a single function
    """

    def __init__(self, mlil_function, tracelet_length=3):
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
        # TODO: decide on a naming convention for functions
        self.name = self.filename
        # a list of all Tracelet objects within the function
        self.tracelets: list = []
        # extract all tracelets from the function
        trace_list = Tracelet_Matching.extract_tracelets(self.mlil_function, tracelet_length)

        # populate the tracelets list with the normalized tracelets
        for TL in trace_list:
            tracelet = Tracelet_Matching.normalize_tracelet(TL)
            self.tracelets.append(tracelet)

    def pretty_print(self):
        print("FUNCTION NAME: ", self.name)
        for index in range(len(self.tracelets)):
            print("INSTRUCTION index #", index)
            print("OPERATIONS: ")
            pprint.pprint(self.tracelets[index].operations)
            print("OPERANDS: ")
            pprint.pprint(self.tracelets[index].operands)
            print("SYMBOLS: ")
            pprint.pprint(self.tracelets[index].symbols)

    def dump_to_db(self):
        """
        :return: success: (BOOLEAN) True if successfully inserted, otherwise False.
        """
        driver = DB.init_db()
        DB.populate_traced_function(self, driver)

    def is_not_empty(self):
        """
        check if the function is populated with relevant tracelets
        :return: sucess: (BOOLEAN)
        """
        if self.tracelets:
            return True
        else:
            return False


########################################################################################################################
#                                              CONSTANTS                                                               #
########################################################################################################################
REGISTER_NAMES = set()

X86_REGISTER_NAMES = {'eax', 'ebx', 'ecx', 'edx', 'edi', 'esi', 'ebp', 'esp', 'eip'}
REGISTER_NAMES.update(X86_REGISTER_NAMES)

# MLIL_IF = 57 , MLIL_UNIMPL: 81, MLIL_UNIMPL_MEM = 82, MLIL_JUMP = 48, MLIL_JUMP_TO = 49
UNDESIRED_MLIL_OPERATIONS: Set[int] = {81, 57, 82, 48, 49}
