import sqlite3
import os

def build_database():
    db_name = 'jeopardy.db'
    
    # 1. Delete the old database file entirely to prevent table conflicts
    if os.path.exists(db_name):
        os.remove(db_name)
        print("🗑️ Old database deleted.")
    
    print(f"Connecting to {db_name}...")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # 2. Build the new historical schema
    print("Building historical ledger schema...")
    with open('schema.sql', 'r', encoding='utf-8') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("✅ Database successfully built as a historical ledger!")

if __name__ == "__main__":
    build_database()