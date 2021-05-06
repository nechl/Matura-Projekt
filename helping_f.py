class helping_functions:
    def __init__(self, debug_level):
        self.debug_level = debug_level

    def printd(self, msg, lvl=1):
        if lvl <= self.debug_level:
            print(msg)

DEBUG_LEVEL = 1
x = helping_functions(DEBUG_LEVEL)
x.printd("hi", 1)