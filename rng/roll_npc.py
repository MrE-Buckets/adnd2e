import random as rand
import pandas as pd
from .roll_stats import mthd_npc
from .roll_vitals import get_vitals
from data.races import RACES
from data.campaign.tally_npc import export_npc_pop
from data.campaign import db_manager

def create_pop(count, gen_name):
    """Generates population and triggers Gated Summary/Database storage."""
    print(f"Generating {count} NPCs for '{gen_name}'...")
    headers = ['Race', 'Sex', 'Age', 'Weight', 'Height', 'Alignment', 'Stats', 'Tier lvl.', 'Tier', 'Death']
    npc_list = []

    for _ in range(count):
        raw_stats = mthd_npc()
        sum_pwr = sum(raw_stats)
        avg_pwr = round(sum_pwr / 6.0, 2)
        if avg_pwr >= 15.3: tier_name = "Hero"
        elif avg_pwr >= 12.8: tier_name = "Adventurer"
        elif avg_pwr >= 11.2: tier_name = "Elite"
        else: tier_name = "Commoner"
        val_races = [r for r in RACES if all(s <= high for s, (_, high) in zip(raw_stats, r.limits))]
        race = rand.choice(val_races) if val_races else RACES[0]
        r_name = "Half-Elf" if race.name.lower() == "half-elf" else race.name
        r_stats = [s + a for s, a in zip(raw_stats, race.adjust)]
        gender, age, height, weight, align, death_age = get_vitals(race)
        stats_string = f"[ {', '.join(str(s).zfill(2) for s in r_stats)} ]"        
        npc_list.append([f"{r_name}: ", gender, age, weight, height, align, stats_string, avg_pwr, tier_name, death_age])

    df = pd.DataFrame(npc_list, columns=headers)

    # 1. DATABASE (The Green Circle)
    db_manager.save_population_to_db(gen_name, df)

    # 2. SUMMARY (The Green Circle inside the folder)
    export_npc_pop(lists={gen_name: npc_list}, gen_name=gen_name, matrix={})

    return df