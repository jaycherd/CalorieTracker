from dataclasses import dataclass
from typing import Optional

from constants import USRINFO_PATH
from user_data.utility import utility_fxns as utils

"""
"height_cm": 170.18, "weight_kg": 67.95, "bmi": 23.49075517932724, "age": 23, "bmr": 1696.97304, "maintenance_cal": 2460.610908, "cal_plan": 2198}
"""

@dataclass
class User():
    #all this is done, so that static analysis of code knows dynamically set attributes
    name: Optional[str] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    goal_weight: Optional[int] = None
    activity_level: Optional[int] = None
    goal_days: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bmi: Optional[float] = None
    age: Optional[int] = None
    bmr: Optional[float] = None
    maintenance_cal: Optional[float] = None
    cal_plan: Optional[int] = None

    def __init__(self,usrinfo_path=USRINFO_PATH) -> None:
        #keys = {name(str),height(int inches),weight(int lbs),gender(str),birthday(str MM/DD/YYYY),goal_weight(int lbs)}
        user_dict = utils.read_userjson(usrinfo_path=usrinfo_path) # DICTIONARY
        #below is some dope code to DYNAMICALLY set user attributes and name them after the dictionary key, giving value that corresponds to the key
        for key,value in user_dict.items():
            setattr(self,key,value)
    
    def print_user_attributes(self):
        for name,value in vars(self).items():
            if not callable(value):
                print(f"{name}: {value}")
    
    def __repr__(self): #note could also use __str__ to overwrite, but repr is better for debug
        #bcs str should be used to return a cutesy string for the end user
        attrs = ", ".join(f"{name} : {value}" for name, value in vars(self).items() if not callable(value))
        return f"User({attrs})"

        