from binaryninja import *
import pprint

from .Matchers.Tracelet_Matcher.Tracelet_Matching import *
from .Matchers.Tracelet_Matcher.Normalization_Techniques import *
from .Matchers.Tracelet_Matcher.Data_Types_and_Constants import *


def main(bv):
    function_list = []
    for f in bv:
        current_func = TracedFunction(f.medium_level_il)
        #current_func.pretty_print()
        #print('**********************************************************************')
        #print('**********************************************************************')
        #print('**********************************************************************')


PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
