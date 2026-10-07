import random
import string
import urllib.request
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import BaseHTTPRequestHandler

def generate_random_id():
    chars = string.ascii_letters + string.digits + "-_"
    return ''.join(random.choice(chars) for _ in range(11))

def check_single_id(video_id):
    """Checks if a video ID is valid via YouTube's oEmbed endpoint."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=1.5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return True, video_id, data.get("title", "Unknown Title")
    except Exception:
        pass
    return False, video_id, None

def find_first_valid_video(batch_size=50):
    """Generates and checks batch_size random IDs concurrently."""
    candidate_ids = [generate_random_id() for _ in range(batch_size)]
    
    # Run requests in parallel using 20 threads to finish in under 1 second
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(check_single_id, vid) for vid in candidate_ids]
        for future in as_completed(futures):
            is_valid, video_id, title = future.result()
            if is_valid:
                # Cancel remaining futures if we found a valid hit
                executor.shutdown(wait=False, cancel_futures=True)
                return f"'{title}' -> https://youtu.be/{video_id}"
                
    # If none were valid (expected due to 1-in-100-million odds), return a fast sample check
    sample_id = candidate_ids[0]
    return f"try again noob"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        result_text = find_first_valid_video()
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(result_text.encode('utf-8'))
