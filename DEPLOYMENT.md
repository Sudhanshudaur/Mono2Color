# Mono2Color - Deployment Guide

## 🚀 Deploy to Render

### Prerequisites
- GitHub account
- Render account (free tier available at [render.com](https://render.com))

### Deployment Steps

#### 1. Push to GitHub
```bash
# Initialize git repository (if not already done)
git init

# Create .gitignore
echo "__pycache__/
*.pyc
*.jpg
*.png
*.gif
.ipynb_checkpoints/
*.ipynb
GUI.py
image_colarization.py
venv/
env/" > .gitignore

# Add and commit files
git add .
git commit -m "Initial commit - Mono2Color app"

# Push to GitHub
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### 2. Deploy on Render

**Option A: Using render.yaml (Recommended)**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml` and configure your service
5. Click "Apply" to deploy

**Option B: Manual Setup**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** mono2color
   - **Environment:** Docker
   - **Region:** Oregon (or nearest)
   - **Branch:** main
   - **Plan:** Free
5. Click "Create Web Service"

#### 3. Wait for Deployment
- First deployment takes 5-10 minutes
- Render will build the Docker image and start the service
- You'll get a URL like: `https://mono2color.onrender.com`

### Environment Variables (Optional)
No additional environment variables needed. The app auto-configures with Render's PORT variable.

### Important Notes

⚠️ **Free Tier Limitations:**
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30-60 seconds (cold start)
- 750 hours/month free

💡 **Tips:**
- Model files are included in the Docker image
- No persistent storage needed (all processing is in-memory)
- For production use, consider upgrading to a paid plan

## 🐳 Local Docker Testing

Test the Docker build locally before deploying:

```bash
# Build the image
docker build -t mono2color .

# Run the container
docker run -p 5000:5000 mono2color

# Access at http://localhost:5000
```

## 📊 File Structure for Deployment

Required files:
```
├── app.py                          # Flask application
├── Dockerfile                      # Docker configuration
├── requirements.txt                # Python dependencies
├── render.yaml                     # Render configuration
├── .dockerignore                   # Files to exclude from Docker
├── templates/
│   └── index.html                  # Frontend
├── models/
│   ├── colorization_deploy_v2.prototxt
│   └── colorization_release_v2.caffemodel
└── pts_in_hull.npy                 # Color cluster centers
```

## 🔧 Troubleshooting

### Build Fails
- Check that all model files exist in `models/` directory
- Ensure `pts_in_hull.npy` is in the root directory
- Verify `requirements.txt` versions

### App Crashes
- Check Render logs in dashboard
- Common issue: Missing model files
- Increase timeout if images are large

### Slow Performance
- Free tier has limited resources
- First request after cold start is slow
- Consider upgrading for consistent performance

## 📝 Local Development

Run locally without Docker:
```bash
pip install -r requirements.txt
python app.py
```

Access at http://localhost:5000

## 🎨 Features
- ✅ No file storage (all in-memory)
- ✅ Docker optimized
- ✅ Production-ready with gunicorn
- ✅ Render deployment ready
- ✅ Beautiful responsive UI
