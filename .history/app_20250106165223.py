from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from poker_logic.game_manager import GameManager

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Necessary for session management
socketio = SocketIO(app)

game_manager = GameManager()

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Dummy authentication (Replace with actual logic)
        if username == "testuser" and password == "password":  # Replace with database check
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add user to database here
        print(f"New user created: {username}")
        return redirect(url_for('login'))
    return render_template('signup.html')

# Route for the welcome page
@app.route('/welcome')
def welcome():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    return render_template('welcome.html', username=username)

# Route for the game page
@app.route('/game')
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('game.html')



@socketio.on('toggle_game')
def toggle_game():
    if game_manager.game_state == 'waiting':
        if game_manager.start_game():
            socketio.emit('game_started', to = None)
            socketio.emit('update_button', {'button_text': 'End Game'}, to = None)
    elif game_manager.game_state == 'playing':
        game_manager.end_game()
        socketio.emit('game_ended', to = None)
        socketio.emit('update_button', {'button_text': 'Start Game'}, to = None)

# Socket.IO Event Handlers
@socketio.on('message')
def handle_message(msg):
    print('Message received:', msg)
    socketio.emit('update', {'state': 'Game state updated!'})

@socketio.on('join_seat')
def handle_seat(player_info: dict):
    name = player_info[name]


if __name__ == '__main__':
    socketio.run(app, debug=True)
