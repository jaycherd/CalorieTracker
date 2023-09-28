import os
import json
from datetime import datetime


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
    

def generate_usrinfo_json(name: str,height: int, weight: int, gender: str,
                          birthday: str,goal_weight: int,usrinfopath: str):
    # [optional] auto generate goal weight with online recc
    usr_info = {
        "name": name,
        "height": height,
        "weight": weight,
        "gender": gender,
        "birthday": birthday,
        "goal_weight": goal_weight
    }
    with open(usrinfopath,'w',encoding='UTF-8') as file:
        json.dump(usr_info,file)


def calc_default_wt(height: int, gender: str):
    wht = 0
    if gender == "Male":
        wht = 120 + 4.25 * (height - 60)
    else:
        wht = 115 + 4.05 * (height - 60)
    return round(wht)

def calc_age(bday: str):
    birthdate = datetime.strptime(bday,"%m/%d/%Y")
    today = datetime.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    #note 2nd subtraction is to make sure that if birthday hasnt happened yet wont add to age
    return age

def calc_bmi(weight: int, height: int):
    return (weight / (height * height)) * 703


