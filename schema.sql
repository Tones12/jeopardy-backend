CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE clues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER,
    clue_text TEXT NOT NULL,
    correct_response TEXT NOT NULL,
    dollar_value INTEGER NOT NULL,
    is_daily_double INTEGER DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL
);

CREATE TABLE games (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_time TEXT NOT NULL,
    current_round TEXT DEFAULT "Jeopardy"
);

CREATE TABLE game_clue_state (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER,
    clue_id INTEGER,
    is_revealed INTEGER DEFAULT 0,
    answered_by_player_id INTEGER,
    FOREIGN KEY (game_id) REFERENCES games(id),
    FOREIGN KEY (clue_id) REFERENCES clues(id),
    FOREIGN KEY (answered_by_player_id) REFERENCES players(id)
);