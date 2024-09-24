from flask import Flask, Response
import random
import time

app = Flask(__name__)

# Generate data
def generate_data():
    while True:
        try:
            if time.time() % 20 < 1 and time.time() % 20 >= 0:
                value = round(random.uniform(6, 7), 5)   # Value between 10 and 20
            
            elif time.time() % 20 >= 5 and  time.time() % 20 <= 6:
                value = round(random.uniform(0, 1), 5)  # Value between 10 and 20
            else:
                value = round(random.uniform(3, 4), 5)  #  Value between 0 and 1

            time.sleep(1) # Wait a second
            yield f"data: {value}\n\n"
            
        
        # Error handling while generating data
        except Exception as e:
            print(f"Error occurred while generating data: {e}")
            yield "data: An error occurred\n\n"

#URL
@app.route('/stream')

def stream():
    try:
        return Response(generate_data(), mimetype='text/event-stream')
    
    # Error handling while streaming
    except Exception as e:
        print(f"Error occurred while opening the stream: {e}")
        return Response("data: An error occurred\n\n", status=500)

if __name__ == '__main__':
    try:
        app.run(debug=True, threaded=True)

    # Error handling while starting app
    except Exception as e:
        print(f"Error occurred while starting the Flask application: {e}")
