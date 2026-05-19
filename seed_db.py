import sqlite3

def seed_database():
    # Make sure this matches the actual name of your database file!
    # Common names might be 'jeopardy.db', 'game.db', or 'database.sqlite'
    db_name = 'jeopardy.db' 
    
    print(f"Connecting to {db_name}...")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    print("Reading seed.sql...")
    with open('seed.sql', 'r', encoding='utf-8') as file:
        sql_script = file.read()

    print("Executing SQL script...")
    cursor.executescript(sql_script)
    
    conn.commit()
    conn.close()
    
    print("✅ Database successfully wiped and seeded with the new categories!")

if __name__ == "__main__":
    seed_database()