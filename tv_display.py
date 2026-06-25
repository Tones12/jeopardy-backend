import pygame
import sys
import threading
import queue
from game_logic import generate_board

# --- IMPORT THE NEW HOST STATE & COMMAND QUEUE ---
from buzzer_server import run_flask_server, buzzer_queue, registered_players, host_state, host_command_queue

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
            if current_line: lines.append(' '.join(current_line))
            current_line = [word] 
    if current_line: lines.append(' '.join(current_line))
        
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

    header_font = pygame.font.SysFont('impact', 28) # Font size changed from 36 to 28
    value_font = pygame.font.SysFont('impact', 54)
    clue_font = pygame.font.SysFont('arial', 24)

    rounds = ["Jeopardy", "Double Jeopardy", "Final Jeopardy"]
    current_round_idx = 0

    def load_round_state(idx):
        b_data = generate_board(rounds[idx])
        cats = list(b_data.keys())
        cols = max(len(cats), 1)
        rows = 6 if idx < 2 else 2 
        c_w = WIDTH // cols
        r_h = (HEIGHT - 60) // rows
        return b_data, cats, cols, rows, c_w, r_h

    print(f"Loading {rounds[current_round_idx]}...")
    board_data, categories, num_cols, num_rows, col_width, row_height = load_round_state(current_round_idx)

    active_clue = None      
    active_col_row = None   
    current_buzzer = None   
    player_scores = {"1": 0, "2": 0, "3": 0, "4": 0}
    is_wager_screen = False 
    wager_text = ""         
    revealed_clues = set()
    is_game_over = False

    print("Starting Web Server for Buzzers...")
    web_thread = threading.Thread(target=run_flask_server, daemon=True)
    web_thread.start()

    def process_host_command(cmd_string):
        """Helper to process host commands from either Keyboard OR the iPad!"""
        nonlocal active_clue, current_buzzer
        if not active_clue or is_wager_screen:
            return

        if cmd_string == 'esc':
            revealed_clues.add(active_col_row)
            active_clue = None
            host_state["is_active"] = False
            host_state["clue"] = "Waiting for host to select a clue..."
            host_state["answer"] = ""
            host_state["buzzer_name"] = None
        
        elif cmd_string == 'y' and current_buzzer:
            player_scores[current_buzzer] += active_clue['value']
            revealed_clues.add(active_col_row)
            active_clue = None
            current_buzzer = None
            host_state["is_active"] = False
            host_state["clue"] = "Waiting for host to select a clue..."
            host_state["answer"] = ""
            host_state["buzzer_name"] = None
            
        elif cmd_string == 'n' and current_buzzer:
            player_scores[current_buzzer] -= active_clue['value']
            current_buzzer = None 
            host_state["buzzer_name"] = None # Clear the alert on the iPad
            while not buzzer_queue.empty():
                buzzer_queue.get_nowait()

    running = True
    while running:
        # --- 1. CHECK HOST COMMANDS ---
        try:
            remote_cmd = host_command_queue.get_nowait()
            process_host_command(remote_cmd)
        except queue.Empty:
            pass

        # --- 2. EVENT HANDLING (Keyboard/Mouse) ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN and not active_clue and not is_wager_screen:
                if event.key == pygame.K_SPACE: 
                    if current_round_idx < 2:
                        current_round_idx += 1
                        print(f"--- ADVANCING TO {rounds[current_round_idx].upper()} ---")
                        board_data, categories, num_cols, num_rows, col_width, row_height = load_round_state(current_round_idx)
                        revealed_clues.clear()
                        current_buzzer = None
                        while not buzzer_queue.empty():
                            buzzer_queue.get_nowait()
                    elif current_round_idx == 2:
                        print("--- CALCULATING FINAL SCORES ---")
                        is_game_over = True
                        from game_logic import save_game_results
                        save_game_results(player_scores, registered_players)

            elif event.type == pygame.MOUSEBUTTONDOWN and not active_clue and not is_game_over:
                click_x, click_y = event.pos
                clicked_col = click_x // col_width
                clicked_row = click_y // row_height
                
                if clicked_row > 0 and (clicked_col, clicked_row) not in revealed_clues:
                    category_name = categories[clicked_col]
                    clue_list = board_data[category_name]

                    # Only open the clue if it actually exists in the array
                    if (clicked_row - 1) < len(clue_list):
                        active_clue = clue_list[clicked_row - 1]
                        active_col_row = (clicked_col, clicked_row)
                        current_buzzer = None
                        
                        # --- NEW: PUSH DATA TO IPAD ---
                        host_state["is_active"] = True
                        host_state["value"] = active_clue['value']
                        host_state["clue"] = active_clue['clue']
                        host_state["answer"] = active_clue['answer']
                        host_state["buzzer_name"] = None
                        
                        if active_clue.get('is_daily_double', False):
                            is_wager_screen = True
                            wager_text = ""
                        
                        while not buzzer_queue.empty():
                            buzzer_queue.get_nowait()

            elif event.type == pygame.KEYDOWN and is_wager_screen:
                if event.key == pygame.K_RETURN and wager_text != "":
                    active_clue['value'] = int(wager_text)
                    host_state["value"] = active_clue['value'] # Update iPad with new wager
                    is_wager_screen = False
                elif event.key == pygame.K_BACKSPACE:
                    wager_text = wager_text[:-1] 
                elif event.unicode.isnumeric():
                    wager_text += event.unicode  

            elif event.type == pygame.KEYDOWN and active_clue and not is_wager_screen:
                if event.key == pygame.K_ESCAPE: process_host_command('esc')
                elif event.key == pygame.K_y: process_host_command('y')
                elif event.key == pygame.K_n: process_host_command('n')

        # --- 3. CHECK PHONE BUZZERS ---
        if active_clue and not current_buzzer and not is_wager_screen and current_round_idx != 2:
            try:
                current_buzzer = buzzer_queue.get_nowait()
                # --- NEW: PUSH BUZZER NAME TO IPAD ---
                host_state["buzzer_name"] = registered_players.get(current_buzzer, f"Player {current_buzzer}")
            except queue.Empty:
                pass

        # --- 4. RENDER SCREEN ---
        screen.fill(BLACK)
        
        if is_game_over:
            sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
            title_rect = pygame.Rect(0, 50, WIDTH, 100)
            draw_text_centered(screen, "FINAL STANDINGS", value_font, GOLD, title_rect)
            for index, (p_num, score) in enumerate(sorted_players):
                display_name = registered_players.get(p_num, f"Player {p_num}")
                color = GOLD if index == 0 else WHITE
                text = f"{index + 1}. {display_name}   -   ${score}"
                row_rect = pygame.Rect(0, 200 + (index * 100), WIDTH, 100)
                draw_text_centered(screen, text, value_font, color, row_rect)
        else:
            for col_idx, category_name in enumerate(categories):
                header_rect = pygame.Rect(col_idx * col_width, 0, col_width, row_height)
                pygame.draw.rect(screen, JEOPARDY_BLUE, header_rect)
                pygame.draw.rect(screen, BLACK, header_rect, 3) 
                draw_text_wrapped(screen, category_name.upper(), header_font, WHITE, header_rect)

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
                        if current_round_idx == 2:
                            box_text = "FINAL JEOPARDY"
                        else:
                            box_text = f"${clue['value']}"
                        draw_text_centered(screen, box_text, value_font, GOLD, clue_rect)

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
                    display_name = registered_players.get(current_buzzer, f"Player {current_buzzer}")
                    banner_rect = pygame.Rect(100, HEIGHT - 180, WIDTH - 200, 80)
                    pygame.draw.rect(screen, BLACK, banner_rect)
                    pygame.draw.rect(screen, WHITE, banner_rect, 3)
                    alert_text = f"🚨 {display_name.upper()} BUZZED! (Y=Correct, N=Incorrect) 🚨"
                    draw_text_centered(screen, alert_text, header_font, GOLD, banner_rect)

        score_rect = pygame.Rect(0, HEIGHT - 60, WIDTH, 60)
        pygame.draw.rect(screen, BLACK, score_rect)
        pygame.draw.line(screen, WHITE, (0, HEIGHT - 60), (WIDTH, HEIGHT - 60), 3)

        player_width = WIDTH // 4
        for i in range(1, 5):
            p_num = str(i)
            display_name = registered_players.get(p_num, f"Slot {p_num} [Empty]")
            score_color = WHITE
            if player_scores[p_num] > 0:
                score_color = (100, 255, 100) 
            elif player_scores[p_num] < 0:
                score_color = (255, 100, 100) 
                
            score_text = f"{display_name}: ${player_scores[p_num]}"
            p_rect = pygame.Rect((i - 1) * player_width, HEIGHT - 60, player_width, 60)
            draw_text_centered(screen, score_text, clue_font, score_color, p_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()