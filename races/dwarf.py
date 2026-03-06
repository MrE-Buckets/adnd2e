from dice import d

race = 'Dwarf'

# Ability Scores
limits = ((8,18),(3,17),(11,18),(3,18),(3,18),(3,17))
adjust = (0,0,1,0,-1,0)

# Height
base_ht = (43,41)
mod_ht = d(10)

# Weight
base_wt = (130,105)
mod_wt = d(10)*4

# Age
base_age = 40
mod_age = d(6)*5
# Maximum Age
max_age = 250
for i in range(0,2):
    max_age += d(100)
# Middle Age
mdl_age = 125
# Old Age
old_age = 167
# Venerable Age
vnrbl_age = 250