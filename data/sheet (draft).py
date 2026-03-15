import roll_dice as dice
import ability_tbls as tbl
# Specific class modules (thief.py, fighter.py, etc. should be in the same folder)

def get_class_module(class_name):
    # Standardizing naming to match your file structure
    mod_name = class_name.lower()
    try:
        return __import__(mod_name)
    except ImportError:
        return None

def resolve_hero_sheet(row_data):
    """
    Input: A row from your Excel [Race, Sex, Age, Weight, Height, Align, StatsTuple, Power, Tier, Class, Level]
    """
    race, sex, age, weight, height, align, stats, pwr, tier, class_name, level = row_data
    s, d, c, i, w, ch = stats
    
    cls_mod = get_class_module(class_name)
    
    # 1. Strength Resolution using your str_tbl logic
    # Check if Warrior Group for Exceptional Strength
    is_warrior = class_name.lower() in ['fighter', 'paladin', 'ranger', 'warrior']
    if s == 18 and is_warrior:
        exc_roll = dice.d100()
        str_input = (18, exc_roll)
        str_label = f"18/{exc_roll:02d}"
    else:
        str_input = s
        str_label = str(s)
    
    # Call your str_tbl from tables.py
    s_hit, s_dmg, s_wgt, s_prs, s_odr, s_bb = tbl.str_tbl(str_input)

    # 2. Other Ability Lookups
    reac_adj, msl_adj, def_adj = tbl.dex_tbl(d)
    hp_adj, sys_shk, res_srv, pois_sv, regen = tbl.con_tbl(c)
    lang, spl_lvl, chnc_lrn, max_spl, imm_int = tbl.int_tbl(i)
    mdef_adj, spl_fail, bonus_spl, spl_imm_wis = tbl.wis_tbl(w)
    max_hench, loyalty, react_adj = tbl.cha_tbl(ch)

    # 3. Class Math (From your class modules)
    thaco = cls_mod.get_thaco(level)
    saves = cls_mod.get_saves(level)
    hp = cls_mod.roll_hp(level, hp_adj)

    # 4. Format the "Named" Character Sheet
    dossier = f"""
================================================================================
AD&D 2E HERO DOSSIER: {race} {class_name} (Level {level})
================================================================================
STR: {str_label:<7} Hit Prob: {s_hit:+} | Dmg Adj: {s_dmg:+} | Max Press: {s_prs}
DEX: {d:<7} Reaction: {reac_adj:+} | Missile: {msl_adj:+} | Def Adj: {def_adj:+}
CON: {c:<7} HP Adj: {hp_adj:+} | Sys Shock: {sys_shk}% | Res Surv: {res_srv}%
INT: {i:<7} Languages: {lang} | Max Spell Lvl: {spl_lvl} | Learn: {chnc_lrn}%
WIS: {w:<7} Mag Def: {mdef_adj:+} | Spell Fail: {spl_fail}% | Bonus: {bonus_spl}
CHA: {ch:<7} Henchmen: {max_hench} | Loyalty: {loyalty:+} | Reaction: {react_adj:+}
--------------------------------------------------------------------------------
COMBAT STATS:
  HP: {hp} | THAC0: {thaco} | AC (Base): {10 + def_adj}
SAVING THROWS: 
  P/P: {saves[0]} | RSW: {saves[1]} | PP: {saves[2]} | BW: {saves[3]} | Spell: {saves[4]}
================================================================================
"""
    return dossier