from flask import Flask, request, jsonify
import base64
import os
import sys
import numpy as np
from PIL import Image
import io
import traceback

app = Flask(__name__)

# Global ONNX session variable
session = None

def load_model():
    """Load the ONNX model lazily with robust path finding"""
    global session
    if session is None:
        try:
            import onnxruntime as ort
            
            # Try multiple possible paths for the model file in serverless env
            possible_paths = [
                os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.onnx'), # Root from /api
                os.path.join(os.path.dirname(__file__), 'model.onnx'),                 # Same dir as script
                os.path.join(os.getcwd(), 'model.onnx'),                               # Current working dir
                '/var/task/model.onnx'                                                 # Vercel specific
            ]
            
            model_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            
            if not model_path:
                raise FileNotFoundError(f"model.onnx not found. Checked: {possible_paths}")
            
            # Use CPU execution provider (stable for Vercel)
            session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
            print(f"ONNX Model loaded successfully from {model_path}")
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
        image_data = base64.b64decode(image_str)
        image = Image.open(io.BytesIO(image_data))
        
        # Preprocessing
        image = image.convert("L")
        image = image.resize((28, 28))
        image = np.array(image)
        
        # Determine exact input shape required by the model
        input_meta = ort_session.get_inputs()[0]
        input_name = input_meta.name
        input_shape = input_meta.shape # e.g. [None, 28, 28] or [None, 784]
        
        # Handle different potential MNIST model architectures
        if len(input_shape) == 4:
            # Expected: (batch, height, width, channels) -> (1, 28, 28, 1)
            image = image.reshape(1, 28, 28, 1)
        elif len(input_shape) == 2:
            # Expected: (batch, flattened) -> (1, 784)
            image = image.reshape(1, 784)
        else:
            # Default to 3D if that's what's left: (1, 28, 28)
            image = image.reshape(1, 28, 28)

        # Normalize and set type
        image = image / 255.0
        image = image.astype(np.float32)
        
        # Run inference
        outputs = ort_session.run(None, {input_name: image})
        output_data = outputs[0]
        
        prediction = int(np.argmax(output_data[0]))
        confidence = float(np.max(output_data[0])) * 100
        
        return jsonify({ 
            "prediction": str(prediction),
            "confidence": f"{confidence:.2f}"
        })
        
    except Exception as e:
        # Return full error details to help debugging the 500 error
        error_msg = f"Error in prediction: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

# Vercel serverless handler
def handler(event, context):
    return app(event, context)
