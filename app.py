
from flask import Flask, jsonify, request, render_template
import pickle
import numpy as np
app = Flask(__name__)

flowers = ['setosa', 'versicolor',  'virginica']
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    int_features = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = prediction[0]

    return render_template('index.html', prediction_text='Species  should be ' + str(flowers[output]))


@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])
    output = prediction[0]
    return jsonify(str(flowers[output]).upper())

if __name__ == "__main__":
    app.run(debug=True)
