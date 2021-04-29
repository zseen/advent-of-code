from typing import Callable, Optional
import cProfile


def doProfiling(methodToCall: Callable, firstArgumentForMethod: Optional, secondArgumentForMethod: Optional) -> None:
    pr = cProfile.Profile()
    pr.enable()
    pr.runcall(methodToCall, firstArgumentForMethod, secondArgumentForMethod)
    pr.disable()
    pr.print_stats(sort='time')
