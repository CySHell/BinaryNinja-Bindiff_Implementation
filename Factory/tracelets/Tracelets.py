import itertools


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
            self.tracelet_list.extend(self._extract(bb))

    def _extract(self, bb):
        curr_tracelet_len = self.tracelet_block_limit
        print(bb)
        if curr_tracelet_len == 1 or bb.outgoing_edges is None:
            return [bb]
        else:
            for out_edge in bb.outgoing_edges:
                return itertools.product([bb], self._extract(out_edge.target))


print(TraceletsFunc(current_mlil, 3).extract_tracelets())
