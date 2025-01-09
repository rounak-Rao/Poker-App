from flask import Flask, render_template
from flask_socketio import SocketIO, emit #SocketIO enables real-time communication between client and server
from poker_logic import *


app = Flask(__name__)

socketio = SocketIO(app) #instantiates the SocketIO class and binds it to the flask app
game_manager = Game

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')


@socketio.on('message')
def handle_message(msg):
    print('message received: '+ msg)
    socketio.emit('update', {'state': 'Game state updated!'})


@socketio.on('create_player')
def handle_create_player(data):
    name = data['name']
    stack = data['stack']
    new_player = game_manager.add_player(name, stack)
    if new_player:
        emit('player_created', {"name": new_player.name, "stack": new_player.stack, "position": new_player.position}, broadcast=True)
        emit('game_update', game_manager.get_game_state(), broadcast=True)
    else:
        emit('error', {"message": "Game is full"})


if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug = True)