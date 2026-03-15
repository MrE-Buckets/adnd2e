import os
import pandas as pd
from data.campaign.tally_npc import export_npc_pop, apply_npc_styling

def settlement_worker(args):
    """Unpacks arguments for the multi-core pool."""
    df, campaign_name, settlement_name, low, high, path = args
    return create_settlement(df, campaign_name, settlement_name, low, high, path)

def create_settlement(df, campaign_name, settlement_name, low, high, kingdom_prime_path):
    """Takes pre-plucked NPCs from SQLite and extracts Heroes."""
    
    # Population size is now simply the length of the handed-off DataFrame
    settlement_df = df 
    pop_size = len(settlement_df)

    settlement_folder = os.path.join("data/campaign", campaign_name, settlement_name)
    os.makedirs(settlement_folder, exist_ok=True)

    # 1. Export the Settlement Excel Files
    export_npc_pop(
        lists={settlement_name: settlement_df.values.tolist()},
        gen_name=settlement_name, 
        matrix={}, 
        folder_path=settlement_folder
    )

    # 2. Hero Extraction
    prime_file = os.path.join(settlement_folder, f"{settlement_name}_Prime.xlsx")
    
    if os.path.exists(prime_file):
        final_df = pd.read_excel(prime_file, sheet_name=0)
        indices_to_blank = []

        for idx, row in final_df.iterrows():
            if str(row['Tier']).strip() == "Hero":
                hero_folder = os.path.join(settlement_folder, "Heroes")
                os.makedirs(hero_folder, exist_ok=True)
                
                clean_race = str(row.iloc[0]).strip().rstrip(':')
                filename_string = f"HERO_{clean_race}_{settlement_name}_Row-{idx+2}.txt"
                sheet_path = os.path.join(hero_folder, filename_string)
                
                with open(sheet_path, "w") as f:
                    f.write(f"--- HERO CHARACTER SHEET ---\n")
                    f.write(f"Settlement: {settlement_name}\n")
                    f.write(f"Tier Level (Avg): {row['Tier lvl.']}\n")
                    f.write("-" * 30 + "\n")
                    for col_name, value in row.items():
                        f.write(f"{col_name}: {value}\n")
                
                indices_to_blank.append(idx)

        # 3. Local Blanking
        if indices_to_blank:
            final_df.loc[indices_to_blank, :] = None
            with pd.ExcelWriter(prime_file, engine='xlsxwriter') as writer:
                final_df.to_excel(writer, sheet_name=settlement_name, index=False)
                apply_npc_styling(writer, settlement_name, final_df)

    print(f"Settled {pop_size} NPCs for {settlement_name}. Heroes moved to sub-folder.")
    return settlement_df