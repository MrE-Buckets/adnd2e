from dice import d

race = 'Elf'

# Ability Scores
limits = ((3,18),(6,18),(7,18),(8,18),(3,18),(8,18))
adjust = tuple([0,1,-1]+[0]*3)

# Height
base_ht = (55,50)
mod_ht = d(10)

# Weight
base_wt = (90,70)
mod_wt = d(10)*3

# Age
base_age = 100
mod_age = d(6)*5
# Maximum Age
max_age = 350
for i in range(0,4):
    max_age += d(100)
# Middle Age
mdl_age = 175
# Old Age
old_age = 233
# Venerable Age
vnrbl_age = 350