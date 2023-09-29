from constants import USRINFO_PATH
from user_data.utility import utility_fxns as utils


class User():
    def __init__(self,usrinfo_path=USRINFO_PATH) -> None:
        #keys = {name(str),height(int inches),weight(int lbs),gender(str),birthday(str MM/DD/YYYY),goal_weight(int lbs)}
        self.user = utils.read_userjson(usrinfo_path=usrinfo_path) # DICTIONARY
        self.name = self.user.get('name',-1)
        self.weight = self.user.get('weight', -1)
        self.height = self.user.get('height', -1)
        self.gender = self.user.get('gender', '')
        self.birthday = self.user.get('birthday', '')
        self.goal_weight = self.user.get('goal_weight', -1)
        self.act_fct = self.user.get('activity_level', -1)
        self.height_cm = utils.calc_height_cm(height_in=self.height)
        self.weight_kg = utils.calc_weight_kg(weight_lbs=self.weight)
        self.bmi = utils.calc_bmi(weight=self.weight,height=self.height)
        self.age = utils.calc_age(self.birthday)
        self.bmr = utils.calc_bmr(gender=self.gender,weight_kg=self.weight_kg,height_cm=self.height_cm,age=self.age)
        self.maintenance_cal = utils.calc_maintenance_rate(bmr=self.bmr,act_factor=self.act_fct)
    
    def print_user_attributes(self):
        for name,value in vars(self).items():
            if not callable(value):
                print(f"{name}: {value}")
    
    def __repr__(self): #note could also use __str__ to overwrite, but repr is better for debug
        #bcs str should be used to return a cutesy string for the end user
        attrs = ", ".join(f"{name} : {value}" for name, value in vars(self).items() if not callable(value))
        return f"User({attrs})"

        