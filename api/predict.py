from flask import Flask, request, jsonify
import base64
import os
import sys
import numpy as np
from PIL import Image
import io

# Add parent directory to path to access model
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

app = Flask(__name__)

# Global model variable
model = None

def load_model():
    """Load the TensorFlow model lazily"""
    global model
    if model is None:
        try:
            import tensorflow as tf
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.h5')
            model = tf.keras.models.load_model(model_path)
            print("Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return model

@app.route('/api/predict-digit', methods=['POST', 'OPTIONS'])
def predict_digit():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Load model
        model = load_model()
        
        # Get image data
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        image = data['image'].split(",")[1]
        image_data = base64.urlsafe_b64decode(image)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert the RGB image to grayscale image
        image = image.convert("L")

        # Resize the image to 28x28
        image = image.resize((28, 28))

        # Convert the image into numpy array
        image = np.array(image)

        # Reshape the image for the model
        image = image.reshape(1, 28, 28) 

        # Normalize the pixel values in image
        image = image / 255.

        # Set the datatype of image as float32
        image = image.astype(np.float32)
        
        # Make prediction
        values = model.predict(image, verbose=0)
        value = np.argmax(values)
        
        # Get confidence as percentage
        confidence = float(np.max(values)) * 100
        
        response = { 
            "prediction": str(value),
            "confidence": f"{confidence:.2f}"
        }

        return jsonify(response)
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return jsonify({"error": str(e)}), 500

# Vercel serverless handler
def handler(event, context):
    """Vercel serverless function handler"""
    return app(event, context)
