from . import Data_Types_and_Constants, Normalization_Techniques


########################################################################################################################


def extract_tracelets(func, tracelet_length=3):
    """
    extract all tracelets of length tracelet_length from the function
    :param func: (MLIL_FUNCTION) the function to extract tracelets from
    :param tracelet_length: (INT) denotes how many MLIL basic_blocks compose a single tracelet
    :return: tracelet_list: (LIST) list of tracelets in the function. each list object includes
    """

    tracelet_list = []

    if len(func.basic_blocks) < tracelet_length:
        # functions too small to extract tracelets
        return tracelet_list

    for bb in func.basic_blocks:
        _, final_trace_list = define_tracelets(bb, tracelet_length, list(), list())
        for TL in final_trace_list:
            tracelet_list.append(TL)

    return tracelet_list


########################################################################################################################


def define_tracelets(bb, curr_tracelet_len, temp_list, final_list):
    """
    Parse all basic blocks in the function recursively and return a list of all tracelets of the given length.
    The list is of tuples of MLIL Basic Block objects consisting of a single tracelet.
    :param bb: (MLIL_BASIC_BLOCK) the current block being parsed
    :param curr_tracelet_len: (INT) A helper param for the recursion
    :param temp_list: (LIST) A helper param for recursion - holds the blocks in the current tracelet
    :param final_list: (LIST) A helper param for recursion - holds the tracelets so far
    :return: final_list: (LIST) a list of tuples, each tuple represents a single tracelet and denotes its bb's
    :return: temp_list: (LIST) this is only here for the purposes of the recursion
    """

    temp_list.append(bb)

    if curr_tracelet_len == 1 or not bb.outgoing_edges:
        final_list.extend([tuple(temp_list)])
        return temp_list, final_list
    else:
        for out_edge in bb.outgoing_edges:
            temp_list, final_list = define_tracelets(out_edge.target, curr_tracelet_len - 1, temp_list, final_list)
            temp_list.pop()
    return temp_list, final_list


########################################################################################################################


def normalize_tracelet(raw_tracelet):
    """
    receives a tracelet, extracts all the instructions from it and normalizes them.
    :param raw_tracelet: (tuple) a tuple containing the MLIL basic blocks of the tracelet, in descending order (pos[0]=root)
    :return: Tracelet object
    """
    tracelet = Data_Types_and_Constants.Tracelet()

    for bb in raw_tracelet:
        for instruction in bb:
            operations, operands = Normalization_Techniques.normalize_single_instruction(instruction)
            if operations and operands:
                tracelet.add_operation(operations)
                tracelet.add_operands(operands)

    return tracelet
