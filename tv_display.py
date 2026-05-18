import pygame
import sys
import threading
import queue
import logging
from flask import Flask
from game_logic import generate_board

# --- DISABLE FLASK TERMINAL SPAM ---
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- BUZZER QUEUE ---
buzzer_queue = queue.Queue()

# --- WEB SERVER ---
app = Flask(__name__)

# --- CONFIGURATION ---
WIDTH = 1200
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
JEOPARDY_BLUE = (6, 12, 233)
GOLD = (214, 159, 76)

@app.route('/<player_num')
def buzzer_page(player_num):
    colors = {"1": "red", "2": "blue", "3": "green", "4": "purple"}
    bg_color = colors.get(player_num, "gray")

    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
            <style>
                body {{ display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #222; margin: 0; }}
                .buzzer {{ width: 80vw; height: 80vw; max-width: 400px; max-height: 400px; border-radius: 50%; 
                           background-color: {bg_color}; color: white; font-size: 50px; font-weight: bold; border: 10px solid black; }}
                .buzzer:active {{ opacity: 0.5; }}
            </style>
        </head>
        <body>
            <form action="/buzz/{player_num}" method="POST">
                <button class="buzzer" type="submit">PLAYER {player_num}</button>
            </form>
        </body>
    </html>
    """

# --- BUTTON PRESS INTO QUEUE ---
@app.route('/buzz/<player_num>', methods=['POST'])
def buzz(player_num):
    # Player number sent to Pygame mailbox
    buzzer_queue.put(player_num)
    return f"<script>winder.location.href='/{player_num}';</script>"

# --- ENGINE: run on concurrent thread as game ---
def run_flask_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloade=False)

def draw_text_centered(surface, text, font, color, rect):
    """Helper function to perfectly center text inside a box"""
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_text_wrapped(surface, text, font, color, rect):
    """Helper function to word-wrap text inside a specific rectangle (Left-Aligned)"""
    words = text.split(' ')
    lines = []
    current_line = []

    # 1. Group words into lines that fit the width (with 40px total padding)
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        width, height = font.size(test_line)
        
        # If it's too wide, bump the word to the next line
        if width > rect.width - 40: 
            current_line.pop() 
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word] 
            
    if current_line:
        lines.append(' '.join(current_line))
        
    # 2. Calculate the vertical centering for the whole block of text
    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    start_y = rect.centery - (total_height // 2)
    
# 3. Draw each line CENTER-ALIGNED
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        
        # THE FIX: Center horizontally (centerx), but offset vertically based on the line number (i)
        # We add (line_height // 2) because center anchors to the middle of the text, not the top!
        y_position = start_y + (i * line_height) + (line_height // 2)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_position))
        
        surface.blit(text_surface, text_rect)

def main():
    # Initiate pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("This is Jeopardy")

    # --- NEW: The Data Bridge ---
    print("Fetching board data from database...")
    board_data = generate_board()
    categories = list(board_data.keys()) # Grab just the category names

    # --- NEW: The Grid Math ---
    num_cols = len(categories)
    num_rows = 6  # 1 row for Categories at the top + 5 rows for clues
    
    # We use // for integer division because Pygame can't draw half a pixel!
    col_width = WIDTH // num_cols 
    row_height = HEIGHT // num_rows

    print(f"Grid calculated: {num_cols} columns, {num_rows} rows.")
    print(f"Each box will be {col_width}px wide and {row_height}px tall.")

    # --- NEW: Set up fonts ---
    header_font = pygame.font.SysFont('impact', 36)
    value_font = pygame.font.SysFont('impact', 54)
    clue_font = pygame.font.SysFont('arial', 24)

    revealed_clues = set()

    # Web server initiation on background thread
    print("Starting Web Server for Buzzers...")
    web_thread = threading.Thread(target=run_flask_server, daemon=True)
    web_thread.start()

    revealed_clues = set()
    running = True
    while running:
        # Check for events (like clicking the 'X' to close the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- NEW: Mouse Click Detection ---
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_x, click_y = event.pos # Grab the pixel coordinates
                
                # Reverse the grid math to find the column and row index
                clicked_col = click_x // col_width
                clicked_row = click_y // row_height
                
                # Just register clicks on clues, not the categories
                if clicked_row > 0:
                    # Save this specific coordinate pair to our set
                    revealed_clues.add((clicked_col, clicked_row))
                    print(f"BAM! Clicked Col {clicked_col}, Row {clicked_row}")
        
        # --- NEW: Buzzer Mailbox Check ---
        try:
            buzzed_player = buzzer_queue.get_nowait()
            print(f"BING! Player {buzzed_player} buzzed in!")

            #TODO: Add visual Pygame logic here to show who buzzed.
        
        except queue.Empty():
            pass # Mailbox is empty, proceed through game loop

        # Paint the whole screen black to clear the previous frame
        screen.fill(BLACK)

        # 2. Draw the Grid Columns
        for col_idx, category_name in enumerate(categories):
            
            # --- Draw the Category Header (Row 0) ---
            # Rect(x, y, width, height)
            header_rect = pygame.Rect(col_idx * col_width, 0, col_width, row_height)
            pygame.draw.rect(screen, JEOPARDY_BLUE, header_rect)
            pygame.draw.rect(screen, BLACK, header_rect, 3) # Draws a 3px black border
            draw_text_centered(screen, category_name.upper(), header_font, WHITE, header_rect)

            # --- Draw the 5 Clue Values ---
            clues = board_data[category_name]
            for row_idx, clue in enumerate(clues):
                                
                # 1. Calculate the exact grid row for this clue
                screen_row = row_idx + 1
                
                # 2. Figure out the pixel coordinates
                y_position = screen_row * row_height
                clue_rect = pygame.Rect(col_idx * col_width, y_position, col_width, row_height)

                # 3. Paint the blue box and black border
                pygame.draw.rect(screen, JEOPARDY_BLUE, clue_rect)
                pygame.draw.rect(screen, BLACK, clue_rect, 3) # Border
                
                # --- NEW: The Reveal Logic ---
                if (col_idx, screen_row) in revealed_clues:
                    # NEW: Use the wrapping function for the long clue text!
                    draw_text_wrapped(screen, clue['clue'], clue_font, WHITE, clue_rect)
                else:
                    # Nobody clicked it yet. Draw the money!
                    dollar_amount = f"${clue['value']}"
                    draw_text_centered(screen, dollar_amount, value_font, GOLD, clue_rect)

        # Tell Pygame to push our painted frame to the actual monitor
        pygame.display.flip()

    # 4. Clean shutdown when the loop breaks
    pygame.quit()
    sys.exit()

# This is a Python standard that says "If I run this file directly, start the main function"
if __name__ == "__main__":
    main()