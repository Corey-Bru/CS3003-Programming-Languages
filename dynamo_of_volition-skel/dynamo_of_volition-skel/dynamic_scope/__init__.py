from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):
    #mapping is a dictionary that is passed through the class and is stored
    def __init__(self, mapping = None):
        self.env: Dict[str, Optional[Any]] = dict(mapping)
    #sets a new value within the dictionary    
    def __setItem__(self,key, val):
        self.env[key] = val 
    #checks if an item is in a dictionary and will raise an error if the value is not found within the dictionary
    def __getitem__(self, key):
        if key not in self.env:
            raise NameError(f"{key} not found")
        return self.env[key]
    #Iterates through the dictionaru
    def __iter__(self):
        return iter(self.env)
    #gives the length of the dictionary
    def __len__(self):
        return len(self.env)
    

#The purpose of this function is to isolate function pointers and populate the DynamicScope class
def get_dynamic_re() -> DynamicScope:
    #Creates an dictionary from the call stack 
    stack = inspect.stack()
    combined_locals = dict()

    #Iterates through each stack frame and stores the stack information in frame_info
    for frame_info in stack[1:]:
        #item = keys of f_locals within the stack frame
        for key in frame_info.frame.f_locals:
            #The if statement gets rid of function pointers and other things that are not strings
            if(type(frame_info.frame.f_locals.get(key)) == str):
                #Since the call stack is stored recursively this if statement will check the local variables in the function
                #call that was called last. Meaning if variable a = 3 intially but is modified in function1 to a = 1, then only a = 1 is 
                #stored in the dictionary
                if(key in combined_locals):
                    continue
                #logs the keys and their values in a dictionary 
                combined_locals[key] = frame_info.frame.f_locals.get(key)
            else:
                continue
    #passes through a dictionary into the dynamic scope class 
    return DynamicScope(combined_locals)
