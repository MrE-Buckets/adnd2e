from roll_dice import d, d4

def get_thaco(level):
    # Wizards improve 1 per 3 levels
    # 1-3: 20, 4-6: 19, 7-9: 18...
    return 20 - ((level - 1) // 3)

def get_saves(level):
    if level <= 5:   return [14, 11, 13, 15, 12]
    if level <= 10:  return [13, 9, 11, 13, 10]
    if level <= 15:  return [11, 7, 9, 11, 8]
    if level <= 20:  return [10, 5, 7, 9, 6]
    return [8, 3, 5, 7, 4] # 21+

def roll_hp(level, con_bonus=0):
    hp = 0
    # Cap is level 10 for Wizards
    for i in range(min(level, 10)):
        hp += max(1, d4() + min(con_bonus, 2)) # Note: Wizards capped at +2 Con bonus
    if level > 10:
        hp += (level - 10) * 1
    return hp

def get_int_limits(intelligence):
    # Returns (MaxSpellLevel, LearnSpell%, MaxSpellsPerLevel)
    limits = {
        9:  (4, 35, 6),  10: (5, 40, 7),  11: (5, 45, 7),
        12: (6, 50, 7),  13: (6, 55, 9),  14: (7, 60, 9),
        15: (7, 65, 11), 16: (8, 70, 11), 17: (8, 75, 14),
        18: (9, 85, 18), 19: (9, 95, 99)
    }
    return limits.get(intelligence, (0, 0, 0))