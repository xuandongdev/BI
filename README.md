# YOLO Traffic Detection Server

Web application for traffic detection using multiple YOLO models (YOLOv5, YOLOv8, YOLOv11).

## Features
- Support multiple YOLO versions
- Web interface for image upload
- Real-time detection results
- Model comparison

## Deploy to Render.com

1. **Fork this repository**
2. **Sign up at [render.com](https://render.com)**
3. **Create new Web Service**
   - Connect your GitHub repository
   - Select this repo
   - Render will automatically detect `render.yaml`
4. **Deploy!**
   - Build time: ~5-10 minutes (installing AI libraries)
   - Your app will be available at: `https://your-app.onrender.com`

## Local Development

```bash
npm install
pip install -r requirements.txt
npm start
```

Open http://localhost:3000

## Models Required

Make sure you have these model files:
- `v11/best.pt` (YOLOv11)
- `v8half/best.pt` (YOLOv8 Half)
- `v5halfv2/yolov5_half_train/weights/best.pt` (YOLOv5 Half)
- `runs/detect/train2/weights/best.pt` (YOLOv8)
- `runs_yolov5/train_yolov5s/weights/best.pt` (YOLOv5)

## Note
- Free tier on Render has limitations
- Model files should be < 100MB each
- First request may take 30-60 seconds (cold start)
