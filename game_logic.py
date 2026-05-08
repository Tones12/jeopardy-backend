import sqlite3
import json
import datetime

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

    return board_data

# Collect player information and insert into SQL table. input is a list of players
def register_players(player_names):
    # Establish db connection
    connection = sqlite3.connect("jeopardy.db")
    cursor = connection.cursor()

    # Dictionary to store players and ids
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

# Function to create a game session
def create_game_session():
    # Initiate db connection
    connection = sqlite3.connect("jeopardy.db")
    cursor = connection.cursor()
    
    current_time = str(datetime.datetime.now())

    cursor.execute("INSERT INTO games (game_time) VALUES (?);", (current_time,))
    game_id = cursor.lastrowid

    cursor.execute("SELECT id FROM clues")
    clue_ids_results = cursor.fetchall()

    junction_data = []
    for row in clue_ids_results:
        clue_id = row[0]
        junction_data.append((game_id, clue_id))
    
    cursor.executemany(
         "INSERT INTO game_clue_state (game_id, clue_id) VALUES (?, ?);",
         junction_data
    )

    connection.commit()
    connection.close()

    print(f"Game Session {game_id} created succesfully")
    
    return game_id

# Function to record answers during a game
def record_answer(game_id, clue_id, player_id):
    # Initiate db connection
    connection = sqlite3.connect("jeopardy.db")
    cursor = connection.cursor()

    cursor.execute("UPDATE game_clue_state SET is_revealed = ?, answered_by_player_id = ? WHERE game_id = ? AND clue_id = ?;", (1, player_id, game_id, clue_id))
    
    connection.commit()
    connection.close()

    print(f"Success: Player {player_id} captured Clue {clue_id}!")
    return True

# Score calculation and table updates function
def calculate_scores(game_id):
    # Initiate db connection
    connection = sqlite3.connect("jeopardy.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    query = """
        SELECT
            players.player_name,
            SUM(clues.dollar_value) as total_score
        FROM game_clue_state
        JOIN players ON game_clue_state.answered_by_player_id = players.id
        JOIN clues ON game_clue_state.clue_id = clues.id
        WHERE game_clue_state.game_id = ?
        GROUP BY players.player_name
        ORDER BY total_score DESC;
        """
    cursor.execute(query, (game_id,))
    leaderboard_results = cursor.fetchall()
    
    print("\n--- FINAL JEOPARDY LEADERBOARD ---")
    if not leaderboard_results:
        print("No points on the board yet!")
    else:
        for row in leaderboard_results:
            name = row["player_name"]
            score = row["total_score"]
            print(f"{name}: ${score}")
    print("----------------------------------\n")
    
    connection.close()

    return leaderboard_results