import pygame
import sys
import threading
import queue
import logging
import random
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

@app.route('/<player_num>')
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
                /* A quick visual flash when tapped so they know it registered */
                .buzzer:active {{ opacity: 0.5; transform: scale(0.95); }}
            </style>
        </head>
        <body>
            <button class="buzzer" onclick="sendBuzz()">PLAYER {player_num}</button>
            
            <script>
                // This function runs in the background when the button is tapped
                function sendBuzz() {{
                    fetch('/buzz/{player_num}', {{ method: 'POST' }});
                }}
            </script>
        </body>
    </html>
    """

# --- BUTTON PRESS INTO QUEUE ---
@app.route('/buzz/<player_num>', methods=['POST'])
def buzz(player_num):
    # Player number sent to Pygame mailbox
    buzzer_queue.put(player_num)
    return "OK", 200

# --- ENGINE: run on concurrent thread as game ---
def run_flask_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

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
    pygame.display.set_caption("This is Jeopardy!")

    # --- NEW: The Data Bridge ---
    print("Fetching board data from database...")
    board_data = generate_board()
    categories = list(board_data.keys()) # Grab just the category names

    # --- NEW: The Grid Math ---
    num_cols = len(categories)
    num_rows = 6  # 1 row for Categories at the top + 5 rows for clues
    
    # We use // for integer division because Pygame can't draw half a pixel!
    col_width = WIDTH // num_cols 
    row_height = (HEIGHT - 60) // num_rows

    print(f"Grid calculated: {num_cols} columns, {num_rows} rows.")
    print(f"Each box will be {col_width}px wide and {row_height}px tall.")

    # Daily Double Implementation
    dd_col = random.randint(0, num_cols - 1)
    dd_row = random.randint(1, 5)
    daily_double_coords = (dd_col, dd_row)
    print(f"Daily Double location determined")

    # --- NEW: Set up fonts ---
    header_font = pygame.font.SysFont('impact', 36)
    value_font = pygame.font.SysFont('impact', 54)
    clue_font = pygame.font.SysFont('arial', 24)

    # --- NEW: Game State Trackers ---
    active_clue = None      # Holds the data for the clue currently on screen
    active_col_row = None   # Remembers which grid box we clicked
    current_buzzer = None   # Remembers who rang in first
    
    # Player score dictionary
    player_scores = {"1": 0, "2": 0, "3": 0, "4": 0}

    # --- NEW: Launch the Web Server on a Background Thread ---
    print("Starting Web Server for Buzzers...")
    web_thread = threading.Thread(target=run_flask_server, daemon=True)
    web_thread.start()

    revealed_clues = set()
    
    # Daily Double wagering variable definition
    is_wager_screen = False
    wager_text = ""
    
    running = True
    while running:
        # --- 1. EVENT HANDLING (Mouse & Keyboard) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # STATE A: We are on the main board (No active clue)
            elif event.type == pygame.MOUSEBUTTONDOWN and not active_clue:
                click_x, click_y = event.pos
                clicked_col = click_x // col_width
                clicked_row = click_y // row_height
                
                if clicked_row > 0 and (clicked_col, clicked_row) not in revealed_clues:
                    category_name = categories[clicked_col]
                    active_clue = board_data[category_name][clicked_row - 1]
                    active_col_row = (clicked_col, clicked_row)
                    current_buzzer = None
                    
                    # --- New: Daily Double Check ---
                    if active_col_row == daily_double_coords:
                        is_wager_screen = True
                        wager_text = ""

                    # Empty the mailbox of any accidental early buzzes
                    while not buzzer_queue.empty():
                        buzzer_queue.get_nowait()
            
            # --- NEW: STATE C: Daily Double Wager Screen ---
            elif event.type == pygame.KEYDOWN and is_wager_screen:
                if event.key == pygame.K_RETURN and wager_text != "":
                    # Host pressed enter. Overwrite the clue's value and show the question
                    active_clue['value'] = int(wager_text)
                    is_wager_screen = False
                elif event.key == pygame.K_BACKSPACE:
                    wager_text = wager_text[:-1]
                elif event.unicode.isnumeric():
                    wager_text += event.unicode

            # STATE B: A clue is on screen, listen for the Host Keyboard.
            elif event.type == pygame.KEYDOWN and active_clue:
                if event.key == pygame.K_ESCAPE: # HOST: Cancel / Skip Clue
                    revealed_clues.add(active_col_row)
                    active_clue = None
                    
                elif event.key == pygame.K_y and current_buzzer: # HOST: Correct Answer!
                    player_scores[current_buzzer] += active_clue['value']
                    print(f"CORRECT! Player {current_buzzer} now has ${player_scores[current_buzzer]}")
                    revealed_clues.add(active_col_row)
                    active_clue = None
                    current_buzzer = None
                    
                elif event.key == pygame.K_n and current_buzzer: # HOST: Incorrect Answer!
                    player_scores[current_buzzer] -= active_clue['value']
                    print(f"WRONG! Player {current_buzzer} now has ${player_scores[current_buzzer]}")
                    current_buzzer = None 
                    while not buzzer_queue.empty():
                        buzzer_queue.get_nowait()
                
        # --- MAILBOX CHECK (Phone Buzzers) ---
        # Only accept buzzes if a clue is active AND nobody has currently buzzed
        if active_clue and not current_buzzer:
            try:
                current_buzzer = buzzer_queue.get_nowait()
            except queue.Empty:
                pass

        # Paint the whole screen black to clear the previous frame
        screen.fill(BLACK)   

        # Draw the Grid Columns
        for col_idx, category_name in enumerate(categories):
            
            # --- Draw the Category Header (Row 0) ---
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
                
                # --- UPDATED: The Reveal Logic ---
                if (col_idx, screen_row) in revealed_clues:
                    # Draw a blank blue square for completed clues!
                    pass 
                else:
                    # Nobody clicked it yet. Draw the money!
                    dollar_amount = f"${clue['value']}"
                    draw_text_centered(screen, dollar_amount, value_font, GOLD, clue_rect)

        # --- 4. THE FULL-SCREEN OVERLAY ---
        if active_clue:
            # Draw a massive box over the center of the screen
            overlay_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
            pygame.draw.rect(screen, JEOPARDY_BLUE, overlay_rect)
            pygame.draw.rect(screen, WHITE, overlay_rect, 5) # White border
            
            if is_wager_screen:
                title_rect = pygame.Rect(100, 150, WIDTH - 200, 100)
                draw_text_centered(screen, "DAILY DOUBLE", value_font, GOLD, title_rect)
                draw_text_centered(screen, f"Wager: ${wager_text}", value_font, WHITE, overlay_rect)

            else:
                # Draw the giant clue text
                draw_text_wrapped(screen, active_clue['clue'], value_font, WHITE, overlay_rect)
            
                # If someone buzzed, paint an alert banner at the bottom!
                if current_buzzer:
                    banner_rect = pygame.Rect(100, HEIGHT - 180, WIDTH - 200, 80)
                    pygame.draw.rect(screen, BLACK, banner_rect)
                    pygame.draw.rect(screen, WHITE, banner_rect, 3)
                
                    alert_text = f"🚨 PLAYER {current_buzzer} BUZZED IN! (Host: Y=Correct, N=Incorrect) 🚨"
                    draw_text_centered(screen, alert_text, header_font, GOLD, banner_rect)

        # --- 5. THE SCOREBOARD ---
        # Draw a solid black bar across the bottom
        score_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
        pygame.draw.rect(screen, BLACK, score_rect)
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 3) # Top border line

        # Split the width equally among 4 players
        player_width = WIDTH // 4
        for i in range(1, 5):
            p_num = str(i)
            
            # Dynamic coloring: Green for positive, Red for negative, White for zero
            score_color = WHITE
            if player_scores[p_num] > 0:
                score_color = (100, 255, 100) 
            elif player_scores[p_num] < 0:
                score_color = (255, 100, 100) 
                
            score_text = f"Player {p_num}: ${player_scores[p_num]}"
            
            # Calculate the exact box for this specific player's score
            p_rect = pygame.Rect((i - 1) * player_width, HEIGHT - 60, player_width, 60)
            draw_text_centered(screen, score_text, clue_font, score_color, p_rect)

        # Tell Pygame to push our painted frame to the actual monitor
        pygame.display.flip()

    # 4. Clean shutdown when the loop breaks
    pygame.quit()
    sys.exit()

# This is a Python standard that says "If I run this file directly, start the main function"
if __name__ == "__main__":
    main()