from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import requests
import base64
import os
from datetime import datetime
import time
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(1)
        count += 1
        file = r"C:\Users\Cornelius\Documents\GitHub\Intelligent_System\yolov5-master\data\images\detected.jpg"
        if os.path.exists(file):

            with open(file, 'rb') as image_file:
                image_binary = base64.b64encode(image_file.read()).decode('utf-8')

            socketio.emit('my_response',
                        {'data': 'Sending Image...', 'image': image_binary, 'count': count,'time': datetime.fromtimestamp(os.path.getmtime(file)).strftime('%H:%M:%S')
})
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.event
def my_event(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})

# Receive the test request from client and send back a test response
@socketio.on('test_message')
def handle_message(data):
    print('received message: ' + str(data))
    emit('test_response', {'data': 'Test response sent'})

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
    socketio.run(app,host="0.0.0.0", port=5000)