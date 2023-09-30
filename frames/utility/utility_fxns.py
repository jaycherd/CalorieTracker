from datetime import datetime

from frames import constants as csts





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
