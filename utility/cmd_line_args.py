from typing import List

# results = [rrflag,...]
def arg_check(args : List):
    results = [False for _ in range(len(args))]
    for arg in args:
        if arg == "-rr":
            results[0] = True
    return results