from dice import d

race = 'Half-Elf'

# Ability Scores
limits = ((3,18),(6,18),(6,18),(4,18),(3,18),(3,18))
adjust = tuple([0]*6)

# Height
base_ht = (60,58)
mod_ht = d(6)*2

# Weight
base_wt = (110,85)
mod_wt = d(12)*3

# Age
base_age = 15
mod_age = d(6)
# Maximum Age
max_age = 125
for i in range(0,3):
    max_age += d(20)
# Middle Age
mdl_age = 62
# Old Age
old_age = 83
# Venerable Age
vnrbl_age = 125