from dice import d

race = 'Human'

# Ability Scores
limits = ((3,18),(3,18),(3,18),(3,18),(3,18),(3,18))
adjust = tuple([0]*6)

# Height
base_ht = (60,59)
mod_ht = d(10)*2

# Weight
base_wt = (140,100)
mod_wt = d(10)*6

# Age
base_age = 15
mod_age = d(4)
# Maximum Age
max_age = 90
for i in range(0,2):
    max_age += d(20)
# Middle Age
mdl_age = 45
# Old Age
old_age = 60
# Venerable Age
vnrbl_age = 90