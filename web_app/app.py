from flask import Flask, render_template, request, redirect, url_for, flash
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the model
MODEL_PATH = r"C:\Users\adirn\Documents\fish freshness\model.h5"
try:
    model = load_model(MODEL_PATH)
    logging.info("Model loaded successfully.")
except Exception as e:
    logging.error(f"Error loading model from {MODEL_PATH}: {e}")
    exit(1)

# Ensure static directory exists for temporary storage
STATIC_DIR = 'static/uploads'
os.makedirs(STATIC_DIR, exist_ok=True)

# Route for upload page
@app.route('/')
@app.route('/upload')
def upload():
    return render_template('upload.html')

# Route to handle prediction
@app.route('/predict', methods=['POST'])
def predict():
    # Ensure a file was uploaded
    if 'file' not in request.files:
        logging.error("No file part in the request.")
        flash("No file selected. Please upload an image.")
        return redirect(url_for('upload'))
    
    file = request.files['file']
    if file.filename == '':
        logging.error("No file selected.")
        flash("No file selected. Please choose a file.")
        return redirect(url_for('upload'))

    try:
        # Save uploaded file temporarily
        filepath = os.path.join(STATIC_DIR, file.filename)
        file.save(filepath)
        logging.debug(f"File saved to: {filepath}")

        # Preprocess the image
        img = load_img(filepath, target_size=(224, 224))  # Adjust size to model requirements
        img = img_to_array(img) / 255.0
        img = np.expand_dims(img, axis=0)

        # Make prediction
        prediction = model.predict(img)
        logging.debug(f"Prediction result: {prediction}")
        result_message = (
            "The fish is not fresh." if prediction[0][0] > 0.5 else "The fish is fresh."
        )

        # Clean up the uploaded file
        os.remove(filepath)
        logging.debug("Temporary file removed.")

        return render_template('result.html', result_message=result_message)

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        flash("An error occurred while processing the file. Please try again.")
        return redirect(url_for('upload'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
