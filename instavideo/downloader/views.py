import os
import instaloader
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Initialize Instaloader instance
L = instaloader.Instaloader()

@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the JSON body
            video_url = data.get('url')  # Get URL from the frontend
            
            # Handle if no URL is provided
            if not video_url:
                return JsonResponse({'error': 'No URL provided'}, status=400)
            
            # Download the video
            post = instaloader.Post.from_shortcode(L.context, video_url.split("/")[-2])
            video_file_path = f'./downloads/{post.shortcode}.mp4'
            L.download_post(post, target=video_file_path)

            # Return the path where the video is saved
            return JsonResponse({'video_url': video_file_path})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
