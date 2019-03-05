
class TraceletsFunc:
    """
    This class contains the aggregate information of all tracelets in the given MLIL function
    """

    def __init__(self, mlil_function):
        """
        :param mlil_function: (MLIL_FUNCTION) the function to extract tracelets from
        """
        self.func = mlil_function
        self.tracelet_list = []         # a list of Tracelet objects extracted from the function
        self.tracelet_count = 0         # amount of tracelets in the function

    def extract_tracelets(self, tracelet_blocks):
        """
        extract all tracelets of length tracelet_length from the function
        :param tracelet_blocks: (INT) denotes how many MLIL basic_blocks compose a single tracelet
        :return: tracelet_count: (INT) amount of tracelets in the function
        """
        bb_in_func = self.func.basicblocks
        length_bb_in_func = len(bb_in_func)

        if length_bb_in_func < tracelet_blocks:
            # functions too small to extract tracelets
            self.tracelet_count = 0
            return 0

        for bb in bb_in_func:
            self.tracelet_list.append(self.build_tracelet(bb))

    def build_tracelet(self,bb):

class Tracelet:
    """
    This Class represents a single Tracelet
    """

    def __init__(self, bb, tracelet_block_count):
        """
        :param bb: (MLIL_BASIC_BLOCK) basic block starting the tracelet
        :param tracelet_block_count: (INT) how many blocks in the tracelet
        """
        self.tracelet_block_count = tracelet_block_count
        self.tracelet_blocks = [bb]
        self._build_trace()


    def _build_tracelet(self):
        sucess = self.tracelet_block_count
        for index in range(self.tracelet_block_count):
            for outgoing_edges in self.tracelet_blocks[-1]
            self.tracelet_block_count -= 1

