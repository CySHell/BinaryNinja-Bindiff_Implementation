from binaryninja import *
from bindiff.BnbFunction import *



def main(bv):
    function_list = []
    path = 'C:\\Users\\user\\Downloads\\BNB_output.txt'

    for func in bv.functions:
        function_list.append(BnbFunction(func.mlil))

    with open(path,'w') as file:
        file.write(str(function_list))

PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
