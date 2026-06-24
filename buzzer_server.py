import logging
import queue
from flask import Flask, request, redirect, jsonify

# --- DISABLE FLASK TERMINAL SPAM ---
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# --- SHARED STATE MEMORY ---
buzzer_queue = queue.Queue()
host_command_queue = queue.Queue() # NEW: Passes iPad button clicks back to Pygame

registered_players = {}
next_available_slot = 1

# NEW: Pygame will constantly update this dictionary so the iPad knows what is happening
host_state = {
    "is_active": False,
    "clue": "Waiting for host to select a clue...",
    "answer": "",
    "value": 0,
    "buzzer_name": None
}

app = Flask(__name__)

# ==========================================
# PLAYER ROUTES
# ==========================================
@app.route('/')
def registration_page():
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
    global next_available_slot
    name = request.form.get('player_name', '').strip()
    if not name: return "Name cannot be blank!", 400
        
    for slot, existing_name in registered_players.items():
        if existing_name.lower() == name.lower():
            return redirect(f'/buzzer/{slot}')
            
    if next_available_slot > 4: return "Lobby full!", 403
        
    assigned_slot = str(next_available_slot)
    registered_players[assigned_slot] = name
    next_available_slot += 1
    return redirect(f'/buzzer/{assigned_slot}')

@app.route('/buzzer/<player_num>')
def buzzer_page(player_num):
    if player_num not in registered_players: return redirect('/')
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
            <script>function sendBuzz() {{ fetch('/buzz/{player_num}', {{ method: 'POST' }}); }}</script>
        </body>
    </html>
    """

@app.route('/buzz/<player_num>', methods=['POST'])
def buzz(player_num):
    buzzer_queue.put(player_num)
    return "OK", 200

# ==========================================
# HOST ROUTES (THE PODIUM)
# ==========================================
@app.route('/host')
def host_dashboard():
    """The private screen for the host to see answers and press buttons."""
    return """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { background-color: #111; color: white; font-family: sans-serif; padding: 20px; text-align: center; }
                .card { background-color: #060CE9; border: 3px solid white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                h1 { color: #D69F4C; }
                h2 { color: #00FF00; font-size: 28px; }
                .btn { padding: 15px 20px; font-size: 18px; margin: 10px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 45%; }
                .btn-green { background-color: #4CAF50; color: white; }
                .btn-red { background-color: #f44336; color: white; }
                .btn-gray { background-color: #555; color: white; width: 95%; margin-top: 20px;}
                #buzzer-alert { font-size: 24px; color: yellow; font-weight: bold; margin-top: 15px; }
            </style>
        </head>
        <body>
            <h1>HOST PODIUM</h1>
            
            <div class="card">
                <p><strong>Clue Value:</strong> $<span id="val">0</span></p>
                <p style="font-size: 20px;" id="clue">Waiting for clue...</p>
                <hr>
                <p><strong>Correct Response:</strong></p>
                <h2 id="ans">--</h2>
                <div id="buzzer-alert"></div>
            </div>

            <div>
                <button class="btn btn-green" onclick="sendCommand('y')">CORRECT (Y)</button>
                <button class="btn btn-red" onclick="sendCommand('n')">WRONG (N)</button>
            </div>
            <button class="btn btn-gray" onclick="sendCommand('esc')">CANCEL CLUE (ESC)</button>

            <script>
                // This asks the server for the game state every 500 milliseconds!
                setInterval(() => {
                    fetch('/host/state')
                        .then(res => res.json())
                        .then(data => {
                            document.getElementById('val').innerText = data.value;
                            document.getElementById('clue').innerText = data.clue;
                            document.getElementById('ans').innerText = data.answer;
                            
                            if (data.buzzer_name) {
                                document.getElementById('buzzer-alert').innerText = "🚨 " + data.buzzer_name.toUpperCase() + " BUZZED! 🚨";
                            } else {
                                document.getElementById('buzzer-alert').innerText = "";
                            }
                        });
                }, 500);

                function sendCommand(cmd) {
                    fetch('/host/command/' + cmd, { method: 'POST' });
                }
            </script>
        </body>
    </html>
    """

@app.route('/host/state')
def get_host_state():
    """JS fetches this to update the iPad screen"""
    return jsonify(host_state)

@app.route('/host/command/<cmd>', methods=['POST'])
def host_command(cmd):
    """Takes button presses from the iPad and sends them to Pygame"""
    host_command_queue.put(cmd)
    return "OK", 200

def run_flask_server():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)