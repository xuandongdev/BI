#!/bin/bash

echo "🚀 Starting YOLO Detection Server..."

# Install dependencies
echo "📦 Installing Node.js dependencies..."
npm install

echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Create directories
echo "📁 Creating required directories..."
mkdir -p test_img results/predict results/logs results/labels uploads

# Start server
echo "🌐 Starting server on http://localhost:3000"
echo "Press Ctrl+C to stop"
npm start
