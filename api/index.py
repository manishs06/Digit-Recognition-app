from flask import Flask, request, jsonify, send_from_directory
import base64
import os
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__, static_folder='../static', template_folder='../templates')

# Load model
model_path = os.path.join(os.path.dirname(__file__), '..', 'model.h5')
model = tf.keras.models.load_model(model_path)

@app.route("/")
def index():
    return send_from_directory('../public', 'index.html')

@app.route("/api/predict-digit", methods=["POST", "GET"])
def predict_digit():
    try:
        image = request.get_json(silent=True)['image'].split(",")[1]
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
        input_data = image.astype(np.float32)
        values = model.predict(input_data)
        value = np.argmax(values)
        
        # Get confidence as percentage
        confidence = float(np.max(values)) * 100
        
        response = { 
            "prediction": str(value),
            "confidence": f"{confidence:.2f}"
        }

        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Vercel serverless function handler
def handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()
