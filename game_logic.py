import sqlite3
import json

# Game board generation function, grabs categories and clues from SQL database and formats for the game
def generate_board():
    # Set up connection to SQL database
    connection = sqlite3.connect("jeopardy.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    
    # Master game board dictionary
    board_data = {}

    # Fetch all categories
    cursor.execute("SELECT * FROM categories;")
    categories_results = cursor.fetchall()

    # Loop through each category
    for category_row in categories_results:
        # Grab category variables for this category
        cat_id = category_row["id"]
        cat_title = category_row["title"]

        # Fetch clues for this category
        cursor.execute("SELECT * FROM clues WHERE category_id = ? ORDER BY dollar_value", (cat_id,))
        clues_results = cursor.fetchall()

        # Unpack SQLite rows into python list of dictiories
        clean_clues_list = []
        for clue_row in clues_results:
            clean_clue = {
                "value": clue_row["dollar_value"],
                "clue": clue_row["clue_text"],
                "answer": clue_row["correct_response"]
            }
            clean_clues_list.append(clean_clue)

        # Attach cleaned clues list to master dictionary under their category
        board_data[cat_title] = clean_clues_list
    
    connection.close()

    print(json.dumps(board_data, indent=4))

    return board_data

# Collect player information and insert into SQL table. input is a list of players
def register_players(player_names):
    connection = sqlite3.connect("jeopardy.db")
    cursor = connection.cursor()

    registered_data = {}

    for name in player_names:
        cursor.execute("INSERT INTO players (player_name) VALUES (?);", (name,))

        assigned_id = cursor.lastrowid

        registered_data[name] = assigned_id

    connection.commit()
    connection.close()

    print("Players successfully registered:")
    print(json.dumps(registered_data, indent = 2))

    return registered_data

generate_board()

register_players(['Brittany', 'Anna', 'Alex', 'Tony'])
