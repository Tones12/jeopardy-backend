from flask import Flask

app = Flask(__name__)

# This is the webpage your phone will see
@app.route('/')
def home():
    return """
    <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #222; }
                .buzzer { width: 300px; height: 300px; border-radius: 50%; background-color: red; color: white; font-size: 40px; border: 10px solid darkred; font-weight: bold; }
                .buzzer:active { background-color: darkred; }
            </style>
        </head>
        <body>
            <form action="/buzz" method="POST">
                <button class="buzzer" type="submit">BUZZ IN</button>
            </form>
        </body>
    </html>
    """

# This is the "endpoint" the button hits when pressed
@app.route('/buzz', methods=['POST'])
def buzz():
    print("🚨 SOMEONE BUZZED IN! 🚨")
    # Redirect them right back to the buzzer page so they can hit it again
    return "<script>window.location.href='/';</script>"

if __name__ == "__main__":
    # 0.0.0.0 tells Flask to listen on ALL network adapters (including your Ethernet)
    # Port 5000 is the standard Flask web port
    print("Starting buzzer server...")
    app.run(host='0.0.0.0', port=5000)