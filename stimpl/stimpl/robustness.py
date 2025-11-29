from stimpl.test import check_equal, check_run_result, check_program_raises
from stimpl.runtime import run_stimpl
from stimpl.types import *
from stimpl.expression import *


def run_stimpl_robustness_tests():
    program = Program(Assign(Variable("i"), IntLiteral(0)),
                      While(Lt(Assign(Variable("i"), Add(Variable("i"), IntLiteral(1))), IntLiteral(10)), 
                            Ren()))
                    
    run_value, run_type, run_state = run_stimpl(program)
    check_equal((10, Integer()), run_state.get_value("i"))
    print(f"The Test has passed")
    pass 
