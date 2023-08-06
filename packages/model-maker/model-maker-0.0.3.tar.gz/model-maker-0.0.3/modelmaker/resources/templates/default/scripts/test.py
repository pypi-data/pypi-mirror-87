import os
import sys
import numpy as np
from tensorflow import keras
file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(file_path)
project_directory = os.path.dirname(current_directory)
sys.path.insert(0, project_directory)
from {{ package_name }}.models import SimpleClassification

# load model in development mode
model_path = os.path.join(project_directory, 'saved_models', 'simple_model')
simple_model = SimpleClassification(mode='development', model_path=model_path)

# load mnist dataset
_, (x_test, y_test) = keras.datasets.mnist.load_data(path="mnist.npz")

for i, x in enumerate(x_test[0:10]):
    print(simple_model(x), y_test[i])