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
        required_clues = 1 if round_name == "Final Jeopardy" else 5
        robust_categories = {name: clues for name, clues in categories_dict.items() if len(clues) >= required_clues}

        available_categories = list(robust_categories.keys())
        
        if not available_categories:
            print(f"❌ [Local API] Error: Not enough complete categories found for {round_name}!")
            return {}

        safe_category_count = min(num_categories, len(available_categories))
        if round_name == "Final Jeopardy":
            safe_category_count = 1
            
        selected_category_names = random.sample(available_categories, safe_category_count)
        
        # --- THE DOLLAR VALUE FIX ---
        # Set the base multiplier ($200 for Single, $400 for Double)
        base_value = 200 if round_name == "Jeopardy" else 400
        
        organized_board = {}
        for cat_name in selected_category_names:
            # Sort the clues by their original historical difficulty
            sorted_clues = sorted(robust_categories[cat_name], key=lambda x: int(x["value"]))
            
            # Slice EXACTLY the amount we need (prevents 6+ questions from breaking the grid)
            sliced_clues = sorted_clues[:required_clues]
            
            # Overwrite the historical dollar values with perfect increments
            for index, clue in enumerate(sliced_clues):
                if round_name != "Final Jeopardy":
                    clue["value"] = base_value * (index + 1)
                    
            organized_board[cat_name] = sliced_clues

        return organized_board

    except json.JSONDecodeError:
        print("❌ [Local API] Error: Your jeopardy.json file is corrupted or formatted incorrectly.")
        return {}