import random
import string
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

def generate_id():
    chars = string.ascii_letters + string.digits + "-_"
    return ''.join(random.choice(chars) for _ in range(11))

def check_video(video_id):
    """Queries YouTube's oEmbed endpoint to verify video availability."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=0.3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return True, data.get("title", "Valid Video")
    except Exception:
        pass
    return False, None

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        found = False
        selected_id = None
        title = ""

        # Try up to 10 random IDs within ~3 seconds
        for _ in range(10):
            vid = generate_id()
            is_valid, vid_title = check_video(vid)
            if is_valid:
                found = True
                selected_id = vid
                title = vid_title
                break

        # Fallback to a single random URL if none were found
        if not selected_id:
            selected_id = generate_id()

        if found:
            message = f"Found Live Video: '{title}' - https://youtu.be/{selected_id}"
        else:
            message = f"Random URL: https://youtu.be/{selected_id} (Status: Unverified)"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))
