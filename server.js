const express = require('express');
const multer  = require('multer');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static('public'));

app.post('/run', upload.single('image'), (req, res) => {
    const tempPath = req.file.path;
    const originalName = req.file.originalname;

const testImgDir = path.join(__dirname, 'test_img');
const finalPath = path.join(testImgDir, originalName);
const modelType = req.body.model;
const savedir = path.join(__dirname, 'results');


    // Tạo thư mục test_img nếu chưa tồn tại
    if (!fs.existsSync(testImgDir)) {
        fs.mkdirSync(testImgDir, { recursive: true });
    }
    // Tạo thư mục results nếu chưa tồn tại
    if (!fs.existsSync(savedir)) {
        fs.mkdirSync(savedir, { recursive: true });
    }

    if (!fs.existsSync(finalPath)) {
        fs.renameSync(tempPath, finalPath);
    } else {
        fs.unlink(tempPath, () => {});
    }


    let cmd = '';
    if (modelType === 'yolov5') {
        cmd = `python ${path.join(__dirname, 'modelv5.py')} --weights ${path.join(__dirname, 'runs_yolov5', 'train_yolov5s', 'weights', 'best.pt')} --image "${finalPath}" --savedir "${savedir}"`;
    }
    else if (modelType === 'yolov5_half') {
        cmd = `python ${path.join(__dirname, 'modelv5.py')} --weights ${path.join(__dirname, 'v5halfv2', 'yolov5_half_train', 'weights', 'best.pt')} --image "${finalPath}" --savedir "${savedir}"`;
    }
    else if (modelType === 'yolov8') {
        cmd = `python ${path.join(__dirname, 'model.py')} --weights ${path.join(__dirname, 'runs', 'detect', 'train2', 'weights', 'best.pt')} --image "${finalPath}" --savedir "${savedir}"`;
    }
    else if (modelType === 'yolov8_half') {
        cmd = `python ${path.join(__dirname, 'model.py')} --weights ${path.join(__dirname, 'v8half', 'best.pt')} --image "${finalPath}" --savedir "${savedir}"`;
    }
    else if (modelType === 'yolov11') {
        cmd = `python ${path.join(__dirname, 'modelv11.py')} --weights ${path.join(__dirname, 'v11', 'best.pt')} --image "${finalPath}" --savedir "${savedir}"`;
    }
    else {
        return res.status(400).send("Model không hợp lệ.");
    }

    exec(cmd, (err, stdout, stderr) => {
        if (err) {
            console.error("Lỗi khi chạy mô hình:", stderr);
            return res.status(500).send("Lỗi khi chạy mô hình");
        }

        const resultImgPath = path.join(savedir, 'predict', originalName);
        let logPath = null;

        // Xử lý log path cho tất cả models
        const lines = stdout.trim().split('\n');
        const logLine = lines.find(line => line.includes('.txt') && line.includes('log_'));
        logPath = logLine?.trim();

        if (!logPath || !fs.existsSync(logPath)) {
            console.error("Không tìm thấy log:", logPath);
            return res.status(500).send("Không tìm thấy file log");
        }

        fs.readFile(resultImgPath, (err, imgData) => {
            if (err) return res.status(500).send("Không đọc được ảnh kết quả");

            fs.readFile(logPath, 'utf8', (err, logContent) => {
                if (err) return res.status(500).send("Không đọc được log");
                console.log(`Ảnh: ${originalName}`);
                console.log(`Model: ${modelType}`);
                console.log(logContent);
                res.json({
                    image: imgData.toString('base64'),
                    log: logContent,
                    model: modelType
                });
            });
        });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
