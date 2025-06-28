# Deployment Guide

This guide will help you deploy the Instagram Video Downloader project to Render (backend) and Vercel (frontend).

## Prerequisites

### Install Dependencies Locally
Before deploying, make sure all dependencies are installed locally:

1. **Option 1: Use the installation script**
   ```bash
   python install_dependencies.py
   ```

2. **Option 2: Install manually**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test local development**
   ```bash
   cd instavideo
   python manage.py runserver
   ```

## Backend Deployment (Render)

### 1. Prepare Your Repository
- Make sure your code is pushed to a Git repository (GitHub, GitLab, etc.)
- Ensure all files are committed and pushed

### 2. Deploy to Render
1. Go to [Render.com](https://render.com) and sign up/login
2. Click "New +" and select "Web Service"
3. Connect your Git repository
4. Configure the service:
   - **Name**: `instavideo-backend` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn instavideo.wsgi:application`
   - **Root Directory**: `instavideo` (if your Django project is in a subdirectory)

### 3. Set Environment Variables
In your Render service settings, add these environment variables:
```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-render-domain.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app
```

### 4. Deploy
Click "Create Web Service" and wait for the deployment to complete.

## Frontend Deployment (Vercel)

### 1. Prepare Your Repository
- Make sure your frontend code is in the `frontendI` directory
- Ensure all files are committed and pushed

### 2. Deploy to Vercel
1. Go to [Vercel.com](https://vercel.com) and sign up/login
2. Click "New Project"
3. Import your Git repository
4. Configure the project:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontendI`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### 3. Set Environment Variables
In your Vercel project settings, add this environment variable:
```
VITE_API_URL=https://your-render-backend-url.onrender.com
```

### 4. Deploy
Click "Deploy" and wait for the deployment to complete.

## Post-Deployment

### 1. Update CORS Settings
After both deployments are complete:
1. Go to your Render backend service
2. Update the `CORS_ALLOWED_ORIGINS` environment variable with your actual Vercel frontend URL
3. Redeploy the backend service

### 2. Test the Application
1. Visit your Vercel frontend URL
2. Try downloading an Instagram video
3. Check that the backend API is working correctly

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure your frontend URL is included in the `CORS_ALLOWED_ORIGINS` environment variable
2. **Build Failures**: Check that all dependencies are listed in `requirements.txt`
3. **API Connection Issues**: Verify the `VITE_API_URL` environment variable is set correctly in Vercel
4. **ModuleNotFoundError**: Run `python install_dependencies.py` to install missing packages

### Environment Variables Reference

#### Backend (Render)
- `SECRET_KEY`: Django secret key (generate a secure one)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your Render domain
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed frontend URLs

#### Frontend (Vercel)
- `VITE_API_URL`: Your Render backend URL

## Security Notes

1. Never commit sensitive information like secret keys to your repository
2. Use environment variables for all configuration
3. Keep your dependencies updated
4. Monitor your application logs for any issues 