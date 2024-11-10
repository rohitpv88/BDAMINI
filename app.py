from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
# Path to save uploaded images
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize model paths
wheat_model_path = os.path.join(os.path.dirname(__file__), 'wheat.h5')
maize_model_path = os.path.join(os.path.dirname(__file__), 'maize.h5')

# Load models
def load_model(model_path):
    try:
        model = tf.keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path}.")
        return model
    except Exception as e:
        print(f"Error loading model from {model_path}: {e}")
        return None

# Preprocess the image
def preprocess_image(image, target_size=(64, 64)):
    try:
        img = tf.keras.utils.img_to_array(image) / 255.0  # Normalize to [0, 1]
        img = tf.image.resize(img, target_size)
        return np.expand_dims(img, axis=0)  # Add batch dimension
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Predict disease
def predict_disease(model, img_array, class_names):
    if img_array is None:
        print("Invalid image input for prediction.")
        return "Invalid image input for prediction.", None, None

    try:
        predictions = model.predict(img_array)
        predicted_class_index = np.argmax(predictions[0])
        predicted_class_name = class_names[predicted_class_index]

        # Dummy data for demonstration
        # Ideally, this should be replaced with actual data related to each disease
        medicine_recommendations = {
            'leaf rust': 'Fungicide A',
            'loose smut': 'Fungicide B',
            'crown root': 'Treatment C',
            'Healthy': 'No treatment needed',
            'northern leaf blight': 'Fungicide X',
            'cercospora gray spot': 'Fungicide Y',
            'common rust': 'Treatment Z',
            'healthy': 'No treatment needed'
        }

        causes = {
            'leaf rust': 'Caused by the fungus Puccinia triticina.',
            'loose smut': 'Caused by the fungus Ustilago tritici.',
            'crown root': 'Caused by various pathogens affecting the root system.',
            'Healthy': 'No disease present.',
            'northern leaf blight': 'Caused by the fungus Exserohilum turcicum.',
            'cercospora gray spot': 'Caused by the fungus Cercospora zeae-maydis.',
            'common rust': 'Caused by the fungus Puccinia sorghi.',
            'healthy': 'No disease present.'
        }

        predicted_medicine = medicine_recommendations.get(predicted_class_name, 'Not available')
        predicted_cause = causes.get(predicted_class_name, 'Not available')

        print(f"Predicted class index: {predicted_class_index}")
        print(f"Predicted class name: {predicted_class_name}")
        return predicted_class_name, predicted_medicine, predicted_cause
    except Exception as e:
        print(f"Error during prediction: {e}")
        return f"Error during prediction: {e}", None, None

# Initialize models
wheat_class_names = ['leaf rust', 'loose smut', 'crown root', 'Healthy']
maize_class_names = ['northern leaf blight', 'cercospora gray spot', 'common rust', 'healthy']
wheat_model = load_model(wheat_model_path)
maize_model = load_model(maize_model_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files or 'crop' not in request.form:
        return jsonify({'error': 'No image or crop type provided'})

    image_file = request.files['image']
    crop_type = request.form['crop']

    if image_file.filename == '':
        return jsonify({'error': 'No selected file'})

    if image_file:
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)

        image = Image.open(file_path)
        img_array = preprocess_image(image)

        if crop_type == 'wheat':
            model = wheat_model
            class_names = wheat_class_names
        elif crop_type == 'maize':
            model = maize_model
            class_names = maize_class_names
        else:
            return jsonify({'error': 'Invalid crop type'})

        if model:
            result, medicine, cause = predict_disease(model, img_array, class_names)
            return jsonify({'result': result, 'medicine': medicine, 'cause': cause})
        else:
            return jsonify({'error': 'Model not loaded properly'})

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
