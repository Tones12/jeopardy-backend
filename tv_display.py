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

# --- THE MAILBOX ---
buzzer_queue = queue.Queue()

# --- THE WEB SERVER ---
app = Flask(__name__)

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
                .buzzer:active {{ opacity: 0.5; transform: scale(0.95); }}
            </style>
        </head>
        <body>
            <button class="buzzer" onclick="sendBuzz()">PLAYER {player_num}</button>
            <script>
                function sendBuzz() {{
                    fetch('/buzz/{player_num}', {{ method: 'POST' }});
                }}
            </script>
        </body>
    </html>
    """

@app.route('/buzz/<player_num>', methods=['POST'])
def buzz(player_num):
    buzzer_queue.put(player_num)
    return "OK", 200

def run_flask_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# --- CONFIGURATION ---
WIDTH = 1200
HEIGHT = 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
JEOPARDY_BLUE = (6, 12, 233)
GOLD = (214, 159, 76)

def draw_text_centered(surface, text, font, color, rect):
    text_surface = font.render(str(text), True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_text_wrapped(surface, text, font, color, rect):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        width, height = font.size(test_line)
        if width > rect.width - 40: 
            current_line.pop() 
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word] 
    if current_line:
        lines.append(' '.join(current_line))
        
    line_height = font.get_linesize()
    total_height = len(lines) * line_height
    start_y = rect.centery - (total_height // 2)
    
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, color)
        y_position = start_y + (i * line_height) + (line_height // 2)
        text_rect = text_surface.get_rect(center=(rect.centerx, y_position))
        surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("This is Jeopardy")

    print("Fetching board data from database...")
    board_data = generate_board()
    categories = list(board_data.keys())

    num_cols = len(categories)
    num_rows = 6  
    col_width = WIDTH // num_cols 
    row_height = (HEIGHT - 60) // num_rows 

    header_font = pygame.font.SysFont('impact', 36)
    value_font = pygame.font.SysFont('impact', 54)
    clue_font = pygame.font.SysFont('arial', 24)

    # --- GAME STATE TRACKERS ---
    active_clue = None      
    active_col_row = None   
    current_buzzer = None   
    player_scores = {"1": 0, "2": 0, "3": 0, "4": 0}
    is_wager_screen = False 
    wager_text = ""         
    revealed_clues = set()

    # --- LAUNCH WEB SERVER ---
    print("Starting Web Server for Buzzers...")
    web_thread = threading.Thread(target=run_flask_server, daemon=True)
    web_thread.start()

    running = True
    while running:
        # --- 1. EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # STATE A: Main Board Clicks
            elif event.type == pygame.MOUSEBUTTONDOWN and not active_clue:
                click_x, click_y = event.pos
                clicked_col = click_x // col_width
                clicked_row = click_y // row_height
                
                if clicked_row > 0 and (clicked_col, clicked_row) not in revealed_clues:
                    category_name = categories[clicked_col]
                    active_clue = board_data[category_name][clicked_row - 1]
                    active_col_row = (clicked_col, clicked_row)
                    current_buzzer = None
                    
                    if active_clue.get('is_daily_double', False):
                        is_wager_screen = True
                        wager_text = ""
                    
                    while not buzzer_queue.empty():
                        buzzer_queue.get_nowait()

            # STATE C: Daily Double Wager Typing
            elif event.type == pygame.KEYDOWN and is_wager_screen:
                if event.key == pygame.K_RETURN and wager_text != "":
                    active_clue['value'] = int(wager_text)
                    is_wager_screen = False
                elif event.key == pygame.K_BACKSPACE:
                    wager_text = wager_text[:-1] 
                elif event.unicode.isnumeric():
                    wager_text += event.unicode  

            # STATE B: Host Controls (Y/N/ESC)
            elif event.type == pygame.KEYDOWN and active_clue and not is_wager_screen:
                if event.key == pygame.K_ESCAPE: 
                    revealed_clues.add(active_col_row)
                    active_clue = None
                    
                elif event.key == pygame.K_y and current_buzzer: 
                    player_scores[current_buzzer] += active_clue['value']
                    revealed_clues.add(active_col_row)
                    active_clue = None
                    current_buzzer = None
                    
                elif event.key == pygame.K_n and current_buzzer: 
                    player_scores[current_buzzer] -= active_clue['value']
                    current_buzzer = None 
                    while not buzzer_queue.empty():
                        buzzer_queue.get_nowait()

        # --- 2. MAILBOX CHECK ---
        if active_clue and not current_buzzer and not is_wager_screen:
            try:
                current_buzzer = buzzer_queue.get_nowait()
            except queue.Empty:
                pass

        # --- 3. PAINT THE GRID ---
        screen.fill(BLACK)
        for col_idx, category_name in enumerate(categories):
            header_rect = pygame.Rect(col_idx * col_width, 0, col_width, row_height)
            pygame.draw.rect(screen, JEOPARDY_BLUE, header_rect)
            pygame.draw.rect(screen, BLACK, header_rect, 3) 
            draw_text_centered(screen, category_name.upper(), header_font, WHITE, header_rect)

            clues = board_data[category_name]
            for row_idx, clue in enumerate(clues):
                screen_row = row_idx + 1
                y_position = screen_row * row_height
                clue_rect = pygame.Rect(col_idx * col_width, y_position, col_width, row_height)

                pygame.draw.rect(screen, JEOPARDY_BLUE, clue_rect)
                pygame.draw.rect(screen, BLACK, clue_rect, 3) 
                
                if (col_idx, screen_row) in revealed_clues:
                    pass 
                else:
                    dollar_amount = f"${clue['value']}"
                    draw_text_centered(screen, dollar_amount, value_font, GOLD, clue_rect)

        # --- 4. THE FULL-SCREEN OVERLAY ---
        if active_clue:
            overlay_rect = pygame.Rect(100, 100, WIDTH - 200, HEIGHT - 200)
            pygame.draw.rect(screen, JEOPARDY_BLUE, overlay_rect)
            pygame.draw.rect(screen, WHITE, overlay_rect, 5) 
            
            if is_wager_screen:
                title_rect = pygame.Rect(100, 150, WIDTH - 200, 100)
                draw_text_centered(screen, "DAILY DOUBLE", value_font, GOLD, title_rect)
                draw_text_centered(screen, f"Wager: ${wager_text}", value_font, WHITE, overlay_rect)
            else:
                draw_text_wrapped(screen, active_clue['clue'], value_font, WHITE, overlay_rect)
                if current_buzzer:
                    banner_rect = pygame.Rect(100, HEIGHT - 180, WIDTH - 200, 80)
                    pygame.draw.rect(screen, BLACK, banner_rect)
                    pygame.draw.rect(screen, WHITE, banner_rect, 3)
                    alert_text = f"🚨 PLAYER {current_buzzer} BUZZED! (Y=Correct, N=Incorrect) 🚨"
                    draw_text_centered(screen, alert_text, header_font, GOLD, banner_rect)

        # --- 5. THE SCOREBOARD ---
        score_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
        pygame.draw.rect(screen, BLACK, score_rect)
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 3)

        player_width = WIDTH // 4
        for i in range(1, 5):
            p_num = str(i)
            score_color = WHITE
            if player_scores[p_num] > 0:
                score_color = (100, 255, 100) 
            elif player_scores[p_num] < 0:
                score_color = (255, 100, 100) 
                
            score_text = f"Player {p_num}: ${player_scores[p_num]}"
            p_rect = pygame.Rect((i - 1) * player_width, HEIGHT - 60, player_width, 60)
            draw_text_centered(screen, score_text, clue_font, score_color, p_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()