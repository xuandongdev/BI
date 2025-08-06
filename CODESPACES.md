# 🚀 GitHub Codespaces - YOLO Detection Server

This repository is configured to run in GitHub Codespaces with all dependencies pre-installed.

## 🎯 Quick Start in Codespaces

1. **Create Codespace:**
   - Go to your GitHub repository
   - Click the green **"Code"** button
   - Select **"Codespaces"** tab
   - Click **"Create codespace on main"**

2. **Wait for Setup:**
   - Codespace will automatically install all dependencies
   - This takes ~3-5 minutes on first run

3. **Start Server:**
   ```bash
   npm start
   ```

4. **Access Web Interface:**
   - VS Code will automatically forward port 3000
   - Click on the **"Open in Browser"** notification
   - Or go to **Ports** tab and click the globe icon

## 📊 Features Available in Codespaces

- ✅ **Full YOLO Detection** - All models supported
- ✅ **Web Interface** - Upload and process images
- ✅ **60 hours/month** - Free tier
- ✅ **Auto-save** - Your work is saved automatically
- ✅ **VS Code** - Full IDE experience

## 🔧 Development Commands

```bash
# Start server
npm start

# Start with auto-reload
npm run dev

# Check Python environment
python --version
pip list

# Test image processing (if models available)
python model.py --help
```

## 📁 File Structure

```
/workspaces/BI/
├── server.js          # Main server file
├── public/            # Web interface
├── test_img/          # Upload images here
├── results/           # Detection results
├── models/            # YOLO model files (.pt)
└── .devcontainer/     # Codespaces configuration
```

## ⚠️ Important Notes

1. **Model Files:** Make sure your `.pt` model files are in the repo
2. **Free Limits:** 60 hours/month on free GitHub account
3. **Data Persistence:** Files are saved between sessions
4. **Internet Access:** Required for first-time dependency installation

## 🛠️ Troubleshooting

### Server won't start?
```bash
# Check dependencies
npm install
pip install -r requirements.txt

# Create directories
mkdir -p test_img results/predict results/logs results/labels uploads
```

### Port not accessible?
- Check the **Ports** tab in VS Code
- Ensure port 3000 is forwarded
- Try accessing via the forwarded URL

### Python errors?
```bash
# Reinstall Python packages
pip install --upgrade -r requirements.txt

# Check Python path
which python
```

## 🌐 Public Access

To share your Codespace publicly:
1. Go to **Ports** tab
2. Right-click on port 3000
3. Select **"Port Visibility" → "Public"**
4. Share the generated URL

Enjoy your free YOLO detection server! 🎉
