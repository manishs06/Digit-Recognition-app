# 🎨 AI Digit Recognition Web App

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/manishs06/Digit-Recognition-app)

A stunning, modern web application for handwritten digit recognition powered by deep learning. Draw any digit (0-9) on the canvas and watch our neural network predict it in real-time with impressive accuracy!

## 🌐 Live Demo

🔗 **[Try it live on Vercel!](#)** _(Deploy to get your own link!)_

![Digit Recognition Demo](cover.jpeg)

## ✨ Features

- 🎯 **Real-time Prediction** - Instant digit recognition using TensorFlow neural networks
- 🎨 **Interactive Canvas** - Smooth drawing experience with adjustable brush size
- 📊 **Confidence Scores** - See how confident the AI is about its predictions
- 🎉 **Confetti Effects** - Celebratory animations for high-confidence predictions
- 📱 **Fully Responsive** - Works seamlessly on desktop, tablet, and mobile devices
- 🌙 **Premium Dark UI** - Beautiful glassmorphism design with gradient effects
- ⌨️ **Keyboard Shortcuts** - Press 'C' to clear, 'Enter' to predict
- 🎭 **Smooth Animations** - Engaging micro-interactions throughout the interface

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/manishs06/Digit-Recognition-app.git
   cd Digit-Recognition-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

That's it! 🎉 Start drawing digits and see the magic happen!

## 🧠 How It Works

### The Neural Network

The application uses a deep neural network trained on the famous **MNIST dataset** containing 60,000+ handwritten digits.

**Architecture:**
- **Input Layer**: 28x28 pixel grayscale images (flattened)
- **Hidden Layer 1**: 128 neurons with ReLU activation
- **Hidden Layer 2**: 128 neurons with ReLU activation
- **Output Layer**: 10 neurons with Softmax activation (one for each digit 0-9)

**Training Details:**
- Optimizer: Adam
- Loss Function: Sparse Categorical Crossentropy
- Training Epochs: 10
- Accuracy: ~98% on test data

### The Process

1. **Draw**: User draws a digit on the HTML5 canvas
2. **Capture**: Canvas image is converted to base64 and sent to the backend
3. **Preprocess**: Image is converted to grayscale, resized to 28x28, and normalized
4. **Predict**: The trained model processes the image and outputs probabilities
5. **Display**: The predicted digit and confidence score are shown with beautiful animations

## 📁 Project Structure

```
Digit-Recognition-app/
├── app.py                 # Flask backend server
├── model.h5              # Pre-trained TensorFlow model
├── train.py              # Model training script
├── test.py               # Model testing script
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html       # Main HTML template
├── static/
│   ├── style.css        # Premium styling with animations
│   └── script.js        # Interactive canvas and API integration
└── README.md            # This file
```

## 🎮 Usage Guide

### Drawing on Canvas

- **Mouse**: Click and drag to draw
- **Touch**: Works on touch devices (tablets, phones)
- **Brush Size**: Adjust the slider to change brush thickness
- **Clear**: Click "Clear Canvas" or press 'C' key

### Making Predictions

1. Draw a digit on the black canvas
2. Click "Predict Digit" or press 'Enter'
3. Watch the AI analyze your drawing
4. See the predicted digit with confidence score
5. High confidence (>90%) triggers confetti! 🎊

## 🛠️ Technology Stack

### Backend
- **Flask** - Lightweight Python web framework
- **TensorFlow** - Deep learning framework
- **NumPy** - Numerical computing
- **Pillow** - Image processing

### Frontend
- **HTML5 Canvas** - Drawing interface
- **Vanilla CSS** - Premium styling with gradients and animations
- **Vanilla JavaScript** - Interactive functionality
- **Google Fonts** - Inter & JetBrains Mono typography

## 🎨 Design Features

- **Glassmorphism** - Frosted glass effect on cards
- **Gradient Backgrounds** - Dynamic color transitions
- **Micro-animations** - Smooth hover effects and transitions
- **Particle Effects** - Floating background particles
- **Confetti Celebration** - For high-confidence predictions
- **Responsive Layout** - Adapts to all screen sizes

## 📊 Model Performance

The neural network achieves approximately **98% accuracy** on the MNIST test dataset, making it highly reliable for recognizing handwritten digits.

## 🔧 Advanced Usage

### Retrain the Model

If you want to retrain the model with different parameters:

```bash
python train.py
```

This will:
- Download the MNIST dataset
- Train a new model
- Save it as `model.h5`
- Display accuracy and loss metrics

### Test the Model

To test the model on sample data:

```bash
python test.py
```

## 🌐 Deployment

### Deploy to Vercel (Recommended) ⚡

The easiest way to deploy this app is using Vercel:

#### Option 1: One-Click Deploy

Click the button below to deploy to Vercel:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/manishs06/Digit-Recognition-app)

#### Option 2: Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd Digit-Recognition
vercel

# Deploy to production
vercel --prod
```

**📖 For detailed deployment instructions, see [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)**

### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Add `gunicorn` to `requirements.txt`

3. Deploy:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Deploy to Other Platforms

The app can also be deployed to:
- **Railway** - Similar to Heroku
- **Render** - Free tier available
- **PythonAnywhere** - Python-specific hosting
- **AWS Lambda** - Serverless deployment

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- Add support for multiple digits in one image
- Implement drawing history/undo functionality
- Add model comparison (different architectures)
- Create a mobile app version
- Add user accounts and drawing gallery

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Manish Singh**
- GitHub: [@manishs06](https://github.com/manishs06)

## 🙏 Acknowledgments

- **MNIST Dataset** - Yann LeCun and collaborators
- **TensorFlow Team** - For the amazing deep learning framework
- **Flask Community** - For the excellent web framework

## 📸 Screenshots

### Main Interface
Beautiful dark-themed interface with interactive canvas and real-time predictions.

### Prediction Results
Instant feedback with confidence scores and smooth animations.

### Mobile Responsive
Works perfectly on all devices with touch support.

---

**Built with ❤️ using TensorFlow & Flask**

⭐ Star this repo if you found it helpful!

## 🐛 Troubleshooting

### Common Issues

**Issue**: Model file not found
- **Solution**: Ensure `model.h5` is in the root directory. Run `train.py` to generate it.

**Issue**: TensorFlow installation fails
- **Solution**: Try installing with: `pip install tensorflow-cpu` for CPU-only version

**Issue**: Canvas not responding
- **Solution**: Clear browser cache and ensure JavaScript is enabled

**Issue**: Predictions are inaccurate
- **Solution**: Try drawing larger, centered digits. The model expects MNIST-style digits.

## 📚 Learn More

- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
- [Neural Networks Explained](https://www.youtube.com/watch?v=aircAruvnKk)

---

**Happy Drawing! 🎨✨**

# Smile-detection