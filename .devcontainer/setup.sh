#!/bin/bash

echo "🚀 Setting up YOLO Detection Server in GitHub Codespaces..."

# Update system
echo "📦 Updating system packages..."
sudo apt-get update

# Install system dependencies for OpenCV
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libgtk-3-0 \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Create required directories
echo "📁 Creating required directories..."
mkdir -p test_img results/predict results/logs results/labels uploads

# Set permissions
chmod +x start.sh

echo "✅ Setup completed successfully!"
echo ""
echo "🌐 To start the server, run:"
echo "   npm start"
echo ""
echo "🔗 The server will be available at:"
echo "   http://localhost:3000"
echo ""
echo "📁 Upload images to test_img/ folder"
echo "📊 Results will be saved to results/ folder"
