import os
import pandas as pd
import random as rand
import multiprocessing
from rng import roll_npc, roll_settlement
from data.campaign import db_manager

def main():
    """
    High-Level Campaign Controller - SQLite Warehouse Edition.
    Integrated with Same-Name Conflict Prevention and Custom Seed Naming.
    """
    base_path = "data/campaign"
    os.makedirs(base_path, exist_ok=True)
    
    # 1. SEED PROMPT LOGIC
    seed_input = input("Generate seed: ").strip()
    if seed_input == "":
        seed_value = rand.randint(1000000, 9999999)
    else:
        # Convert to int if numeric string, else hash it for the RNG
        seed_value = hash(seed_input) if not seed_input.isdigit() else int(seed_input)
    
    rand.seed(seed_value)

    # 2. SAVE NAME & CONFLICT PREVENTION LOGIC
    while True:
        gen_name = input("Save seed as: ").strip()
        if gen_name == "":
            print("Error: Save name cannot be blank.")
            continue
            
        # Define the DB path early to check for existence
        campaign_folder = os.path.join(base_path, gen_name)
        db_file = os.path.join(campaign_folder, f"{gen_name}_Globe.db")

        if os.path.exists(db_file):
            print(f"\n--- CONFLICT DETECTED ---")
            print(f"A campaign database named '{gen_name}' already exists.")
            choice = input("Type 'LOAD' to use existing data, or 'NEW' to pick a different name: ").strip().upper()
            
            if choice == 'LOAD':
                is_new_campaign = False
                break
            else:
                print("Returning to name selection...")
                continue
        else:
            is_new_campaign = True
            break

    # 3. DIRECTORY AND SEED RECORD SETUP
    os.makedirs(campaign_folder, exist_ok=True)
    
    # Custom Seed File: {gen_name}_seed.txt
    seed_file_path = os.path.join(campaign_folder, f"{gen_name}_seed.txt")
    
    # Only write the seed file if it's a new campaign to preserve original history
    if is_new_campaign:
        with open(seed_file_path, "w") as f:
            content = seed_input if seed_input != "" else str(seed_value)
            f.write(content)

    # Setup the internal population folder for the Summary
    pop_folder = os.path.join(campaign_folder, "npc_population")
    os.makedirs(pop_folder, exist_ok=True)
    
    # Path for settlement_worker argument compatibility (Legacy _Prime path)
    path = os.path.join(pop_folder, f"{gen_name}_Prime.xlsx")

    # 4. DATA GENERATION / DB INITIALIZATION
    if is_new_campaign:
        pop_size = rand.randint(5000, 200000)
        print(f"Generating new campaign population: {pop_size}...")
        # roll_npc handles the save_population_to_db internally
        roll_npc.create_pop(pop_size, gen_name)
    else:
        print(f"Successfully loaded existing Warehouse: {db_file}")

    type_map = {
        "A":"Thorp", "B":"Hamlet", "C":"Village", "D":"Small Town", 
        "E":"Large Town", "F":"Small City", "G":"Large City", 
        "H":"Metropolis", "I":"Megalopolis"
    }

    tasks = []

    # 5. SETTLEMENT LOOP (SQLite "Pluck" Logic)
    # We loop until the DB is surgically blanked of all inhabitants
    while True:
        # Get current global population counts from DB
        summary_df = db_manager.get_global_counts(gen_name)
        pop_left = summary_df['Count'].sum()
        
        if pop_left == 0: 
            break

        full_ranges = {
            "A":(1,80), "B":(80,375), "C":(375,900), "D":(900,1850), 
            "E":(1850,4500), "F":(4500,10000), "G":(10000,24000), 
            "H":(24000,45000), "I":(45000,100000)
        }
        
        # Determine available settlement types based on remaining population
        available = [k for k, v in full_ranges.items() if pop_left >= v[0]]
        if not available:
            # If population is too small for a Thorp (unlikely but possible), break
            break
            
        picked = rand.choice(available)
        low, high = full_ranges[picked]
        
        # Determine target size for this specific settlement
        target_size = rand.randint(low, high)
        if pop_left < target_size: 
            target_size = int(pop_left)
        
        # SURGICAL BLANKING: Extract and DELETE the chunk from the DB
        set_chunk = db_manager.pluck_settlement_pop(gen_name, target_size)
        
        if set_chunk is None or set_chunk.empty:
            break
            
        set_num = len(tasks) + 1
        name = f"Set.{set_num}-{type_map[picked]}"
        
        # Package data for Multiprocessing Pool
        tasks.append((set_chunk, gen_name, name, low, high, path))

    # 6. MULTIPROCESSING
    if tasks:
        print(f"Processing {len(tasks)} settlements across {multiprocessing.cpu_count()} cores...")
        
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            print(f"--- Distribution Complete ---")
            print(f"Total Settlements Planned: {len(tasks)}")
            print(f"Starting Multi-Processor Pool...")
            pool.map(roll_settlement.settlement_worker, tasks)
    else:
        print("No settlements to process.")

    print(f"\nSQLite Campaign '{gen_name}' processing complete.")

if __name__ == "__main__":
    main()