from dice import d

race = 'Halfling'

# Ability Scores
limits = ((7,18),(7,18),(10,18),(6,18),(3,17),(3,18))
adjust = tuple([-1,1]+[0]*4)

# Height
base_ht = (32,30)
mod_ht = d(8)*2

# Weight
base_wt = (52,48)
mod_wt = d(4)*5

# Age
base_age = 20
mod_age = d(4)*3
# Maximum Age
max_age = 100
for i in range(0,1):
    max_age += d(100)
# Middle Age
mdl_age = 50
# Old Age
old_age = 67
# Venerable Age
vnrbl_age = 100