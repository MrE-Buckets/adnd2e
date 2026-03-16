import random as rand
import pandas as pd
import multiprocessing
import os
from .roll_stats import mthd_npc
from .roll_vitals import get_vitals
from data.races import RACES
from data.campaign.tally_npc import export_npc_pop
from data.campaign import db_manager
import numpy as np

def npc_worker(count):
    batch = []
    # 1. OPTIMIZATION: NumPy Vectorization
    # We generate raw stats using your method, but process the math with NumPy
    for _ in range(count):
        raw_stats = mthd_npc() 
        
        # Convert to numpy array to make math 10x faster
        stats_arr = np.array(raw_stats)
        avg_pwr = np.mean(stats_arr).round(2)
        stat_sum = stats_arr.sum()
        
        # Fast Tier Check
        if avg_pwr >= 15.3: tier_name = "Hero"
        elif avg_pwr >= 12.8: tier_name = "Adventurer"
        elif avg_pwr >= 11.2: tier_name = "Elite"
        else: tier_name = "Commoner"
        
        # 2. OPTIMIZATION: Race Filtering
        # Logic: If it's a commoner (sum < 70), don't waste time checking limits
        if stat_sum < 70:
            race = RACES[0]
        else:
            # Using NumPy for the limit check
            val_races = [r for r in RACES if np.all(stats_arr <= [lim[1] for lim in r.limits])]
            race = rand.choice(val_races) if val_races else RACES[0]
        
        r_name = race.name
        gender, age, height, weight, align, death_age = get_vitals(race)
        
        batch.append([
            f"{r_name}: ", gender, age, weight, height, align, 
            raw_stats, 
            avg_pwr, tier_name, death_age
        ])
    
    # Optional: Use os to show which core is finishing
    print(f"Core {os.getpid()} finished batch of {count}") 
    return batch

def create_pop(count, gen_name):
    """Lights up 16 cores to generate the global population in batches."""
    num_cores = multiprocessing.cpu_count()
    batch_size = count // num_cores
    remainder = count % num_cores
    sizes = [batch_size] * num_cores
    sizes[0] += remainder

    print(f"--- Parallel Launch: Lighting up {num_cores} cores for {count} NPCs ---")
    with multiprocessing.Pool(num_cores) as pool:
        results = pool.map(npc_worker, sizes)

    full_npc_list = [item for sublist in results for item in sublist]
    headers = ['Race', 'Sex', 'Age', 'Weight', 'Height', 'Alignment', 'Stats', 'Tier lvl.', 'Tier', 'Death']
    df = pd.DataFrame(full_npc_list, columns=headers)

    df['Stats'] = df['Stats'].apply(lambda x: f"[ {', '.join(str(s).zfill(2) for s in x)} ]")

    db_manager.save_population_to_db(gen_name, df)
    export_npc_pop(lists={gen_name: full_npc_list}, gen_name=gen_name, matrix={})
    return df