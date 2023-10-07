import json
from datetime import datetime
from typing import List,Tuple
from icecream import ic

from frames import constants as csts
from frames.utility import constants_dashboard as cdash





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

def calc_bmr(gender: str, weight_kg: float, height_cm: float, age: int) -> float:
    if gender == "Male" or gender == "male":
        return 66.5 + (13.75*weight_kg) + (5.003*height_cm) - (6.75*age)
    return 655.1 + (9.563*weight_kg) + (1.85*height_cm) - (4.676*age)

def calc_maintenance_rate(bmr: float,act_factor: float):
    return bmr*act_factor

"""
note that 1 lb =~ 3500 cals : note usually this overestimates weightloss
"""
def calc_rec_cals(maintcal: float,total_weight: float,goal_wt: float,in_numdays: int) -> int:
    weight_to_lose = total_weight - goal_wt
    cals_to_burn = weight_to_lose * 3500
    cals_to_burn_perday = cals_to_burn/in_numdays
    return round(maintcal - cals_to_burn_perday)


"""
Most guidelines recommend a weight loss of between 0.5 to 2.0 pounds or
1 to 2 percent of total bodyweight per week
im going to use 1 percent because, it is way to much using 2 percent.. also weird they say that 
bcs 1 percent of 200 is 2 pounds u would probs want these too things to align but the loss in 
pounds is way less than percent, so lets try 0.5 percent as a 200 pounder would then lose
one pound per week
"""

    # twopcnt_total = total_weight * 0.02
    # print(f"twopcnt: {twopcnt_total}")
    # #3500 cals per pound, div by seven to turn week loss into daily caloric def required
    # cal_def =  (twopcnt_total * 3500) / 7
    # print(f"cal def: {cal_def}")
    # print(f"maint - caldef : {maintcal} - {cal_def}")
    # return round(maintcal - cal_def)

#returns code to plans validity
#1 great, 2 somewhat aggressive, 3 aggressive, 4 not allowed
#1 - 85-115%, 2 - 65-85%, 3 - 50-65%, 4 - < 50% 
def check_calplan_validity(maintcal: float, cal_plan: int) -> (str,int):
    pcnt = cal_plan/maintcal
    if pcnt >= .85 and pcnt <= 1.15:
        return csts.CALPLAN_SVR1,1
    if (pcnt >= .60 and pcnt < .85) or (pcnt > 1.15 and pcnt <= 1.40):
        return csts.CALPLAN_SVR2,2
    if (pcnt >= .5 and pcnt < .60) or (pcnt > 1.40 and pcnt <= 1.5):
        return csts.CALPLAN_SVR3,3
    return csts.CALPLAN_SVR4,4

def calc_days_to_goal(maintcal: float, cal_plan:int, currweight: float, goalweight: float) -> int:
    weight_loss = currweight-goalweight
    cals_to_lose = weight_loss * 3500
    cal_def = maintcal - cal_plan
    return round(cals_to_lose/cal_def)

def get_weights_datetimes_fromjson(fname: str) -> Tuple[List[float],List[datetime]]:
    try:
        with open(fname, 'r',encoding='UTF-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("weight log file NOT FOUND")
        return ([-1],[-1])
    except json.JSONDecodeError:
        print("decoding weightlog error occurred, possibly because no weights have been logged")
        return ([-1],[-1])
    weights = []
    dates = []
    for date,weight in data.items():
        weights.append(weight)
        dates.append(datetime.strptime(date,"%m/%d/%Y"))
    return (weights,dates)

def get_calories_datetimes_fromjson(fname=cdash.CALORIESLOG_PATH) -> Tuple[List[float],List[datetime]]:
    try:
        with open(fname, 'r',encoding='UTF-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("weight log file NOT FOUND")
        return ([-1],[-1])
    except json.JSONDecodeError:
        print("decoding weightlog error occurred, possibly because no weights have been logged")
        return ([-1],[-1])
    calories = []
    dates = []
    for date,weight in data.items():
        calories.append(weight)
        dates.append(datetime.strptime(date,"%m/%d/%Y"))
    return (calories,dates)

def log_calories(calories: float,filename=cdash.CALORIESLOG_PATH) -> None:
    today = datetime.today()
    today = today.strftime("%m/%d/%Y")
    try:
        with open(filename, 'r',encoding='UTF-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {} #if file empty start with empty dictionary

    if today in data:
        data[today] += calories
    else:
        data[today] = calories

    # Write updated content back to file
    with open(filename, 'w',encoding='UTF-8') as file:
        json.dump(data, file,indent=4)

def check_todays_calories(filename=cdash.CALORIESLOG_PATH) -> float:
    today = datetime.today()
    today = today.strftime("%m/%d/%Y")
    try:
        with open(filename, 'r',encoding='UTF-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return 0.0

    if today in data:
        return data[today] #return todays calories
    return 0.0 #return 0, no cals been logged for today, must be first time opening app today

def log_food(servings,food_dict,fname=cdash.FOODLOG_PATH):
    def convert_servings(servings: str) -> (int,str):
        if servings == "":
            return 0,""
        num_str = ""
        char_to_app = ""
        for char in servings:
            if char.isnumeric() and char_to_app == "":
                num_str += char
            else:
                if char == " " and num_str != "" and char_to_app != "":
                    break
                char_to_app += char
        if num_str != "":
            return float(num_str),char_to_app
        else:
            return 0,""

    try:
        with open(fname, 'r',encoding='UTF-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {} #if file empty start with empty dictionary
    #key is exact time, so user can log food over and over, and get new logs;
    exact_time = datetime.today()
    exact_time = exact_time.strftime("%m/%d/%Y %H:%M:%S")

    #util fxn looks at the string for serving size for ex: 15oz -> then returns tuple(15.0,oz)
    amount_str,units = convert_servings(food_dict.get('servingsize',''))
    data[exact_time] = {
        'name': food_dict.get('name','unknown Name!'),
        'serving_size': food_dict.get('servingsize',0),
        'amount_total': str(amount_str * servings) + units,
        'calories': food_dict.get('energy_serving_kcal',0),
        'calories_total': food_dict.get('energy_serving_kcal',0)*servings,
        'protein': food_dict.get('proteins_serving',0),
        'protein_total': food_dict.get('proteins_serving',0)*servings,
        'fat': food_dict.get('fats_serving',0),
        'fat_total': food_dict.get('fats_serving',0)*servings,
        'carbs': food_dict.get('carbohydrates_serving',0),
        'carbs_total': food_dict.get('carbohydrates_serving',0)*servings,
        'sugars': food_dict.get('sugars_serving',0),
        'sugars_total': food_dict.get('sugars_serving',0)*servings

    }

    # Write updated content back to file
    with open(fname, 'w',encoding='UTF-8') as file:
        json.dump(data, file,indent=4)