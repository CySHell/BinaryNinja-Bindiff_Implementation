import pprint

class TraceletsFunc:
    """
    This class contains the aggregate information of all tracelets in the given MLIL function
    """

    def __init__(self, mlil_function, tracelet_block_limit):
        """
        :param mlil_function: (MLIL_FUNCTION) the function to extract tracelets from
        """
        self.func = mlil_function
        self.tracelet_list = []  # a list of Tracelet objects extracted from the function
        self.tracelet_count = 0  # amount of tracelets in the function
        self.tracelet_block_limit = tracelet_block_limit  # denotes how many MLIL basic_blocks compose a single tracelet

    def extract_tracelets(self):
        """
        extract all tracelets of length tracelet_length from the function
        :return: tracelet_count: (INT) amount of tracelets in the function
        """
        bb_in_func = self.func.basic_blocks
        length_bb_in_func = len(bb_in_func)

        if length_bb_in_func < self.tracelet_block_limit:
            # functions too small to extract tracelets
            self.tracelet_count = 0
            return 0

        for bb in bb_in_func:
            self._extract(bb, self.tracelet_block_limit, list())

        return self.tracelet_list

    def _extract(self, bb, curr_tracelet_len, temp_list):
        temp_list.append(bb)
        if curr_tracelet_len == 1 or not bb.outgoing_edges:
            tracelet_instruction_list = self._extract_instructions(temp_list)
            self.tracelet_list.append(list(tracelet_instruction_list))
            return
        else:
            for out_edge in bb.outgoing_edges:
                self._extract(out_edge.target, curr_tracelet_len - 1, temp_list)
                temp_list.pop()

    def _extract_instructions(self, temp_list):
        """
        receives a list of basic blocks that forms a tracelet, and extracts all the relevant instructions.
        removes the last instruction from any block, due to it probably being a control flow instruction.
        TODO: add a check for relevant IL_OP of control flow instructions, instead of just removing the last instruction
        :param temp_list: (LIST) a list of mlil basic blocks comprising the tracelet
        :return: (LIST) single list of all relevant instructions
        """
        instr_list = []
        temp = []
        for bb in temp_list:
            for index in range(bb.start, bb.end):
                # normalize the instruction tokens for comparison
                for token in self.func[index].tokens:
                    temp.append(self._normalize_token(str(token.value)))
            # remove the last instruction, it is probably a control flow instruction
                instr_list.append(temp)

            if instr_list:
                instr_list.pop()

        return instr_list

    def _normalize_token(self, token):
        """
        receives a token from an mlil instruction and normalizes it for comparison purposes
        :param token: (STR) the string to normalize
        :return: (STR): normalized form
        """

        # is the element in the instruction a hexdecimal literal? (i.e 0x43432534)
        if token.startswith('0x'):
            token = 'LITERAL'

        # remove traces of SSA form
        token = token.split('_')[0]

        return token

TL = TraceletsFunc(current_mlil, 4)
TL.extract_tracelets()
pprint.pprint(TL.tracelet_list[0])