from binaryninja import *
#from .Matchers.Tracelet_Matcher import Data_Types_and_Constants, Normalization_Techniques, Tracelet_Matching
from .Matchers.Tracelet_Matcher.Tracelet_Matching import *
from .Matchers.Tracelet_Matcher.Normalization_Techniques import *
from .Matchers.Tracelet_Matcher.Data_Types_and_Constants import *


def main(bv):
    for f in bv:
        trace_list = extract_tracelets(f.medium_level_il, 3)
        for TL in trace_list:
            print(normalize_instructions(TL))


PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
