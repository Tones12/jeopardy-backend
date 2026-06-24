import csv
import json

def process_dataset():
    # Make sure this matches the exact name of the file you downloaded!
    input_file = 'jeopardy_kids_dataset.tsv' 
    output_file = 'jeopardy.json'
    
    print(f"⚙️ Extracting data from {input_file}...")

    master_list = []

    # Map their dataset's round numbers to our engine's round names
    round_mapper = {
        "1": "Jeopardy",
        "2": "Double Jeopardy",
        "3": "Final Jeopardy"
    }

    try:
        # NOTE: If your file is a .csv, change delimiter='\t' to delimiter=','
        with open(input_file, mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile, delimiter='\t')
            
            for row in reader:
                round_num = row.get('round', '')
                
                # Only process rows that have a valid round number
                if round_num in round_mapper:
                    
                    # Clean up the money value (Final Jeopardy is usually blank or 0)
                    raw_value = row.get('clue_value', '0')
                    try:
                        clean_value = int(raw_value)
                    except ValueError:
                        clean_value = 0
                        
                    # Transform their columns into our JSON dictionary format
                    clue_data = {
                        "round": round_mapper[round_num],
                        "category": row.get('category', 'UNKNOWN'),
                        "value": clean_value,
                        "clue": row.get('answer', ''),    # The text on the board
                        "answer": row.get('question', '') # The correct response
                    }
                    
                    master_list.append(clue_data)

        print(f"💾 Transforming and loading {len(master_list)} clues into {output_file}...")
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(master_list, outfile, indent=2)
            
        print("✅ Pipeline complete! Your local JSON API is armed and ready.")

    except FileNotFoundError:
        print(f"❌ Error: Could not find {input_file}. Check the file name!")

if __name__ == "__main__":
    process_dataset()