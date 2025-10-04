from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect

def test():
    a = "hello"
    b = "world"
    c = "outerworld"
    def inside3():
        a = "Actually erm there is a world"
        print(dyn())
    def inside():
        a = "world"
        b = "hello"
        def inside2():
            d = "FUck this assignment"
            lit = "ughhhhhh"
            a = "No World is left anymore"
            inside3()
        inside2()
    inside()

def dyn():
     stack = inspect.stack()
     
     combined_locals = dict()

    # Iterate over all frames except dyn() itself
     for frame_info in stack[1:]:
        #item = keys of r_locals within the stack frame
        for key in frame_info.frame.f_locals:
            print(type(frame_info.frame.f_locals.get(key)))
            if(type(frame_info.frame.f_locals.get(key)) == str):
                if(key in combined_locals):
                    continue
                #print(key)
                if(type(frame_info.frame.f_locals.get(key)) == FunctionType):
                    print(frame_info.frame.f_locals.get(key))
                combined_locals[key] = frame_info.frame.f_locals.get(key)
            else:
                continue

     return combined_locals

if __name__ == "__main__":
    test()    