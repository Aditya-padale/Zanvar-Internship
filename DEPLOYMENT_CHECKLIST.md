# Vercel Deployment Checklist ✅

Use this checklist to ensure your deployment is successful:

## Pre-Deployment Setup

### 1. Repository Setup
- [ ] Code is pushed to GitHub repository
- [ ] All sensitive data (API keys) are removed from code
- [ ] `.env` files are in `.gitignore`
- [ ] `.vercelignore` file is present

### 2. Configuration Files
- [ ] `vercel.json` is configured correctly
- [ ] `requirements.txt` contains all necessary Python packages
- [ ] Frontend `package.json` has `vercel-build` script
- [ ] API functions are in `/api` directory

### 3. Environment Variables
- [ ] `GOOGLE_API_KEY` obtained from Google AI Studio
- [ ] `.env.example` file created for reference
- [ ] Environment variables documented

## Deployment Steps

### 4. Vercel Account Setup
- [ ] Vercel account created at vercel.com
- [ ] GitHub connected to Vercel
- [ ] Project imported from GitHub

### 5. Build Configuration
- [ ] **Framework Preset**: Other
- [ ] **Root Directory**: `/` (leave blank)
- [ ] **Build Command**: `cd frontend && npm install && npm run build`
- [ ] **Output Directory**: `frontend/dist`

### 6. Environment Variables in Vercel
- [ ] `GOOGLE_API_KEY` added in Vercel dashboard
- [ ] Variables marked as production/preview appropriately

### 7. API Functions
- [ ] All API functions deploy without errors
- [ ] Python dependencies install successfully
- [ ] Functions are accessible at `/api/*` routes

## Post-Deployment Testing

### 8. Frontend Verification
- [ ] Website loads correctly
- [ ] Navigation works between pages
- [ ] UI components render properly
- [ ] API status indicator shows correct status

### 9. API Testing
- [ ] Health check: `GET /api/health`
- [ ] File upload: `POST /api/upload`
- [ ] Chat functionality: `POST /api/chat`
- [ ] Chart generation: `POST /api/charts` (if implemented)

### 10. Integration Testing
- [ ] File upload from frontend works
- [ ] Chat messages send successfully
- [ ] Error handling works correctly
- [ ] Charts display properly (if implemented)

## Performance & Monitoring

### 11. Performance Check
- [ ] Page load times are acceptable
- [ ] API response times are reasonable
- [ ] Serverless functions cold start quickly

### 12. Monitoring Setup
- [ ] Vercel dashboard monitoring configured
- [ ] Function logs are accessible
- [ ] Error tracking is working

## Troubleshooting Common Issues

### Build Errors
- [ ] Check Vercel build logs
- [ ] Verify all dependencies are listed
- [ ] Ensure Python version compatibility

### API Errors
- [ ] Check function logs in Vercel dashboard
- [ ] Verify environment variables are set
- [ ] Test API endpoints individually

### Frontend Issues
- [ ] Check browser console for errors
- [ ] Verify API base URL is correct for production
- [ ] Test in different browsers

## Security Review

### 13. Security Checklist
- [ ] API keys are not exposed in frontend
- [ ] CORS is configured properly
- [ ] No sensitive data in client-side code
- [ ] Environment variables are secure

## Documentation

### 14. Documentation Complete
- [ ] README.md updated with deployment info
- [ ] API documentation is current
- [ ] Environment setup instructions clear
- [ ] Troubleshooting guide available

## Final Verification

### 15. End-to-End Test
- [ ] Complete user workflow works
- [ ] Data upload → Analysis → Visualization
- [ ] All features function as expected
- [ ] Performance is satisfactory

---

## Quick Commands for Testing

### Test API Health
```bash
curl https://your-app.vercel.app/api/health
```

### Test File Upload
```bash
curl -X POST https://your-app.vercel.app/api/upload \
  -F "file=@sample.csv"
```

### Test Chat
```bash
curl -X POST https://your-app.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, can you help me analyze data?"}'
```

---

## Need Help?

- 📖 [Vercel Documentation](https://vercel.com/docs)
- 💬 [Vercel Community](https://github.com/vercel/vercel/discussions)
- 🐛 [Report Issues](https://github.com/vercel/vercel/issues)

---

**Date Completed**: ________________
**Deployed URL**: ________________
**Notes**: ________________
