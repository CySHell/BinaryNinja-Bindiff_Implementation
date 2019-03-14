from binaryninja import *
import pprint

from .Matchers.Tracelet_Matcher.Tracelet_Matching import *
from .Matchers.Tracelet_Matcher.Normalization_Techniques import *
from .Matchers.Tracelet_Matcher.Data_Types_and_Constants import *


def main(bv):
    function_list = []
    for f in bv:
        current_func = TracedFunction(f.medium_level_il)
        if current_func.is_empty():
#            current_func.dump_to_file('C:\\Users\\user\\Downloads\\test.txt')
            current_func.pretty_print()



PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
