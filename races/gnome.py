from dice import d

race = 'Gnome'

# Ability Scores
limits = ((6,18),(3,18),(8,18),(6,18),(3,18),(3,18))
adjust = tuple([0]*4+[-1,1])

# Height
base_ht = (38,36)
mod_ht = d(6)

# Weight
base_wt = (72,68)
mod_wt = d(4)*5

# Age
base_age = 60
mod_age = d(12)*3
# Maximum Age
max_age = 200
for i in range(0,3):
    max_age += d(100)
# Middle Age
mdl_age = 100
# Old Age
old_age = 133
# Venerable Age
vnrbl_age = 200