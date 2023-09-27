import sys

import cmd_line_args as cmdla
from frames.dashboard_frame import DashboardFrame



def main():
    if len(sys.argv) > 1:
        cmdla.arg_check(sys.argv[1:])
    dashboard = DashboardFrame()



if __name__ == "__main__":
    main()