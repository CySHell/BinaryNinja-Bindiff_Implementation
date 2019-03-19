from binaryninja import *
from .Matchers.Tracelet_Matcher.Data_Types_and_Constants import *
import threading


def main(bv):

    thread_count = 0

    for f in bv:
        current_func = TracedFunction(f.medium_level_il)
        if current_func.is_not_empty():
            t = threading.Thread(target=current_func.dump_to_db)
            t.start()
            thread_count += 1
            if thread_count == 16:
                t.join()
                thread_count = 0




PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
