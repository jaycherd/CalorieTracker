import sys
import datetime as dt

from frames.dashboard_frame import DashboardFrame
from frames.firstrun_frame import FirstRunFrame
import utility.cmd_line_args as cmdla
import utility.utility_fxns as utils
import constants as csts


def main():
    cmdla_res = None
    if len(sys.argv) > 1:
        # results = [rrflag,...]
        cmdla_res = cmdla.arg_check(sys.argv[1:])

    # if -rr or isfirstrun then need to generate json for user info: height,weight,etc.
    if (cmdla_res and cmdla_res[0] is True) or utils.is_firstrun(usrinfo_path=csts.USRINFO_PATH):
        fr_frame = FirstRunFrame()
        utils.generate_usrinfo_json(name="JC",height=5*12 + 11,weight=210,gender="male",birthday="11/20/1996",goal_weight=195,usrinfopath=csts.USRINFO_PATH)
        # utils.generate_usrinfo()
    dashboard = DashboardFrame()



if __name__ == "__main__":
    main()