# Mono2Color - AI-Powered Black & White Image Colorizer

Transform black & white images into vibrant colors using deep learning!

## 🎨 Features
- Beautiful modern web interface
- No file storage - all processing in-memory
- Docker-ready for easy deployment
- Optimized for Render cloud platform
- Fast colorization using Caffe deep learning model

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open in browser
http://localhost:5000
```

### Docker
```bash
# Build and run
docker build -t mono2color .
docker run -p 5000:5000 mono2color
```

### Deploy to Render
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📁 Project Structure
```
├── app.py                  # Flask backend
├── Dockerfile             # Docker configuration
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment config
├── templates/
│   └── index.html        # Web interface
├── models/               # Pre-trained colorization model
└── pts_in_hull.npy      # Color cluster centers
```

## 🛠️ Technology Stack
- **Backend**: Flask + OpenCV + NumPy
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Model**: Caffe deep learning network
- **Deployment**: Docker + Gunicorn

## 📝 How It Works
1. Upload a black & white image
2. AI model processes the luminance channel
3. Predicts color channels using deep learning
4. Returns colorized image instantly

## 📄 License
Open source - feel free to use and modify!


