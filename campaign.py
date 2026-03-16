import os
import pandas as pd
import random as rand
import multiprocessing
from rng import roll_npc, roll_settlement, roll_dice as d
from data.campaign import db_manager
from data.campaign.tally_npc import write_summary
from datetime import datetime

def main():
    """
    High-Level Campaign Controller - SQLite Warehouse Edition.
    Baseline Version: Pure Random Plucking (No Weights).
    """
    base_path = "data/campaign"
    os.makedirs(base_path, exist_ok=True)
    
    # # 1. SEED PROMPT LOGIC
    # seed_input = input("Generate seed: ").strip()
    # if seed_input == "":
    #     seed_value = rand.randint(1000000, 9999999)
    # else:
    #     seed_value = hash(seed_input) if not seed_input.isdigit() else int(seed_input)
    
    # rand.seed(seed_value)

    # 1. SEED PROMPT LOGIC
    seed_input = input("Generate seed: ").strip()
    if seed_input == "":
        seed_value = "%010X" % rand.randint(0, 0xFFFFFFFFFF)
    elif seed_input.isdigit():
        seed_value = int(seed_input)
    else:
        seed_value = seed_input
    
    rand.seed(seed_value)

    # 2. SAVE NAME & CONFLICT PREVENTION LOGIC
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    gen_name = f"{timestamp}.{seed_value}"
    campaign_folder = os.path.join(base_path, gen_name)
    pop_folder = os.path.join(campaign_folder, "npc_population")
    os.makedirs(pop_folder, exist_ok=True)
    print(f"\n----------------------------")
    print(f"{gen_name}")
    print(f"----------------------------\n")

    # 4. DATA GENERATION / DB INITIALIZATION
    # if is_new_campaign:
    global_pop = rand.randint(100000, 1000000)
    print(f"--- GENERATING GLOBAL POPULATION: {global_pop} ---")
    roll_npc.create_pop(global_pop, gen_name)
    
    num_continents = d.d6()
    num_countries = [max(1, d.d8()) for _ in range(num_continents)]
    total_world_countries = sum(num_countries)

    excess_pop = global_pop - total_world_countries
    cut_points = sorted(rand.choices(range(0, excess_pop + 1), k=total_world_countries - 1))
    full_cuts = [0] + cut_points + [excess_pop]
    all_country_pops = [(full_cuts[i+1] - full_cuts[i]) + 1 for i in range(total_world_countries)]

    countries_by_continent = []
    pop_index = 0
    for count in num_countries:
        countries_by_continent.append(all_country_pops[pop_index : pop_index + count])
        pop_index += count
    
    type_map = {
        "A":"Thorp", "B":"Hamlet", "C":"Village", "D":"Small Town", 
        "E":"Large Town", "F":"Small City", "G":"Large City", 
        "H":"Metropolis", "I":"Megalopolis"
    }
    global_census_data = []
    tasks = []
        
    for cont_idx, continent in enumerate(countries_by_continent):
        if not continent: continue
        
        continent_tag = f"LND.{"%05X" % rand.randint(0, 0xFFFFF)}"
        continent_path = os.path.join(campaign_folder, continent_tag)
        os.makedirs(continent_path, exist_ok=True)

        # FIXED: Removed 'seed_value + cont_idx' argument
        cont_pop_total = sum(continent)
        cont_df = db_manager.pluck_settlement_pop(gen_name, cont_pop_total)
        write_summary(cont_df, f"{gen_name}_{continent_tag}", continent_path)

        for country_idx, country_pop_size in enumerate(continent):
            country_tag = f"NAT.{"%04X" % rand.randint(0, 0xFFFF)}"
            country_path = os.path.join(continent_path, country_tag)
            os.makedirs(country_path, exist_ok=True)
            
            # FIXED: We pluck directly from the continent DataFrame pool randomly
            country_df = cont_df.sample(n=min(len(cont_df), country_pop_size))
            cont_df = cont_df.drop(country_df.index) # Surgical Blanking
            
            print(f"--- Processing {country_tag} (Pop: {country_pop_size}) ---")
            write_summary(country_df, f"{gen_name}_{country_tag}", country_path)
            global_census_data.append(country_df)

            # LEVEL 3: SETTLEMENT PLUCK
            while not country_df.empty:
                pop_left = len(country_df)
                full_ranges = {
                    "A":(1,80), "B":(81,375), "C":(376,900), "D":(901,1850), 
                    "E":(1851,4500), "F":(4501,10000), "G":(10001,24000), 
                    "H":(24001,45000), "I":(45001,100000)
                }
                available = [k for k, v in full_ranges.items() if pop_left >= v[0]]
                if not available: break
                
                picked = rand.choice(available)
                low, high = full_ranges[picked]
                target_size = min(pop_left, rand.randint(low, high))
                
                set_num = len(tasks) + 1
                
                # FIXED: Simple random sample from country DataFrame
                set_chunk = country_df.sample(n=target_size)
                country_df = country_df.drop(set_chunk.index)
                
                # set_name = f"SET.{set_num}-{type_map[picked]}"
                set_hex = "%03X" % set_num 
                set_name = f"SET.{set_hex}-{type_map[picked]}"
                tasks.append((set_chunk, gen_name, set_name, low, high, os.path.join(country_path, set_name)))

    # 5. MULTI-PROCESSING EXECUTION
    if tasks:
        core_count = multiprocessing.cpu_count()
        worker_count = max(1, core_count - 1) 
        
        print(f"--- Launching Engine: {len(tasks)} tasks on {worker_count}/{core_count} cores ---")
        def settlement_generator(all_tasks):
            for task in all_tasks:
                yield task
        
        with multiprocessing.Pool(processes=worker_count) as pool:
            for _ in pool.imap_unordered(roll_settlement.settlement_worker, settlement_generator(tasks)):
                pass
                
        print("\n--- Campaign Generation Complete ---")
    else:
        print("No settlements found in tasks list.")

    # 6. GLOBAL FINALIZATION
    if global_census_data:
        print(f"Finalizing Master Summary for {gen_name}...")
        final_global_df = pd.concat(global_census_data)
        write_summary(final_global_df, gen_name, pop_folder)

    print(f"\nSQLite Campaign '{gen_name}' processing complete.")

if __name__ == "__main__":
    main()