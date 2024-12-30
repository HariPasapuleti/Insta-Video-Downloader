import logging
import os
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from instaloader import Instaloader, Post
from instavideo import settings
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import json
import instaloader

# Set up logging
logger = logging.getLogger(__name__)

class VideoDetails(APIView):
    def get(self, request, format=None):
        url = request.query_params.get('url', None)

        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Extract shortcode from the Instagram URL
            shortcode = url.split("/")[-2]
            loader = Instaloader()

            # Fetch post information
            post = Post.from_shortcode(loader.context, shortcode)

            if not post.is_video:
                return Response({"error": "The provided link does not contain a video."}, status=400)

            thumbnail_url = post.url  # Instagram post URL also serves as the thumbnail
            video_url = post.video_url  # URL to the video file

            return Response({
                "thumbnail": thumbnail_url,
                "qualities": [{"quality": "Original", "url": video_url}]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching video details: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            body = json.loads(request.body.decode('utf-8'))
            url = body.get('url')
            
            # Check if URL is provided
            if not url:
                return JsonResponse({'error': 'URL not provided'}, status=400)

            # Process URL...
            # Send the response
            return JsonResponse({'message': 'Success'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)