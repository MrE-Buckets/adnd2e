from roll_dice import d, d6

def get_thaco(level):
    # Rogues improve 1 per 2 levels
    # 1-2: 20, 3-4: 19, 5-6: 18...
    return 20 - ((level - 1) // 2)

def get_saves(level):
    if level <= 4:   return [13, 14, 12, 16, 15]
    if level <= 8:   return [12, 12, 11, 15, 13]
    if level <= 12:  return [11, 10, 10, 14, 11]
    if level <= 16:  return [10, 8, 9, 13, 9]
    if level <= 20:  return [9, 6, 8, 12, 7]
    return [8, 4, 7, 11, 5] # 21+

def roll_hp(level, con_bonus=0):
    hp = 0
    # Cap is level 10
    for i in range(min(level, 10)):
        hp += max(1, d6() + min(con_bonus, 2)) # Rogues also capped at +2 Con bonus
    if level > 10:
        hp += (level - 10) * 2
    return hp

def get_base_skills():
    # PP, OL, FRT, MS, HS, DN, CW, RL
    return [15, 10, 5, 10, 5, 15, 60, 0]