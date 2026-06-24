import sqlite3
import random
import api_client

def generate_board(round_name="Jeopardy"):
    """
    Calls the API client for raw data, applies game rules (Daily Doubles),
    and formats it into the exact dictionary Pygame expects.
    """
    print(f"⚙️ [Game Logic] Formatting the board for {round_name}...")
    
    # 1. Ask the API client to go get the data
    board_data = api_client.fetch_board_data(round_name)
    
    if not board_data:
        print("⚠️ [Game Logic] Warning: API returned empty board data.")
        return {}

    # 2. Extract a flat list of all clues so we can pick Daily Doubles
    all_clues_list = []
    for cat_name, clues in board_data.items():
        all_clues_list.extend(clues)
    
    # 3. Apply the Daily Double Rules
    if all_clues_list and round_name != "Final Jeopardy":
        num_daily_doubles = 2 if round_name == "Double Jeopardy" else 1
        
        # Safely pick random unique clues (making sure we don't pick mare than exist
        safe_sample_size = min(num_daily_doubles, len(all_clues_list))
        daily_doubles = random.sample(all_clues_list, safe_sample_size)
        
        for clue in daily_doubles:
            clue['is_daily_double'] = True

    return board_data

def save_game_results(player_scores, registered_players):
    """
    Saves the final scores to our SQLite Historical Ledger.
    Resolves temporary slot IDs to permanent, unique human user profiles.
    """
    print("💾 Saving final results to the historical ledger...")
    connection = sqlite3.connect("jeopardy.db")
    cursor = connection.cursor()

    # 1. Open a pristine log entry for this game night session
    cursor.execute("INSERT INTO games DEFAULT VALUES;")
    game_id = cursor.lastrowid

    # 2. Iterate over the tactical slot dictionary
    for player_num, score in player_scores.items():
        # Match slot index against web-server session registrations
        # Default safely to generic identifier if a chair was empty
        player_name = registered_players.get(player_num, f"Player {player_num}")

        # SQLite handles thread safety & structural deduplication natively via UNIQUE constraint
        cursor.execute("INSERT OR IGNORE INTO players (player_name) VALUES (?);", (player_name,))
        
        # Pull down the validated identity primary key
        cursor.execute("SELECT id FROM players WHERE player_name = ?;", (player_name,))
        player_id = cursor.fetchone()[0]

        # Populate relational junction ledger
        cursor.execute("""
            INSERT INTO game_results (game_id, player_id, final_score)
            VALUES (?, ?, ?);
        """, (game_id, player_id, score))

    connection.commit()
    connection.close()
    
    print("✅ Game results successfully archived!")
    return True