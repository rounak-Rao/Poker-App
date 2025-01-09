from flask import Flask, render_template
from flask_socketio import SocketIO #SocketIO enables real-time communication between client and server

app = Flask(__name__)

socketio = SocketIO(app) #instantiates the SocketIO class and binds it to the flask app

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
    

if __name__ == '__main__':
    app.run(debug=True)
    socketio.run(app, debug = True)