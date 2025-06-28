# Fix CORS Issue

## Problem
Your backend is running in DEBUG mode and has CORS issues with your Vercel frontend.

## Solution

### 1. Update Render Environment Variables

Go to your Render dashboard: https://dashboard.render.com

1. Find your `insta-video-downloader-backend` service
2. Click on it
3. Go to "Environment" tab
4. Add/update these environment variables:

```
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=insta-video-downloader-backend-7ya3.onrender.com
CORS_ALLOWED_ORIGINS=https://insta-video-downloader-apgk.vercel.app
```

### 2. Redeploy Backend

After updating the environment variables:
1. Go to "Manual Deploy" tab
2. Click "Deploy latest commit"
3. Wait for deployment to complete

### 3. Test

After redeployment, test your frontend again. The CORS issue should be resolved.

## Alternative Quick Fix

If you want to keep DEBUG=True for now, you can temporarily allow all origins:

```
CORS_ALLOW_ALL_ORIGINS=True
```

But this is not recommended for production. 