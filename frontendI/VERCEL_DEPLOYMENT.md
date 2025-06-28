# Vercel Deployment Guide

## Quick Deployment Steps

### 1. Deploy to Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Click "New Project"
3. Import your Git repository
4. Configure the project:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontendI`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. Click "Deploy"

### 2. Environment Variables (Optional)
After deployment, you can optionally set environment variables:
1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add: `VITE_API_URL` = `https://insta-video-downloader-backend-7ya3.onrender.com`
4. Redeploy

**Note**: The frontend is already configured to use your backend URL by default, so this step is optional.

### 3. Update Backend CORS
After getting your Vercel URL:
1. Go to your Render backend: https://dashboard.render.com
2. Add environment variable: `CORS_ALLOWED_ORIGINS` = `https://your-vercel-url.vercel.app`
3. Redeploy the backend

### 4. Test
Visit your Vercel URL and test the Instagram video downloader!

## Troubleshooting
- If you get environment variable errors, just deploy without setting any environment variables
- The frontend will automatically use the production backend URL 