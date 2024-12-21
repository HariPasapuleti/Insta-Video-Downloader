import requests

def fetch_video(video_url):
    try:
        response = requests.get(video_url, stream=True)
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            with open("downloaded_video.mp4", "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print("Video saved as 'downloaded_video.mp4'")
        else:
            print(f"Failed to fetch video. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# Replace this URL with the Instagram video URL you're testing
video_url = "https://www.instagram.com/reel/DD1S0mtPKl0/?utm_source=ig_web_copy_link"  # Example URL
fetch_video(video_url)
