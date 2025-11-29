from typing import Any, Tuple, Optional

from stimpl.expression import *
from stimpl.types import *
from stimpl.errors import *

"""
Interpreter State
"""


class State(object):
    def __init__(self, variable_name: str, variable_value: Expr, variable_type: Type, next_state: 'State') -> None:
        self.variable_name = variable_name
        self.value = (variable_value, variable_type)
        self.next_state = next_state

    def copy(self) -> 'State':
        variable_value, variable_type = self.value
        return State(self.variable_name, variable_value, variable_type, self.next_state)

    def set_value(self, variable_name: str, variable_value: Expr, variable_type: Type):
        return State(variable_name, variable_value, variable_type, self)

    #This function takes in a variable name from the evaluate function and cycles through each state from the class until a variable is found that matches 
    #The variable's value is either returned or nothing at all 
    def get_value(self, variable_name: str) -> Any:
        """ TODO: Implement. """
       #checks if the given variable name matches with the the classes saved variable name 
        if(variable_name == self.variable_name):
            return self.value
        #Then if the next state is null then nothing is returned 
        if(self.next_state is None):
            return None
        #Moves to the next state to find a variable that matches with the given variable 
        return self.next_state.get_value(variable_name)

    def __repr__(self) -> str:
        return f"{self.variable_name}: {self.value}, " + repr(self.next_state)


class EmptyState(State):
    def __init__(self):
        pass

    def copy(self) -> 'EmptyState':
        return EmptyState()

    def get_value(self, variable_name: str) -> None:
        return None

    def __repr__(self) -> str:
        return ""


"""
Main evaluation logic!
"""
def evaluate(expression: Expr, state: State) -> Tuple[Optional[Any], Type, State]:
    match expression:
        case Ren():
            return ((), Unit(), state)

        case IntLiteral(literal=l):
            return (l, Integer(), state)

        case FloatingPointLiteral(literal=l):
            return (l, FloatingPoint(), state)

        case StringLiteral(literal=l):
            return (l, String(), state)

        case BooleanLiteral(literal=l):
            return (l, Boolean(), state)

        case Print(to_print=to_print):
            printable_value, printable_type, new_state = evaluate(
                to_print, state)

            match printable_type:
                case Unit():
                    print("Unit")
                case _:
                    print(f"{printable_value}")

            return (printable_value, printable_type, new_state)
        
        #This method type goes through each expression given in a "Sequence or Program" and returns the last expression' value, type and current state 
        #If no expression is found or is Ren then return none Unit() and state 
        case Sequence(exprs=exprs) | Program(exprs=exprs):
            """ TODO: Implement. """
            if not exprs:
                return (None, Unit(), state)

            current_state = state
            
            #cycles through each expression
            for expr in exprs:
                
                value, typ, current_state = evaluate(expr, current_state)

            if typ == Unit():
                return (None, Unit(), state)

                
            
            return (value, typ, current_state)

        case Variable(variable_name=variable_name):
            value = state.get_value(variable_name)
            if value == None:
                raise InterpSyntaxError(
                    f"Cannot read from {variable_name} before assignment.")
            # Now that we know the result from `get_value` is not None,
            # we can look at the (v, tau) pieces of `value` that we know
            # forms its return value.
            variable_value, variable_type = value
            return (variable_value, variable_type, state)

        case Assign(variable=variable, value=value):

            value_result, value_type, new_state = evaluate(value, state)

            variable_from_state = new_state.get_value(variable.variable_name)
            _, variable_type = variable_from_state if variable_from_state else (
                None, None)

            if value_type != variable_type and variable_type != None:
                raise InterpTypeError(f"""Mismatched types for Assignment:
            Cannot assign {value_type} to {variable_type}""")

            new_state = new_state.set_value(
                variable.variable_name, value_result, value_type)
            return (value_result, value_type, new_state)

        case Add(left=left, right=right):
            
            result = 0
            left_result, left_type, new_state = evaluate(left, state)
            right_result, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Add:
            Cannot add {left_type} to {right_type}""")

            match left_type:
                case Integer() | String() | FloatingPoint():
                    result = left_result + right_result
                case _:
                    raise InterpTypeError(f"""Cannot add {left_type}s""")

            return (result, left_type, new_state)

        #Separates an expression into two a left and right 
        #Each expression is evaulated and checked for type errors such as a type being a string 
        case Subtract(left=left, right=right):
            """ TODO: Implement. """

            result = 0
            left_result, left_type, new_state = evaluate(left,state)
            right_result, right_type, new_state = evaluate(right,new_state)
            if(left_type != right_type):
                raise InterpTypeError(f"Types are not compatible: Types have to be the same")

            match right_type:
                #The result is calculated by subtracting the left and right results 
                #And throws errors if the type is invalid 
                case Integer() | FloatingPoint():
                    result = left_result - right_result
                case Error:
                    raise InterpTypeError(f"""Cannot subtract {left_type}s""")
                
            return(result, left_type, new_state)
        
        #Separates an expression into two a left and right 
        #Each expression is evaulated and checked for type errors such as a type being a string 
        case Multiply(left=left, right=right):
            """ TODO: Implement. """
            result = 0
            left_result, left_type, new_state = evaluate(left,state)
            right_result, right_type, new_state = evaluate(right,new_state)
            if(left_type != right_type):
                raise InterpTypeError(f"Types are not compatible")
            
            match right_type:
                #The result is calculated by multiplying the left and right results 
                #And throws errors if the type is invalid 
                case Integer() | FloatingPoint():
                    result = left_result * right_result
                case Error:
                    raise InterpTypeError(f"""Cannot multiply {left_type}s""")
                
            return(result, left_type, new_state)
            
        #Separates an expression into two a left and right 
        #Each expression is evaulated and checked for type errors such as a type being a string 
        case Divide(left=left, right=right):
            """ TODO: Implement. """
            result = 0
            left_result, left_type, new_state = evaluate(left,state)
            right_result, right_type, new_state = evaluate(right,new_state)
            if(left_type != right_type):
               raise InterpTypeError(f"Types are not compatible")
            
            elif(right_result == 0):
                raise InterpMathError(f"Cannot divide by zero")
            match right_type:
                #The result is calculated by multiplying the left and right results 
                #And throws errors if the type is invalid 
                case Integer() | FloatingPoint():
                    result = left_result / right_result
                    if(left_result < right_result and right_type == Integer()):
                        result = 0
                case Error:
                    raise InterpTypeError(f"""Cannot divide {left_type}s""")
                
            return(result, left_type, new_state)
            

        case And(left=left, right=right):
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for And:
            Cannot evaluate {left_type} and {right_type}""")
            match left_type:
                case Boolean():
                    result = left_value and right_value
                case _:
                    raise InterpTypeError(
                        "Cannot perform logical and on non-boolean operands.")

            return (result, left_type, new_state)
        
        #Returns the result, type, and state
        case Or(left=left, right=right):
            """ TODO: Implement. """
            #gathers the left and right part of the expression and evualates their value, type and the new_state
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            #Checks for the type errors must be the same type 
            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for And:
            Cannot evaluate {left_type} and {right_type}""")
            match left_type:
                case Boolean():
                    result = left_value or right_value
                case error:
                    raise InterpTypeError("Cannot perform logical or on non-boolean operands.")

            return (result, left_type, new_state)
        #Takes in an expression that should be of a type boolean and flips the value 
        #Returns flipped value, type and the new state of the expression
        #If the expression is not type boolean then an error will be raised 
        case Not(expr=expr):
            """ TODO: Implement. """
            value, typ, new_state = evaluate(expr,state)
            if(typ == Boolean()):
                return(not value, typ, new_state)
            else:
                raise InterpTypeError("Invalid Type: Only accepts boolean")
            
        
        case If(condition=condition, true=true, false=false):
            """ TODO: Implement. """
            #Evaluates the condition to find whether it is true or false, type to check if boolean, and new state 
            condition_value, condition_type, new_state = evaluate(condition, state)

            if condition_type != Boolean():
                raise InterpTypeError("Invalid Type Operation")
            #Evaluates the result based off of the condition value 
            if condition_value == True:
                result_val, result_type, next_new_state = evaluate(true, new_state)
            else:
                result_val, result_type, next_new_state = evaluate(false, new_state)
            #Checks if result_type has a type (unit)
            if result_type == Unit():
                return(None, Unit(), None)
            return (result_val, result_type, next_new_state)
        
        case Lt(left=left, right=right):
            #Evaluates the left and right side of an expression giving values, types and the new state
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None
            #Makes sure the type is the same 
            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                #Makes sure the type is valid for operation
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value < right_value
                #The result will be an automatic false if the left_type is a Unit 
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform < on {left_type} type.")
            #Returns the result, type and the new state
            return (result, Boolean(), new_state)

        case Lte(left=left, right=right):
            """ TODO: Implement. """
            #Evaluates the left and right side of an expression giving values, types and the new state

            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None
            #Makes sure the type is the same 

            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                #Makes sure the type is valid for operation
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value <= right_value
                
                #The result will be an automatic false if the left_type is a Unit 
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(
                        f"Cannot perform <= on {left_type} type.")
            #Returns the result, type and the new state
            return (result, Boolean(), new_state)    

            

        case Gt(left=left, right=right):
            """ TODO: Implement. """
            #Evaluates the left and right side of an expression giving values, types and the new state
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            #Makes sure the type is the same 
            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                #Makes sure the type is valid for operation
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value > right_value
                #The result will be an automatic false if the left_type is a Unit 
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform > on {left_type} type.")
            #Returns the result, type and the new state
            return (result, Boolean(), new_state)
            

        case Gte(left=left, right=right):
            """ TODO: Implement. """
            #Evaluates the left and right side of an expression giving values, types and the new state

            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None
            #Makes sure the type is the same 
            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                #Makes sure the type is valid for operation
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value >= right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(
                        f"Cannot perform >= on {left_type} type.")
            #Returns the result, type and the new state
            return (result, Boolean(), new_state)
            

        case Eq(left=left, right=right):
            """ TODO: Implement. """
            #Evaluates the left and right side of an expression giving values, types and the new state
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None
            #Makes sure the type is the same 
            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                #Makes sure the type is valid for operation
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value == right_value
                case Unit():
                    result = True
                case _:
                    raise InterpTypeError(
                        f"Cannot perform == on {left_type} type.")
            #Returns the result, type and the new state
            return (result, Boolean(), new_state)
            

        case Ne(left=left, right=right):
            """ TODO: Implement. """
            #Evaluates the left and right side of an expression giving values, types and the new state            
            left_value, left_type, new_state = evaluate(left, state)
            right_value, right_type, new_state = evaluate(right, new_state)

            result = None

            #Makes sure the type is the same 
            if left_type != right_type:
                raise InterpTypeError(f"""Mismatched types for Lt:
            Cannot compare {left_type} and {right_type}""")

            match left_type:
                #Makes sure the type is valid for operation
                case Integer() | Boolean() | String() | FloatingPoint():
                    result = left_value != right_value
                case Unit():
                    result = False
                case _:
                    raise InterpTypeError(
                        f"Cannot perform != on {left_type} type.")
            
            #Returns the result, type and the new state
            return (result, Boolean(), new_state)
            

        case While(condition=condition, body=body):
            """ TODO: Implement. """
            #Evauluates the condition finding whether the condition is true or false
            #Must be type boolean for it to work....Will throw an error if the type is not boolean 
            condition_value, condition_type, new_state = evaluate(condition, state)
            if condition_type  != Boolean():
                raise InterpTypeError("Invalid type operation")
            #Runs a while loop while the condition is being 
            while condition_value:
                #Evaulates the body giving the variable value, type and new state
                variable_value, variable_type, new_state = evaluate(body, new_state)
                #checks whether the condition will still be true or false 
                condition_value, condition_type, new_state = evaluate(condition, new_state)
            #If the body is Ren then the condition value, its type and state is returned
            if(variable_type == Unit()):
                return(condition_value, Boolean(), new_state)

            return (variable_value, variable_type, new_state)

        case _:
            raise InterpSyntaxError("Unhandled!")
    pass


def run_stimpl(program, debug=False):
    state = EmptyState()
    program_value, program_type, program_state = evaluate(program, state)

    if debug:
        print(f"program: {program}")
        print(f"final_value: ({program_value}, {program_type})")
        print(f"final_state: {program_state}")

    return program_value, program_type, program_state
