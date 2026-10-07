import random
import string
import requests
from http.server import BaseHTTPRequestHandler

def generate_random_id():
    chars = string.ascii_letters + string.digits + "-_"
    return ''.join(random.choice(chars) for _ in range(11))

def find_valid_video(max_attempts=10):
    for _ in range(max_attempts):
        video_id = generate_random_id()
        url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
        try:
            res = requests.get(url, timeout=2)
            if res.status_code == 200:
                title = res.json().get("title", "Unknown Title")
                return f"Found video: {title} - https://youtu.be/{video_id}"
        except Exception:
            pass
    
    # If no valid video was hit after max_attempts:
    return f"Random check: https://youtu.be/{generate_random_id()} (Availability unconfirmed)"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = find_valid_video()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
