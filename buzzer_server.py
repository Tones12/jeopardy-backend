import logging
import queue
from flask import Flask, request, redirect

# --- DISABLE FLASK TERMINAL SPAM ---
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- SHARED STATE MEMORY ---
# We define these here so tv_display.py can import and read them!
buzzer_queue = queue.Queue()
registered_players = {}
next_available_slot = 1

# --- THE WEB SERVER ---
app = Flask(__name__)

@app.route('/')
def registration_page():
    """Step 1: The Landing Page. Captures the human name."""
    return """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #222; color: white; font-family: sans-serif; margin: 0; }
                input { padding: 15px; font-size: 18px; margin-bottom: 15px; border-radius: 5px; border: none; width: 80%; max-width: 300px; text-align: center; }
                button { padding: 15px 30px; font-size: 18px; background-color: #d69f4c; border: none; border-radius: 5px; cursor: pointer; color: black; font-weight: bold; width: 80%; max-width: 300px; }
            </style>
        </head>
        <body>
            <h2>Join the Jeopardy Game!</h2>
            <form action="/register" method="POST">
                <input type="text" name="player_name" placeholder="Enter Your Name" required maxlength="12"><br>
                <button type="submit">LOCK IN BUZZER</button>
            </form>
        </body>
    </html>
    """

@app.route('/register', methods=['POST'])
def handle_registration():
    """Step 2: The Logic Gate. Dynamically assigns a name to an open physical slot."""
    global next_available_slot
    
    name = request.form.get('player_name', '').strip()
    if not name:
        return "Name cannot be blank!", 400
        
    for slot, existing_name in registered_players.items():
        if existing_name.lower() == name.lower():
            return redirect(f'/buzzer/{slot}')
            
    if next_available_slot > 4:
        return "The game lobby is full! Maximum 4 players.", 403
        
    assigned_slot = str(next_available_slot)
    registered_players[assigned_slot] = name
    next_available_slot += 1
    
    return redirect(f'/buzzer/{assigned_slot}')

@app.route('/buzzer/<player_num>')
def buzzer_page(player_num):
    """Step 3: The View. Renders the custom button with the human name."""
    if player_num not in registered_players:
        return redirect('/')
        
    name = registered_players[player_num]
    colors = {"1": "red", "2": "blue", "3": "green", "4": "purple"}
    bg_color = colors.get(player_num, "gray")
    
    return f"""
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
            <style>
                body {{ display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #222; margin: 0; }}
                .buzzer {{ width: 80vw; height: 80vw; max-width: 400px; max-height: 400px; border-radius: 50%; 
                           background-color: {bg_color}; color: white; font-size: 40px; font-weight: bold; border: 10px solid black; }}
                .buzzer:active {{ opacity: 0.5; transform: scale(0.95); }}
            </style>
        </head>
        <body>
            <button class="buzzer" onclick="sendBuzz()">{name.upper()}</button>
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
    """Starts the Flask server loop"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)