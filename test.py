from helping_f import helping_functions

# Here you can add a certain debug level, so that you are able to edit the comments which get called, if printd is higher than DEBUG_LEVEL, it gets printed, else it will be skipped.
DEBUG_LEVEL = 1

printd = helping_functions(DEBUG_LEVEL).printd

printd("This is a level 2 debug comment",2)
printd("This is a level 1 debug comment",1)
printd("This is a level 0 debug comment",0)