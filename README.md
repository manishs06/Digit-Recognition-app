# 🎨 AI Digit Recognition Web App

Draw any digit (0-9) on the interactive canvas and watch our deep learning model predict it in real-time with impressive accuracy! This project uses a neural network trained on the MNIST dataset, optimized with ONNX Runtime for fast and lightweight inference on the web.

## 🌐 Live Demo

🔗 **[Try it live on Render!](https://digit-recognition-app-xzwb.onrender.com)**



## 🧠 How It Works

1. **Draw**: You draw a digit on the interactive HTML5 canvas.
2. **Process**: The drawing is captured as an image and sent to our Python backend.
3. **Analyze**: A deep neural network (trained on the MNIST dataset) analyzes the image using **ONNX Runtime** for lightning-fast inference.
4. **Predict**: The model identifies the digit and returns its prediction along with a confidence score.

## 📁 Project Structure

```
Digit-Recognition-app/
├── app.py                  # Flask production server (Render/Local)
├── public/                 # Static web assets
│   └── index.html          # Main interface
├── static/                 # CSS and JS files
├── model.onnx              # Optimized AI model (~470KB)
├── render.yaml             # Render deployment configuration
├── requirements.txt        # Production dependencies
└── README.md               # Project documentation
```