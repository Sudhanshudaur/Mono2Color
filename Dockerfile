# Use Python 3.10 for better compatibility
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY pts_in_hull.npy .
COPY templates/ templates/
COPY models/ models/

# Expose port
EXPOSE 5000

# Environment variables
ENV PYTHONUNBUFFERED=1

# Run application
CMD ["python", "app.py"]