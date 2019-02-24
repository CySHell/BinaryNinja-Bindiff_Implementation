class BnbBasicBlock:
    """
    Holds all information regarding the Basic Block, and also how to extract the information
    """

    def __init__(self, basic_block):
        self._basic_block = basic_block

        # A dictionary defining all information to store about the given basic block
        self.bb_metadata = {
            'outgoing_edges': 0,
            'incoming_edges': 0,
            'imported_func_calls': [],  # list of imported functions called within the basic block
            'imported_func_count': 0,  # number of imported function calls
            'internal_func_calls': 0,  # number of internal function calls (funcs within the module)
            'dynamic_func_calls': 0,  # number of dynamic function calls (e.g 'call eax')
        }

        self.populate_metadata()


    def populate_metadata(self):
        """
        :return: (DICT) returns the basic block metadata object
        """

        self.bb_metadata['outgoing_edges'] = len(self._basic_block.outgoing_edges)
        self.bb_metadata['incoming_edges'] = len(self._basic_block.incoming_edges)

        for instruction in self._basic_block:
            # If the MLIL operation is a call instruction <MediumLevelILOperation.MLIL_CALL: 51>
            if instruction.operation.value == 51:
                # If it is a call to a constant <MediumLevelILOperation.MLIL_CONST_PTR: 14>
                if instruction.dest.operation == 14:
                    self.bb_metadata['internal_func_calls'] += 1
                # If it is a call to an imported function < MediumLevelILOperation.MLIL_IMPORT: 17 >
                else:
                    if instruction.dest.operation == 17:
                        self.bb_metadata['imported_func_count'] += 1
                        self.bb_metadata['imported_func_calls'].append(instruction.dest.tokens[0])
                    # It must be a dynamic call
                    else:
                        self.bb_metadata['dynamic_func_calls'] += 1

        return self.bb_metadata

    def __repr__(self):
        return str(self.bb_metadata)
