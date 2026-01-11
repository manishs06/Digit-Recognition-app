from flask import Flask, request, jsonify
import base64
import os
import sys
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Global ONNX session variable
session = None

def load_model():
    """Load the ONNX model lazily"""
    global session
    if session is None:
        try:
            import onnxruntime as ort
            model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.onnx')
            if not os.path.exists(model_path):
                # Fallback check in same directory
                model_path = os.path.join(os.path.dirname(__file__), 'model.onnx')
            
            # Use CPU execution provider for deployment
            session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
            print("ONNX Model loaded successfully")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise
    return session

@app.route('/api/predict-digit', methods=['POST', 'OPTIONS'])
def predict_digit():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        # Load model/session
        ort_session = load_model()
        
        # Get image data
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        image_str = data['image'].split(",")[1]
        image_data = base64.urlsafe_b64decode(image_str)
        image = Image.open(io.BytesIO(image_data))
        
        # Preprocessing
        image = image.convert("L")
        image = image.resize((28, 28))
        image = np.array(image)
        
        # Reshape for the model - ONNX models from Keras usually expect (batch, ...)
        # Based on previous code, the model expects (1, 28, 28) or (1, 784) or (1, 28, 28, 1)
        # We need to match the input name and shape of the ONNX model
        input_name = ort_session.get_inputs()[0].name
        input_shape = ort_session.get_inputs()[0].shape
        
        if len(input_shape) == 4:
            # (1, 28, 28, 1)
            image = image.reshape(1, 28, 28, 1)
        elif len(input_shape) == 3:
            # (1, 28, 28)
            image = image.reshape(1, 28, 28)
        else:
            # (1, 784)
            image = image.reshape(1, 784)

        image = image / 255.0
        image = image.astype(np.float32)
        
        # Run inference
        outputs = ort_session.run(None, {input_name: image})
        output_data = outputs[0]
        
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
