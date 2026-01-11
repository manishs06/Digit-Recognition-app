from flask import Flask, request, jsonify, send_from_directory
import base64
import os
import numpy as np
from PIL import Image
import io

# Initialize Flask app
# We tell Flask to serve static files from the 'static' folder and templates from 'public' (where index.html is)
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Global ONNX session for inference
_session = None

def get_session():
    global _session
    if _session is None:
        import onnxruntime as ort
        model_path = os.path.join(os.path.dirname(__file__), 'model.onnx')
        _session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
    return _session

@app.route('/')
def index():
    """Serve the main frontend page"""
    return send_from_directory('public', 'index.html')

@app.route('/api/predict-digit', methods=['POST'])
def predict():
    """API endpoint for digit prediction using ONNX"""
    try:
        session = get_session()
        
        data = request.get_json(silent=True)
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        # Extract base64 image data
        image_str = data['image'].split(",")[1]
        image_data = base64.b64decode(image_str)
        image = Image.open(io.BytesIO(image_data)).convert("L").resize((28, 28))
        
        # Prepare image for ONNX model
        input_meta = session.get_inputs()[0]
        input_name = input_meta.name
        input_shape = input_meta.shape
        
        image_array = np.array(image).astype(np.float32) / 255.0
        
        # Reshape to match model input (handles NHWC, NCHW, or flattened)
        if len(input_shape) == 4:
            if input_shape[1] == 1: # NCHW
                image_array = image_array.reshape(1, 1, 28, 28)
            else: # NHWC
                image_array = image_array.reshape(1, 28, 28, 1)
        elif len(input_shape) == 2:
            image_array = image_array.reshape(1, 784)
        else:
            image_array = image_array.reshape(1, 28, 28)

        # Run inference
        outputs = session.run(None, {input_name: image_array})
        prediction = int(np.argmax(outputs[0][0]))
        confidence = float(np.max(outputs[0][0])) * 100
        
        return jsonify({
            "prediction": str(prediction),
            "confidence": f"{confidence:.2f}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
