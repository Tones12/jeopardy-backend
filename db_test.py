import sqlite3

connection = sqlite3.connect("jeopardy.db")
connection.row_factory = sqlite3.Row 

cursor = connection.cursor()
cursor.execute("SELECT * FROM clues;")

results = cursor.fetchall()

print("--- Jeopardy Clues ---")
for row in results:
    clue = row["clue_text"]
    response = row["correct_response"]
    value = row["dollar_value"]
    
    print(f"For ${value}: {clue}")
    print(f"Answer: {response}")
    print("-" * 20)

connection.close()