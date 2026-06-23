import sqlite3

def build_database():
    db_name = 'jeopardy.db'
    
    print(f"Connecting to {db_name}...")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # --- NEW: Build the structure first! ---
    print("Building schema...")
    with open('schema.sql', 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    # --- Fill it with data ---
    print("Seeding data...")
    with open('seed.sql', 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())
    
    conn.commit()
    conn.close()
    print("✅ Database successfully built and seeded!")

if __name__ == "__main__":
    build_database()