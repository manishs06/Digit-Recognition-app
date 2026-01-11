from flask import Flask, request, jsonify
import base64
import os
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Global session variable for lazy loading
_session = None

def get_session():
    global _session
    if _session is None:
        import onnxruntime as ort
        # Standard Vercel path: api/predict.py is one level deep, model.onnx is at root
        model_path = os.path.join(os.path.dirname(__file__), '..', 'model.onnx')
        
        # Fallback for different Vercel build layouts
        if not os.path.exists(model_path):
            model_path = os.path.join(os.getcwd(), 'model.onnx')
            
        _session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    return _session

@app.route('/api/predict-digit', methods=['POST'])
def predict():
    try:
        # Load session
        session = get_session()
        
        # Get data
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        # Process image
        image_str = data['image'].split(",")[1]
        image_data = base64.b64decode(image_str)
        image = Image.open(io.BytesIO(image_data)).convert("L").resize((28, 28))
        
        # Prepare for ONNX
        input_meta = session.get_inputs()[0]
        input_name = input_meta.name
        input_shape = input_meta.shape
        
        image_array = np.array(image).astype(np.float32) / 255.0
        
        # Handle dynamic input shapes (batch, H, W, C) or (batch, flat)
        if len(input_shape) == 4:
            if input_shape[1] == 1: # NCHW
                image_array = image_array.reshape(1, 1, 28, 28)
            else: # NHWC
                image_array = image_array.reshape(1, 28, 28, 1)
        elif len(input_shape) == 2:
            image_array = image_array.reshape(1, 784)
        else:
            image_array = image_array.reshape(1, 28, 28)

        # Predict
        outputs = session.run(None, {input_name: image_array})
        prediction = int(np.argmax(outputs[0][0]))
        confidence = float(np.max(outputs[0][0])) * 100
        
        return jsonify({
            "prediction": str(prediction),
            "confidence": f"{confidence:.2f}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Simple health check to verify the function starts
@app.route('/api/health')
def health():
    return jsonify({"status": "healthy", "model_exists": os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'model.onnx'))})
