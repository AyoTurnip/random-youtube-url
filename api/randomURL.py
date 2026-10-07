import random
import string
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Generate 11 random valid YouTube ID characters
        chars = string.ascii_letters + string.digits + "-_"
        video_id = ''.join(random.choice(chars) for _ in range(11))
        
        # Plain text message for StreamElements
        message = f"Random YouTube URL: https://youtu.be/{video_id}"
        
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
