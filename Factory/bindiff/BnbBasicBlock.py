from Helpers.Prime_product_Hash import *
from Helpers.Extract_Literals import *


class BnbBasicBlock:
    """
    Holds all information regarding the Basic Block, and also how to extract the information
    """

    def __init__(self, basic_block):
        self._basic_block = basic_block
        self._function = basic_block.function
        # A dictionary defining all information to store about the given basic block
        self.bb_metadata = {
            'outgoing_edges': 0,
            'incoming_edges': 0,
            'imported_func_calls': [],  # list of imported functions called within the basic block
            'imported_func_count': 0,  # number of imported function calls
            'internal_func_calls': 0,  # number of internal function calls (funcs within the module)
            'dynamic_func_calls': 0,  # number of dynamic function calls (e.g 'call eax')
            'mlil_prime_sum': 0,  # each mlil operation is assigned a prime number, this is the sum of numbers
            # in the current basic block. The sum is agnostic to the arrangment of the
            # operations by the compiler\assembler.
            'int_literals': [],  # list of integer literals found within this basic block
            'string_literals': [],  # list of string literals found within this basic block
        }

        self.populate_metadata()

    def populate_metadata(self):
        """
        :return: (DICT) returns the basic block metadata object
        """

        self.bb_metadata['outgoing_edges'] = len(self._basic_block.outgoing_edges)
        self.bb_metadata['incoming_edges'] = len(self._basic_block.incoming_edges)

        # This loop iterates over all instructions in the basic block.
        # Each iteration extract multiple features from the instruction, capable of serving
        # different matching strategies.
        for instruction in self._basic_block:
            operation_type = instruction.operation.value

            # If the MLIL operation is a call instruction <MediumLevelILOperation.MLIL_CALL: 51>
            if operation_type == 51:
                # If it is a call to a constant <MediumLevelILOperation.MLIL_CONST_PTR: 14>
                if operation_type == 14:
                    self.bb_metadata['internal_func_calls'] += 1
                # If it is a call to an imported function < MediumLevelILOperation.MLIL_IMPORT: 17 >
                else:
                    if operation_type == 17:
                        self.bb_metadata['imported_func_count'] += 1
                        self.bb_metadata['imported_func_calls'].append(instruction.dest.tokens[0])
                    # It must be a dynamic call
                    else:
                        self.bb_metadata['dynamic_func_calls'] += 1

            self.bb_metadata['mlil_prime_sum'] += prime_mlil_enum[operation_type]

            self.bb_metadata['string_literals'] = extract_literals(instruction)['string']
            self.bb_metadata['int_literals'] = extract_literals(instruction)['int']

        return self.bb_metadata

    def __repr__(self):
        return str(self.bb_metadata)
