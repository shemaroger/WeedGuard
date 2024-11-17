# prediction/ml_model.py
import joblib
import numpy as np
from tensorflow.keras.preprocessing import image # type: ignore
import tensorflow as tf
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), 'D:\Project\WeedGuard\weedGuard\weedGuardApp\weed_crop_model.joblib')
model = joblib.load(model_path)

IMG_SIZE = (128, 128)

def predict_image(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    return "Weed detected" if prediction > 0.5 else "Crop detected"

