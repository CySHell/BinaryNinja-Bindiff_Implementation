import os

cwd = 'C:\\Program Files\\Vector35\\BinaryNinja'
path = 'C:\\Users\\user\\OneDrive\\Research Projects\\Binary Ninja - Bindiff implementation\\Factory\\'
os.chdir(path)
print(os.getcwd())
from .BnbFunction import BnbFunction
from .BnbBasicBlock import BnbBasicBlock
os.chdir(cwd)


#from BnbFunction import BnbFunction

function_list = []

for func in bv.functions:
    print(BnbFunction(func.mlil))
