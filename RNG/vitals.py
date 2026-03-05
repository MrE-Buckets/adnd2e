from .dice import d
from . import basics as roll
from .abl_scrs import stats as new

raceID = d(6)-1
race = roll.race(raceID)
genderID = d(2)-1
gender = roll.gender(genderID)
alignID = (d(3)-1,d(3)-1)
alignment = roll.alignment(alignID[0],alignID[1])
age = roll.age(raceID)
height = roll.height(raceID,genderID)
weight = roll.weight(raceID,genderID)
# Stats
stats = new(raceID)

char = [race,gender,alignment,age,height,weight,stats]