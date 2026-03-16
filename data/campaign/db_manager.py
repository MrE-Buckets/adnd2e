import sqlite3
import os
import pandas as pd

def get_db_connection(gen_name):
    """Establishes a connection to the campaign's specific SQLite database."""
    db_path = f"data/campaign/{gen_name}/{gen_name}_global.db"
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
    ################
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON world_data(id)')
    ################
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
    Uses chunked deletion to avoid 'too many SQL variables' error.
    """
    conn = get_db_connection(gen_name)
    cursor = conn.cursor()
    
    # 1. Randomly select the IDs and data
    cursor.execute('''
        SELECT * FROM world_data 
        ORDER BY RANDOM() 
        LIMIT ?
    ''', (pop_size,))
    
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    
    if not rows:
        conn.close()
        return None

    # 2. Extract IDs for Surgical Blanking
    ids_to_remove = [row[0] for row in rows]
    
    # 3. Perform Chunked Surgical Blanking (Fix for 'too many SQL variables')
    # We use a chunk size of 999, well below the ~32k SQLite limit.
    chunk_size = 999
    for i in range(0, len(ids_to_remove), chunk_size):
        chunk = ids_to_remove[i : i + chunk_size]
        cursor.execute(f'''
            DELETE FROM world_data 
            WHERE id IN ({','.join(['?'] * len(chunk))})
        ''', chunk)
    
    conn.commit()
    conn.close()
    
    # Return as a DataFrame, removing 'id' for compatibility
    df_out = pd.DataFrame(rows, columns=columns).drop(columns=['id'])
    
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