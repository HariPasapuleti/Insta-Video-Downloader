# utils.py
import requests

def get_instagram_video_url(instagram_url):
    try:
        # Your logic to extract the video URL from Instagram
        response = requests.get(instagram_url)
        
        if response.status_code == 200:
            # Extract the video URL (this is just a placeholder logic)
            # Make sure to parse the HTML or use an API to extract the actual video URL
            video_url = "https://example.com/video.mp4"  # Replace with actual URL extraction logic
            return video_url
        else:
            print(f"Failed to fetch Instagram page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Instagram video: {e}")
        return None
