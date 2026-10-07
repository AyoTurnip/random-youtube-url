import random
import re
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

WORDS = ['gaming', 'vlog', 'music', 'funny', 'review', 'tutorial', 'clip', 'shorts', 'stream', 'highlight', 'cat', 'dog', 'setup', 'build', 'guide']

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = f"{random.choice(WORDS)} {random.choice(WORDS)}"
        encoded_query = urllib.parse.quote(query)
        url = f"https://www.youtube.com/feeds/videos.xml?search_query={encoded_query}"

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                xml_data = response.read().decode('utf-8')

            video_ids = re.findall(r'<yt:videoId>(.*?)</yt:videoId>', xml_data)

            if video_ids:
                chosen_id = random.choice(video_ids)
                output = f"https://youtu.be/{chosen_id}"
            else:
                output = "https://youtu.be/dQw4w9WgXcQ"

        except Exception:
            output = "https://youtu.be/dQw4w9WgXcQ"

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))
