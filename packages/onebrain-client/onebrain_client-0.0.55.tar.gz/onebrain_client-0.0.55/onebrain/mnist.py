# TensorFlow and tf.keras
import tensorflow as tf
import os
from tensorflow import keras
from pathlib import Path
# Helper libraries
import numpy as np
import matplotlib.pyplot as plt
import os

# download the data
print('load data')
datapath = '/dataset/mnist.npz'
(train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data(datapath)

class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

train_images = train_images / 255.0
test_images = test_images / 255.0


def create_model():
    # It's necessary to give the input_shape，or it will fail when you load the model
    # The error will be like : You are trying to load the 4 layer models to the 0 layer
    model = keras.Sequential([
        keras.layers.Conv2D(32, [5, 5], activation=tf.nn.relu, input_shape=(28, 28, 1)),
        keras.layers.MaxPool2D(),
        keras.layers.Conv2D(64, [7, 7], activation=tf.nn.relu),
        keras.layers.MaxPool2D(),
        keras.layers.Flatten(),
        keras.layers.Dense(576, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model


# reshape the shape before using it, for that the input of cnn is 4 dimensions
train_images = np.reshape(train_images, [-1, 28, 28, 1])
test_images = np.reshape(test_images, [-1, 28, 28, 1])

# train
model = create_model()
model.fit(train_images, train_labels, epochs=4)

# save the model
my_file = Path("/model")
if not my_file.exists():
    os.mkdir("/model")

# Evaluate
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=0)
print('Test accuracy:', test_acc)
saved_model_path = "/model"
tf.keras.experimental.export_saved_model(model, saved_model_path)