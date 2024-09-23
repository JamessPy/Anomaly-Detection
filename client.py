import requests

def listen_to_stream():
    url = 'http://127.0.0.1:5000/stream'
    with requests.get(url, stream=True) as response:
        for line in response.iter_lines():
            if line:
                # Gelen veriyi işleme
                data = line.decode('utf-8').strip()
                print(data)

if __name__ == '__main__':
    listen_to_stream()
