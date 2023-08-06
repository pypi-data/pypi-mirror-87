#!/bin/env python3

from langauge.core.service import main
from flask_socketio import SocketIO

app = main.create_app(debug=True)
socketio = SocketIO(app)

host = app.config.get("HOST")
port = app.config.get("PORT")

if __name__ == '__main__':
    print("Server running at http://%s:%s" % (host, port))
    socketio.run(app, host, port=int(port))
