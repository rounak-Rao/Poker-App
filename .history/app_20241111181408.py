from flask import Flask
from flask_socketio import SocketIO #SocketIO enables real-time communication between client and server

app = Flask(__name__)

socketio = SocketIO(app) #instantiates the SocketIO class and binds it to the flask app

@app.route('/')
def home():
    return "Welcome to my poker bot app"

if __name__ == '__main__':
    app.run(debug=True)