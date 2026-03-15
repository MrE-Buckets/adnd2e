from roll_dice import d, d10, d100

def get_thaco(level):
    # Warriors improve 1 per level: Level 1=20, 2=19... 20=1
    return max(1, 21 - level)

def get_saves(level):
    # PPD, RSW, PP, BW, Spells
    if level <= 2:   return [14, 16, 15, 17, 17]
    if level <= 4:   return [13, 15, 14, 16, 16]
    if level <= 6:   return [11, 13, 12, 13, 14]
    if level <= 8:   return [10, 12, 11, 12, 13]
    if level <= 10:  return [8, 10, 9, 9, 11]
    if level <= 12:  return [7, 9, 8, 8, 10]
    if level <= 14:  return [5, 7, 6, 5, 8]
    if level <= 16:  return [4, 6, 5, 4, 7]
    return [3, 5, 4, 4, 6] # 17+

def roll_hp(level, con_bonus=0):
    hp = 0
    # Roll d10 for first 9 levels
    for i in range(min(level, 9)):
        hp += max(1, d10() + con_bonus)
    # +3 flat for every level above 9
    if level > 9:
        hp += (level - 9) * 3
    return hp

def roll_exceptional_strength():
    # Only for Warriors with STR 18
    return d100()