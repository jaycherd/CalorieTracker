import os
import json
from datetime import datetime
from typing import Dict, Optional

from constants import USRINFO_PATH
from frames.constants import ACTLVL_OP1,ACTLVL_OP2,ACTLVL_OP3,ACTLVL_OP4,ACTLVL_OP5,ACTLVL_OP6,ACTLVL_OP7
from user_data.utility import constants_user as csts



def calc_age(bday: str):
    birthdate = datetime.strptime(bday,"%m/%d/%Y")
    today = datetime.today()
    age=today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    #note 2nd subtraction is to make sure that if birthday hasnt happened yet wont add to age
    return age

def calc_bmi(weight: int, height: int) -> float:
    return (weight / (height * height)) * 703

def calc_height_cm(height_in: int) -> float:
    return height_in * 2.54

def calc_weight_kg(weight_lbs: float) -> float:
    return weight_lbs*0.453

def calc_bmr(gender: str, weight_kg: int, height_cm: float, age: int) -> float:
    if gender == "Male" or gender == "male":
        return 66.5 + (13.75*weight_kg) + (5.003*height_cm) - (6.75*age)
    return 655.1 + (9.563*weight_kg) + (1.85*height_cm) - (4.676*age)
    #     return 10*weight + 6.25*height_cm - 5*age + 5
    # return 10*weight + 6.25*height_cm - 5*age - 161

def read_userjson(usrinfo_path=USRINFO_PATH) -> Optional[Dict]:
    if os.path.exists(usrinfo_path) and os.path.getsize(usrinfo_path) > 0:
        try:
            with open(usrinfo_path,'r',encoding="UTF-8") as file:
                return json.load(file)
        except json.JSONDecodeError: # catch when the file is corrup so values will be recalcced
            print(f"Error: {usrinfo_path} not valid json file or is corrup")
        except IOError as err_e: # also catch any other general IOError
            print(f"An I/O error occurred: {str(err_e)}")
    else:
        raise ValueError(f"File Path: {USRINFO_PATH} does not exist")
    return None

def convert_actlvl_toint(actlvl_str: str) -> float:
    op1 = 1.2
    op2 = 1.45
    op3 = 1.725
    op4 = 1.9
    string_num_mapping = {
        ACTLVL_OP1: op1,
        ACTLVL_OP2: op2,
        ACTLVL_OP3: op3,
        ACTLVL_OP4: op4,
        ACTLVL_OP5: (op1+op2)/2,
        ACTLVL_OP6: (op2+op3)/2,
        ACTLVL_OP7: (op3+op4)/2
    }
    return string_num_mapping.get(actlvl_str,-1)

def calc_maintenance_rate(bmr: float,act_factor: float):
    return bmr*act_factor


def generate_usrinfo_json(usr_info: Dict, usrinfopath=USRINFO_PATH):
    # [optional] auto generate goal weight with online recc
    with open(usrinfopath,'w',encoding='UTF-8') as file:
        json.dump(usr_info,file)

def log_weight(weight: float,filename=csts.WEIGHTLOG_PATH) -> None:
    today = datetime.today()
    today = today.strftime("%m/%d/%Y")
    try:
        with open(filename, 'r',encoding='UTF-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # Define new entry
    new_entry = {today: weight}

    # Append new entry to data
    data.append(new_entry)

    # Write updated content back to file
    with open(filename, 'w',encoding='UTF-8') as file:
        json.dump(data, file)