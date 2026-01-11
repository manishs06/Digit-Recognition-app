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

def get_model_path():
    """Find the ONNX model file in the current environment"""
    # Define possible paths relative to this script
    possible_paths = [
        # Local & Vercel deployment root
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.onnx'),   # api/../model.onnx
        os.path.join(os.path.dirname(__file__), 'model.onnx'),                   # api/model.onnx
        os.path.join(os.getcwd(), 'model.onnx'),                                 # ./model.onnx
        'model.onnx',                                                            # relative model.onnx
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
            
    # Try absolute path based on standard Vercel layout
    abs_path = os.path.join('/var/task', 'model.onnx')
    if os.path.exists(abs_path):
        return abs_path
        
    return None

def load_model():
    """Load the ONNX model lazily with simplified error handling"""
    global session
    if session is None:
        try:
            import onnxruntime as ort
            
            model_path = get_model_path()
            if not model_path:
                raise FileNotFoundError("Could not find model.onnx in any expected location.")
            
            # Use CPUExecutionProvider (standard for serverless)
            session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
            print(f"Model loaded successfully from {model_path}")
        except Exception as e:
            # Re-raise so it gets caught in predict_digit
            raise RuntimeError(f"Failed to initialize ONNX session: {str(e)}")
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
        image = image.convert("L").resize((28, 28))
        image = np.array(image).astype(np.float32) / 255.0
        
        # Get input metadata
        input_meta = ort_session.get_inputs()[0]
        input_name = input_meta.name
        input_shape = input_meta.shape
        
        # Reshape based on what the model expects
        if len(input_shape) == 4:
            # (batch, height, width, 1) or (batch, 1, height, width)
            if input_shape[1] == 1:
                image = image.reshape(1, 1, 28, 28)
            else:
                image = image.reshape(1, 28, 28, 1)
        elif len(input_shape) == 2:
            # (batch, flattened)
            image = image.reshape(1, 784)
        else:
            # (batch, height, width)
            image = image.reshape(1, 28, 28)

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
        # Log to server console and return JSON error
        print(f"Prediction Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            "error": str(e),
            "traceback": traceback.format_exc() if os.environ.get('VERCEL_ENV') != 'production' else "truncated"
        }), 500

# Entry point for Vercel
def handler(event, context):
    return app(event, context)
