from flask import Flask, Response
import random
import time

app = Flask(__name__)

def generate_data():
    while True:
        
        if time.time() % 10 < 1:
            value = random.uniform(10, 20)  # 10-20 arası bir değer
        else:
            value = random.uniform(0, 1)  # 0-1 arası bir değer

        yield f"data: {value}\n\n"
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(generate_data(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
