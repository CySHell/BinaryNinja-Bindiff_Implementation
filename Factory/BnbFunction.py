from .BnbBasicBlock import *


class BnbFunction:
    """
    A factory class for Bnb functions.
    This class encapsulates all metadata necessary to create the Bnb static signature for the functions.
    """

    def __init__(self, mlil_function):
        """
        :param mlil_function: (MediumLevelILFunction) Function to create a signature for
        """
        self._mlil_function = mlil_function
        self.function_features = {
            'basic_block_count': 0,  # number of basic blocks in the function
            'number_of_args': 0,  # number of function arguments. equals -1 if the function is variadic
            'bnb_basic_blocks': [],  # A list containing all BnbBasicBlock objects in the function
        }

        self.collect_features()

    def collect_features(self):
        """
        Populate the self.function_features dictionary
        """
        self.function_features['basic_block_count'] = len(self._mlil_function.basic_blocks)
        self.function_features['number_of_args'] = len(self._mlil_function.source_function.parameter_vars)
        self.function_features['bnb_basic_blocks'] = self.populate_basic_blocks()

    def populate_basic_blocks(self):
        """
        :return: (LIST) list of BnbBasicBlock objects contained within the given function
        """
        bb_object_list = []

        for basic_block in self._mlil_function:
            bnb_bb = BnbBasicBlock(basic_block)
            bb_object_list.append(bnb_bb)

        return bb_object_list

    def __repr__(self):
        return str(self.function_features)
