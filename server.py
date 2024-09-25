from flask import Flask
from flask_socketio import SocketIO, emit
import random
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Generate data
def generate_data():
    while True:
        try:
            if time.time() % 20 < 1:  # Approximately once every 20 seconds
                value = round(random.uniform(6, 7), 5)  # Value between 6 and 7
            
            elif time.time() % 20 >= 5 and time.time() % 20 <= 6:  # Approximately once every 20 seconds
                value = round(random.uniform(0, 1), 5)  # Value between 0 and 1
            else:
                value = round(random.uniform(3, 4), 5)  # Value between 3 and 4

            socketio.sleep(1)  # Wait a second
            socketio.emit('data_update', {'value': value})  # Emit data via WebSocket
            
        except Exception as e:
            print(f"Error occurred while generating data: {e}")

# Start the data generation in a background thread
@socketio.on('connect')
def handle_connect():
    print('Client connected')

    # Start generating data
    socketio.start_background_task(generate_data)

# Error handling
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
