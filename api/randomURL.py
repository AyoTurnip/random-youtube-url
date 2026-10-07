import random
import string
import requests

def generate_random_youtube_url():
    # YouTube IDs use A-Z, a-z, 0-9, hyphen (-), and underscore (_)
    characters = string.ascii_letters + string.digits + "-_"
    
    # Generate 11 random characters
    video_id = ''.join(random.choice(characters) for _ in range(11))
    
    url = f"https://youtu.be/{video_id}"
    return video_id, url

def check_video_availability(video_id):
    """
    Checks if a video ID points to a valid public video.
    Note: YouTube uses HTTP redirects or status codes for valid vs invalid IDs.
    """
    check_url = f"https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
    try:
        response = requests.get(check_url, timeout=5)
        # YouTube's oEmbed endpoint returns HTTP 200 for public videos, 
        # and 404 or 400 for non-existent/private/deleted videos.
        if response.status_code == 200:
            data = response.json()
            return True, data.get("title", "Unknown Title")
        else:
            return False, None
    except requests.RequestException as e:
        return False, str(e)

# Example Usage: Search until a valid video is found (or run N attempts)
if __name__ == "__main__":
    attempts = 10
    print(f"Generating and checking {attempts} random YouTube URLs...\n")

    for i in range(1, attempts + 1):
        video_id, url = generate_random_youtube_url()
        is_available, title_or_err = check_video_availability(video_id)
        
        if is_available:
            print(f"[{i}] FOUND! {url} | Title: {title_or_err}")
        else:
            print(f"[{i}] Unavailable: {url}")
