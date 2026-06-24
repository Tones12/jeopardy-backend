-- 1. PLAYERS TABLE: A master list of everyone who has ever played
CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT UNIQUE NOT NULL
);

-- 2. GAMES TABLE: The master log of every game night session
CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    played_on DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. GAME RESULTS TABLE: The junction table linking the player, the game, and their score
CREATE TABLE game_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    player_id INTEGER,
    final_score INTEGER NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (player_id) REFERENCES players(id)
);