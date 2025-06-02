import logging
import os
import requests
import tempfile
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
import re
import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# Set up logging with more detailed format
logging.basicConfig(level=logging.INFO)
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

def extract_shortcode(url):
    # Handle different Instagram URL formats
    patterns = [
        r'instagram.com/reel/([^/?]+)',  # Reel format
        r'instagram.com/p/([^/?]+)',     # Post format
        r'instagram.com/tv/([^/?]+)'     # TV format
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_frame(video_url):
    try:
        logger.info(f"Attempting to get video frame from URL: {video_url}")
        
        # Download video to temporary file
        response = requests.get(video_url, stream=True)
        if response.status_code != 200:
            logger.error(f"Failed to download video. Status code: {response.status_code}")
            return None

        with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file_path = temp_file.name
            logger.info(f"Video downloaded to temporary file: {temp_file_path}")

        # Open video file
        cap = cv2.VideoCapture(temp_file_path)
        if not cap.isOpened():
            logger.error("Failed to open video file with OpenCV")
            return None

        # Read first frame
        ret, frame = cap.read()
        cap.release()

        # Clean up temporary file
        os.unlink(temp_file_path)
        logger.info("Temporary file cleaned up")

        if not ret:
            logger.error("Failed to read frame from video")
            return None

        # Convert frame to JPEG
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            logger.error("Failed to encode frame to JPEG")
            return None

        # Convert to base64
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')
        base64_url = f"data:image/jpeg;base64,{jpg_as_text}"
        logger.info(f"Generated base64 URL (first 50 chars): {base64_url[:50]}...")
        return base64_url

    except Exception as e:
        logger.error(f"Error getting video frame: {str(e)}")
        return None

def get_thumbnail_data(url):
    try:
        logger.info(f"Fetching thumbnail from URL: {url}")
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            logger.error(f"Failed to fetch thumbnail. Status code: {response.status_code}")
            return None
            
        # Convert the image to base64
        image_data = response.content
        base64_data = base64.b64encode(image_data).decode('utf-8')
        mime_type = response.headers.get('content-type', 'image/jpeg')
        return f"data:{mime_type};base64,{base64_data}"
    except Exception as e:
        logger.error(f"Error fetching thumbnail: {str(e)}")
        return None

@csrf_exempt
def download_video(request):
    if request.method == 'POST':
        try:
            # Parse JSON body
            body = json.loads(request.body.decode('utf-8'))
            url = body.get('url')
            logger.info(f"Received request for URL: {url}")
            
            # Check if URL is provided
            if not url:
                return JsonResponse({'error': 'URL not provided'}, status=400)

            # Extract shortcode from URL
            shortcode = extract_shortcode(url)
            if not shortcode:
                logger.error(f"Invalid Instagram URL: {url}")
                return JsonResponse({'error': 'Invalid Instagram URL'}, status=400)

            logger.info(f"Extracted shortcode: {shortcode}")

            # Initialize Instaloader
            loader = Instaloader()
            
            try:
                # Get post information
                post = Post.from_shortcode(loader.context, shortcode)
                logger.info("Successfully retrieved post information")
                
                if not post.is_video:
                    logger.error("Post does not contain a video")
                    return JsonResponse({'error': 'The provided link does not contain a video'}, status=400)
                
                # Get video URL and thumbnail
                video_url = post.video_url
                logger.info(f"Video URL: {video_url}")
                
                # Get thumbnail URL - try multiple methods
                thumbnail_url = None
                if hasattr(post, 'display_url'):
                    thumbnail_url = post.display_url
                    logger.info(f"Found display_url: {thumbnail_url}")
                elif hasattr(post, 'thumbnail_url'):
                    thumbnail_url = post.thumbnail_url
                    logger.info(f"Found thumbnail_url: {thumbnail_url}")
                elif hasattr(post, 'url'):
                    thumbnail_url = post.url
                    logger.info(f"Found url: {thumbnail_url}")
                
                # Convert thumbnail URL to base64 data
                if thumbnail_url:
                    logger.info("Converting thumbnail to base64")
                    thumbnail_data = get_thumbnail_data(thumbnail_url)
                    if thumbnail_data:
                        thumbnail_url = thumbnail_data
                        logger.info("Successfully converted thumbnail to base64")
                    else:
                        logger.error("Failed to convert thumbnail to base64")
                        # Try getting video frame as fallback
                        thumbnail_url = get_video_frame(video_url)
                else:
                    # If no thumbnail URL found, get first frame of video
                    logger.info("No thumbnail URL found, attempting to get video frame")
                    thumbnail_url = get_video_frame(video_url)
                    if thumbnail_url:
                        logger.info("Successfully got video frame as thumbnail")
                    else:
                        logger.error("Failed to get video frame")
                
                # Get caption and truncate it
                caption = post.caption if post.caption else ''
                if caption:
                    # Split by newlines and take first line
                    caption = caption.split('\n')[0]
                    # Truncate if too long
                    if len(caption) > 100:
                        caption = caption[:97] + '...'
                logger.info(f"Caption: {caption}")
                
                # Create response with video URL and thumbnail
                response_data = {
                    'message': video_url,
                    'caption': caption
                }
                
                if thumbnail_url:
                    response_data['thumbnail'] = thumbnail_url
                    logger.info("Added thumbnail to response")
                else:
                    logger.warning("No thumbnail available")
                
                return JsonResponse(response_data)
                
            except instaloader.exceptions.InstaloaderException as e:
                logger.error(f"Instaloader error: {str(e)}")
                return JsonResponse({'error': 'Error accessing Instagram content'}, status=500)

        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)