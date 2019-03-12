from binaryninja import *
import pprint

#from .Matchers.Tracelet_Matcher import Data_Types_and_Constants, Normalization_Techniques, Tracelet_Matching
from .Matchers.Tracelet_Matcher.Tracelet_Matching import *
from .Matchers.Tracelet_Matcher.Normalization_Techniques import *
from .Matchers.Tracelet_Matcher.Data_Types_and_Constants import *


def main(bv):
    function_list = []
    for f in bv:
        function_metadata = Data_Types_and_Constants.TracedFunction()
        function_metadata.filename = bv.file.filename
        function_metadata.raw_file_offset = f.start - f.view.start

        trace_list = extract_tracelets(f.medium_level_il, 3)

        for TL in trace_list:
            tracelet = normalize_tracelet(TL)
            function_metadata.tracelets.append(tracelet)

        function_metadata.pretty_print()

PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
