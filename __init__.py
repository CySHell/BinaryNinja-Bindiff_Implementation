from binaryninja import *
from .Factory.BnbFunction import *



def main(bv):
    function_list = []
    for func in bv.functions:
        print(BnbFunction(func.mlil))


PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
