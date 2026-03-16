import os
import pandas as pd
from data.campaign.tally_npc import write_summary

def settlement_worker(args):
    """
    PARALLEL DISPATCHER: Unpacks the 6-tuple from campaign.py.
    Restores compatibility with the pool.map call.
    """
    df, campaign_name, settlement_name, low, high, path = args
    return create_settlement(df, campaign_name, settlement_name, low, high, path)

def create_settlement(df, campaign_name, settlement_name, low, high, final_path):
    """
    OPTIMIZED WORKER: Handles permanent CSV storage and Hero extraction.
    """
    os.makedirs(final_path, exist_ok=True)
    write_summary(df, settlement_name, final_path)
    # 1. PERMANENT CSV RECORD (Replaces settlement XLSX)
    csv_path = os.path.join(final_path, f"{settlement_name}.csv")
    df.to_csv(csv_path, index=False)

    # 2. HERO EXTRACTION (In-Memory)
    indices_to_blank = []
    hero_mask = df['Tier'].astype(str).str.strip() == "Hero"
    
    if hero_mask.any():
        hero_folder = os.path.join(final_path, "Heroes")
        os.makedirs(hero_folder, exist_ok=True)
        heroes_df = df[hero_mask]
        for idx, row in heroes_df.iterrows():
            clean_race = str(row.iloc[0]).strip().rstrip(':')
            filename = f"HERO_{clean_race}_{settlement_name}_Row-{idx+2}.txt"
            with open(os.path.join(hero_folder, filename), "w") as f:
                f.write(f"--- HERO CHARACTER SHEET ---\n")
                f.write(f"Settlement: {settlement_name} | Seed: {campaign_name}\n")
                f.write(f"Tier Level (Avg): {row.get('Tier lvl.', 'N/A')}\n")
                f.write("-" * 30 + "\n")
                for col_name, value in row.items():
                    f.write(f"{col_name}: {value}\n")
            indices_to_blank.append(idx)

    # 3. BLANKING & EXCEL SUMMARY
    # Blanks heroes so they don't count towards demographic totals
    if indices_to_blank:
        df.loc[indices_to_blank, :] = None
    

    print(f"Settled {len(df)} NPCs for {settlement_name}. (PID: {os.getpid()})")
    return df