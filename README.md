# jeopardy-backend
Personal Project 1 on Boot.Dev
Creating a Jeopardy clone with a focus on backend functionality and less on the frontend bells and whistles.
Development was spread out over a few months with lots of refactoring and tweaking.
Lots of web research and AI discussion during development, I used Gemini Pro quite a bit.
A learning with AI is that it tends to just try and cram everything into one .py file to the point I ended up
with several functions in my game logic file not even being used, just sitting there as dead code.
A little extra effort and I split things up in a more logical way and I'm pretty happy with how it turned out.

🎮 How to Play
1. Start the Engine
Make sure you have your local dataset ready (run python3 build_json.py if you haven't yet). Then, launch the main display engine from your terminal:

Bash
python3 tv_display.py
The Jeopardy game board will open in full-screen on your computer, and the local Flask server will automatically spin up in the background.

2. Connect the Players
Have your players pull out their smartphones and connect to the same Wi-Fi network as your host computer.

Open a web browser (Safari/Chrome).

Navigate to: http://<YOUR-IP-ADDRESS>:5000/

Enter their name to lock in their buzzer.
(The system supports up to 4 concurrent players. Once registered, their phone screens will turn into massive, color-coded buzzer buttons).

3. Open the Host Podium
The host should use a separate device (like an iPad or a second smartphone) so they can see the answers secretly.

Connect to the same Wi-Fi network.

Navigate to: http://<YOUR-IP-ADDRESS>:5000/host

Keep this screen hidden from the players!

4. The Game Flow & Controls
The game is driven by the Host using a combination of the PC mouse (to select clues) and the Host Podium (to judge answers).

Selecting a Clue: Click any dollar value on the main TV screen using the computer mouse.

Judging Responses: When a player buzzes in on their phone, their name will flash on the Host Podium. Use the buttons on your Podium to grade them:

Tap CORRECT (Y) to award points and clear the clue.

Tap WRONG (N) to deduct points and re-open the floor for other buzzers.

Tap CANCEL CLUE (ESC) if nobody knows the answer.

Daily Doubles / Final Jeopardy: When a wager screen appears, use the computer keyboard to type the wager amount, then press ENTER to lock it in and reveal the clue.

Advancing the Game: When the board is clear, press the SPACEBAR on the computer keyboard to advance to the next round (Single -> Double -> Final -> Final Standings).

5. Saving the Results
When you press SPACEBAR after Final Jeopardy, the engine will automatically calculate the winner, display the Final Standings on the TV, and archive the game data (including player names, date, and final scores) to the SQLite historical ledger.
