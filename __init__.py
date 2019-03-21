from binaryninja import *
from .Matchers.Tracelet_Matcher.Data_Types_and_Constants import *
from queue import Queue
from collections import deque
from threading import Thread


def main(bv):

    que = Queue()
    threads_list = list()

    for f in bv:
        t = Thread(target=lambda q, arg1: q.put(TracedFunction(arg1)), args=(que, f.medium_level_il))
        t.start()
        threads_list.append(t)

    for t in threads_list:
        t.join()

#    function_objects = list()
    thread_count = 0

#    while not que.empty():
#        function_objects.append(que.get().dump_to_db())

    while not que.empty():
        t = Thread(target=que.get().dump_to_db)
        t.start()
        thread_count += 1
        if thread_count == 16:
            t.join()
            thread_count = 0




PluginCommand.register("BNB - BinDja", "BNB - Bindiff Implementation for Binja", main)
