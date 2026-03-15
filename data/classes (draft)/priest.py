from roll_dice import d, d8

def get_thaco(level):
    # Priests improve 2 per 3 levels (Table 53)
    # 1-3: 20, 4-6: 18, 7-9: 16...
    return 20 - (2 * ((level - 1) // 3))

def get_saves(level):
    if level <= 3:   return [10, 14, 13, 16, 15]
    if level <= 6:   return [9, 13, 12, 15, 14]
    if level <= 9:   return [7, 11, 10, 13, 12]
    if level <= 12:  return [6, 10, 9, 12, 11]
    if level <= 15:  return [4, 8, 7, 10, 9]
    if level <= 18:  return [2, 6, 5, 8, 7]
    return [1, 5, 4, 7, 6] # 19+

def roll_hp(level, con_bonus=0):
    hp = 0
    for i in range(min(level, 9)):
        hp += max(1, d8() + con_bonus)
    if level > 9:
        hp += (level - 9) * 2
    return hp

def get_bonus_spells(wisdom):
    # Returns [Level1, Level2, Level3, Level4...]
    bonus = {
        13: [1], 14: [2], 15: [2, 1], 16: [2, 2],
        17: [2, 2, 1], 18: [2, 2, 1, 1],
        19: [3, 2, 1, 2] # etc based on PHB Table 5
    }
    return bonus.get(wisdom, [0])