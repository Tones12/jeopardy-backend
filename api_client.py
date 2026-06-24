import json
import random
import os

def fetch_board_data(round_name, num_categories=5):
    """
    Simulates an API request by reading a local JSON dataset.
    Filters the massive dataset down to the specific round and formats it.
    """
    print(f"📂 [Local API] Reading local JSON dataset for {round_name}...")
    
    file_path = "jeopardy.json"
    
    if not os.path.exists(file_path):
        print(f"❌ [Local API] Critical Error: {file_path} not found!")
        return {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            all_clues = json.load(file)
            
        # 1. Filter out only the clues that belong to the round we are playing
        valid_clues = [c for c in all_clues if c.get("round") == round_name]
        
        # 2. Group the clues by category
        categories_dict = {}
        for clue in valid_clues:
            cat_name = clue.get("category", "UNKNOWN")
            if cat_name not in categories_dict:
                categories_dict[cat_name] = []
            
            categories_dict[cat_name].append({
                "value": clue.get("value", 0),
                "clue": clue.get("clue", ""),
                "answer": clue.get("answer", ""),
                "is_daily_double": False
            })

        # 3. Select a random subset of categories to build the board
        available_categories = list(categories_dict.keys())
        
        # Make sure we don't try to pick more categories than actually exist in the file!
        safe_category_count = min(num_categories, len(available_categories))
        
        # Final Jeopardy only needs 1 category!
        if round_name == "Final Jeopardy":
            safe_category_count = 1
            
        selected_category_names = random.sample(available_categories, safe_category_count)
        
        # 4. Build the final organized board dictionary
        organized_board = {}
        for cat_name in selected_category_names:
            # Sort the 5 clues by dollar value so they look right on the Pygame grid
            sorted_clues = sorted(categories_dict[cat_name], key=lambda x: int(x["value"]))
            organized_board[cat_name] = sorted_clues

        return organized_board

    except json.JSONDecodeError:
        print("❌ [Local API] Error: Your jeopardy.json file is corrupted or formatted incorrectly.")
        return {}