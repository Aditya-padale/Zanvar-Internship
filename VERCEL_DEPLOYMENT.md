# Vercel Deployment Guide

This guide will help you deploy your Data Analysis website to Vercel serverless platform.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Environment Variables**: You'll need a Google AI API key

## Project Structure for Vercel

The project has been restructured for Vercel deployment:

```
├── api/                          # Serverless API functions
│   ├── upload.py                # File upload endpoint
│   ├── chat.py                  # Chat/AI endpoint  
│   ├── charts.py                # Chart creation endpoint
│   ├── health.py                # Health check endpoint
│   └── serverless_analyzer.py   # Simplified analyzer for serverless
├── frontend/                     # React frontend
│   ├── src/
│   ├── package.json
│   └── dist/                    # Built files (generated)
├── vercel.json                  # Vercel configuration
├── requirements.txt             # Python dependencies for API
└── .env.example                # Environment variables template
```

## Environment Variables

Set these in your Vercel dashboard:

1. **GOOGLE_API_KEY**: Your Google AI API key
   - Get it from [Google AI Studio](https://ai.google.dev/)
   - Required for AI-powered features

2. **VERCEL**: Automatically set by Vercel (don't add manually)

## Deployment Steps

### Option 1: Deploy via Vercel Dashboard

1. **Connect Repository**:
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository

2. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: Leave blank (/)
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`

3. **Set Environment Variables**:
   - In project settings, add `GOOGLE_API_KEY`

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete

### Option 2: Deploy via CLI

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy from project root**:
   ```bash
   vercel
   ```

4. **Set environment variables**:
   ```bash
   vercel env add GOOGLE_API_KEY
   ```

## API Endpoints

Once deployed, your API will be available at:

- `https://your-app.vercel.app/api/health` - Health check
- `https://your-app.vercel.app/api/upload` - File upload
- `https://your-app.vercel.app/api/chat` - AI chat
- `https://your-app.vercel.app/api/charts` - Chart creation

## Frontend

The React frontend will be served from:
- `https://your-app.vercel.app/` - Main application

## Configuration Files

### vercel.json
Configures how Vercel builds and routes your application:
- Routes API calls to serverless functions
- Serves frontend as static files
- Sets Python runtime for API functions

### requirements.txt
Lists Python dependencies for serverless functions. Keep minimal for faster cold starts.

## Local Development

For local development with the new structure:

1. **Frontend** (Terminal 1):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

2. **Backend** (Terminal 2):
   ```bash
   cd backend
   python app.py
   ```

## Troubleshooting

### Build Errors
- Check that all Python dependencies are compatible with Vercel
- Ensure frontend builds successfully locally first

### API Errors
- Check Vercel function logs in dashboard
- Verify environment variables are set
- Test API endpoints individually

### Frontend Issues
- Check that `VITE_API_BASE` is not set in production
- Verify API calls use relative paths in production

## Performance Optimization

1. **Serverless Functions**:
   - Keep dependencies minimal
   - Use caching where possible
   - Optimize import statements

2. **Frontend**:
   - Enable Vite build optimizations
   - Use lazy loading for components
   - Optimize images and assets

## Monitoring

Monitor your deployment:
- **Vercel Dashboard**: Function invocations, errors, performance
- **Browser DevTools**: Frontend performance and API calls
- **Health Endpoint**: `GET /api/health` for service status

## Cost Considerations

Vercel Hobby Plan includes:
- 100GB bandwidth
- 100GB-hours of serverless function execution
- 6,000 function invocations per day

For higher usage, consider upgrading to Pro plan.

## Security

- Never commit API keys to repository
- Use environment variables for sensitive data
- Enable CORS properly for production domain
- Consider rate limiting for API endpoints

## Support

If you encounter issues:
1. Check Vercel documentation
2. Review function logs in Vercel dashboard
3. Test API endpoints with curl/Postman
4. Verify environment variables are set correctly
