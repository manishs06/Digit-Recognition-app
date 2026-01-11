from flask import Flask, request, jsonify
import base64
import os
import sys
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Global model variables
interpreter = None
input_details = None
output_details = None

def load_model():
    """Load the TFLite model lazily"""
    global interpreter, input_details, output_details
    if interpreter is None:
        try:
            # Try importing tflite_runtime first (preferred for small size)
            try:
                import tflite_runtime.interpreter as tflite
            except ImportError:
                # Fallback to full tensorflow if available (local development)
                try:
                    import tensorflow.lite as tflite
                except ImportError:
                    import tensorflow as tf
                    tflite = tf.lite

            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.tflite')
            if not os.path.exists(model_path):
                # Fallback check in same directory
                model_path = os.path.join(os.path.dirname(__file__), 'model.tflite')
            
            interpreter = tflite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()
            
            input_details = interpreter.get_input_details()
            output_details = interpreter.get_output_details()
            
            print("TFLite Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return interpreter

@app.route('/api/predict-digit', methods=['POST', 'OPTIONS'])
def predict_digit():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Load model/interpreter
        load_model()
        
        # Get image data
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        image_str = data['image'].split(",")[1]
        image_data = base64.urlsafe_b64decode(image_str)
        image = Image.open(io.BytesIO(image_data))
        
        # Preprocessing (same as before)
        image = image.convert("L")
        image = image.resize((28, 28))
        image = np.array(image)
        
        # TFLite specific: Check if input needs 4D (1, 28, 28, 1) or 3D (1, 28, 28)
        # Most MNIST models are (1, 28, 28, 1) or (1, 784)
        input_shape = input_details[0]['shape']
        
        if len(input_shape) == 4:
            # (1, 28, 28, 1)
            image = image.reshape(1, 28, 28, 1)
        else:
            # (1, 28, 28)
            image = image.reshape(1, 28, 28) 

        image = image / 255.0
        image = image.astype(np.float32)
        
        # Run inference
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        
        # Get results
        output_data = interpreter.get_tensor(output_details[0]['index'])
        prediction = int(np.argmax(output_data[0]))
        confidence = float(np.max(output_data[0])) * 100
        
        response = { 
            "prediction": str(prediction),
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
