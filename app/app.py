import schedule as schedule
from flask import Flask, render_template, request, redirect, flash
from werkzeug.utils import secure_filename
import os
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import io
from datetime import datetime
import schedule
import streamlit as st

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/upload/'
app.config['IMAGE_UPLOAD_FOLDER'] = './static/images/'
app.config['SECRET_KEY'] = ' '

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    print("directory created")

if not os.path.exists(app.config['IMAGE_UPLOAD_FOLDER']):
    os.makedirs(app.config['IMAGE_UPLOAD_FOLDER'])
    print("image directory created")

# Load the Android malware detection classifier
import classifier

# Load the image malware detection model
def recall_m(y_true, y_pred):
    # implementation of recall_m function
    pass

def precision_m(y_true, y_pred):
    # implementation of precision_m function
    pass

def f1_m(y_true, y_pred):
    # implementation of f1_m function
    pass

def extract_image_metadata(image_path):
    with Image.open(image_path) as img:
        # Extract metadata
        name = os.path.basename(image_path)
        creation_date = datetime.fromtimestamp(os.path.getctime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
        width, height = img.size
        dimensions = f"{width} x {height}"
        return name, creation_date, dimensions

model_file = './static/models/model.h5'
model = load_model(model_file, custom_objects={'f1_m': f1_m, 'precision_m': precision_m, 'recall_m': recall_m})

CATEGORIES = ['Adialer.C', 'Agent.FYI', 'Allaple.A', 'Allaple.L', 'Alueron.gen!J', 'Autorun.K', 'C2LOP.P',
              'C2LOP.gen!g', 'Dialplatform.B', 'Dontovo.A', 'Fakerean', 'Instantaccess', 'Lolyda.AA1', 'Lolyda.AA2',
              'Lolyda.AA3', 'Lolyda.AT', 'Malex.gen!J', 'Obfuscator.AD', 'Rbot!gen', 'Skintrim.N', 'Swizzor.gen!E',
              'Swizzor.gen!I', 'VB.AT', 'Wintrim.BX', 'Yuner.A']

@app.route("/", methods=["GET", "POST"])
def home():
    algorithms = { 'Support Vector Classifier': '92 %'}
    result_apk, accuracy, name, sdk, size = '', '', '', '', ''
    result_image = ''
    image_name, creation_date, dimensions = '', '', ''

    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # If the user does not select a file, the browser also
        # submits an empty part without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file.filename.lower().endswith('.apk'):
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if request.form['algorithm'] == 'Support Vector Classifier':
                accuracy = algorithms['Support Vector Classifier']
                result_apk, name, sdk, size = classifier.classify(os.path.join(app.config['UPLOAD_FOLDER'], filename), 1)

        elif file.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.jfif')):
            filename = secure_filename(file.filename)
            print(filename)
            file_path = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Extract image metadata
            image_name, creation_date, dimensions = extract_image_metadata(file_path)
            # Load and preprocess the image
            with open(file_path, 'rb') as f:
                image_stream = io.BytesIO(f.read())
                image_stream.seek(0)  # Move cursor to beginning of stream
                img = Image.open(image_stream)
                img = img.convert('RGB')  # Convert image to RGB mode
                img = img.resize((64, 64))  # Resize image
                img_array = np.array(img) / 255.0  # Normalize pixel values
                img_array = np.expand_dims(img_array, axis=0)

                # Make prediction
                prediction = model.predict(img_array)
                pred_name = CATEGORIES[np.argmax(prediction)]

                # Check if the prediction is above a certain threshold before classifying
                if np.max(prediction) > 0.5:
                    if pred_name in ['Adialer.C', 'Agent.FYI', 'Allaple.A', 'Allaple.L', 'Alueron.gen!J', 'Autorun.K',
                                     'C2LOP.P', 'C2LOP.gen!g']:
                        result_image = 'Malicious Image Detected.'
                    else:
                        result_image = 'This file is safe.'
                else:
                    result_image = 'Prediction confidence is too low.'

    return render_template("index.html", result_apk=result_apk, result_image=result_image, algorithms=algorithms.keys(),
                           accuracy=accuracy, name=name, sdk=sdk, size=size, image_name=image_name,
                           creation_date=creation_date, dimensions=dimensions)



