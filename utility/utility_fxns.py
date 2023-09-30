import os
import json


def is_firstrun(usrinfo_path):
    if os.path.exists(usrinfo_path) and os.path.getsize(usrinfo_path) > 0:
        try:
            with open(usrinfo_path,'r',encoding="UTF-8") as file:
                json.load(file)
        except json.JSONDecodeError: # catch when the file is corrup so values will be recalcced
            print(f"Error: {usrinfo_path} not valid json file or is corrup")
            return True
        except IOError as err_e: # also catch any other general IOError
            print(f"An I/O error occurred: {str(err_e)}")
            return True
        return False
    return True #if path doesnt exist, or is empty, then isfirstrun



def calc_default_wt(height: int, gender: str):
    wht = 0
    if gender == "Male":
        wht = 120 + 4.25 * (height - 60)
    else:
        wht = 115 + 4.05 * (height - 60)
    return round(wht)
