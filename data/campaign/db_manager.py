import sqlite3
import os
import pandas as pd

def get_db_connection(gen_name):
    """Establishes a connection to the campaign's specific SQLite database."""
    db_path = f"data/campaign/{gen_name}/{gen_name}_Globe.db"
    # Ensure directory exists before connecting
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def initialize_db(gen_name):
    """Creates the database and the world_data table if they don't exist."""
    conn = get_db_connection(gen_name)
    cursor = conn.cursor()
    
    # We mirror your 10-column structure exactly.
    # 'id' is used for the "Surgical Blanking" (DELETE) logic.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS world_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Race TEXT,
            Sex TEXT,
            Age TEXT,
            Weight TEXT,
            Height TEXT,
            Alignment TEXT,
            Stats TEXT,
            Tier_Lvl REAL,
            Tier TEXT,
            Death TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_population_to_db(gen_name, df):
    """
    Initializes the DB and streams a Pandas DataFrame into the SQL table.
    This replaces the 'Init.xlsx' and 'Prime.xlsx' logic at the Kingdom level.
    """
    initialize_db(gen_name)
    conn = get_db_connection(gen_name)
    
    # Map the DataFrame columns to match the SQLite table naming exactly
    # We rename 'Tier lvl.' (from your Excel) to 'Tier_Lvl' for SQL compatibility
    df_sql = df.copy()
    if 'Tier lvl.' in df_sql.columns:
        df_sql = df_sql.rename(columns={'Tier lvl.': 'Tier_Lvl'})
    
    df_sql.to_sql('world_data', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()

def pluck_settlement_pop(gen_name, pop_size):
    """
    Randomly selects NPCs for a settlement and deletes them from the global pool.
    This performs the 'Surgical Blanking' inside the database.
    """
    conn = get_db_connection(gen_name)
    cursor = conn.cursor()
    
    # 1. Randomly select the IDs and data for the requested population size
    cursor.execute('''
        SELECT * FROM world_data 
        ORDER BY RANDOM() 
        LIMIT ?
    ''', (pop_size,))
    
    rows = cursor.fetchall()
    
    # Get column names from the cursor description
    columns = [description[0] for description in cursor.description]
    
    if not rows:
        conn.close()
        return None

    # 2. Extract the IDs so we can delete them (Blanking)
    ids_to_remove = [row[0] for row in rows]
    
    # 3. Perform the Surgical Blanking
    cursor.execute(f'''
        DELETE FROM world_data 
        WHERE id IN ({','.join(['?'] * len(ids_to_remove))})
    ''', ids_to_remove)
    
    conn.commit()
    conn.close()
    
    # Return as a DataFrame, removing the internal 'id' column so roll_settlement is happy
    df_out = pd.DataFrame(rows, columns=columns).drop(columns=['id'])
    
    # Rename 'Tier_Lvl' back to 'Tier lvl.' so the Excel logic remains identical
    if 'Tier_Lvl' in df_out.columns:
        df_out = df_out.rename(columns={'Tier_Lvl': 'Tier lvl.'})
        
    return df_out

def get_global_counts(gen_name):
    """
    Queries the database to get counts for the Summary.xlsx.
    Replaces the heavy Pandas pivot_table logic.
    """
    conn = get_db_connection(gen_name)
    # Re-map names to match your Summary output expectations
    query = "SELECT Race, Tier, COUNT(*) as Count FROM world_data GROUP BY Race, Tier"
    summary_df = pd.read_sql_query(query, conn)
    conn.close()
    return summary_df