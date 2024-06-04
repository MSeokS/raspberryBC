import numpy as np

import tensorflow as tf

from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

model = load_model("Resnet50_False_hyperband.h5")

with open("labels.txt", "r", encoding="utf-8") as file:
    labels = file.read().splitlines()

def predict():
    img_path = "./predict.jpg"

    img_str=open(img_path, 'rb').read()

    img = tf.image.decode_jpeg(img_str, channels=3)
    img = tf.image.resize(img, (224, 224))
    img = img / 255.0

    img = np.expand_dims(img, axis=0)

    return img
