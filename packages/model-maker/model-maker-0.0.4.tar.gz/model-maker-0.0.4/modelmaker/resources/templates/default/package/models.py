import tensorflow as tf
import numpy as np
from tensorflow import keras        
from modelmaker import ClassificationModelInterface
from .utils import normalize, rescale2d

class SimpleClassification(ClassificationModelInterface):

    def setup(self, mode='production', model_path=None):
        self.mode = mode

        if mode == 'development':
            self.model = keras.models.load_model(model_path)
        elif mode == 'production':
            raise Exception('production mode not implemented')
        elif mode == 'training':
            pass
        else:
            raise Exception('invalid mode')

    @property
    def labels(self):
        return {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9
        }

    def get_model(self):
        num_classes = len(self.labels)
        model = keras.Sequential([
            keras.layers.Flatten(),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(128, activation=tf.nn.relu),
            keras.layers.Dense(num_classes, activation=tf.nn.softmax),
        ])
        return model

    def preprocess(self, x):
        y = rescale2d(x, (28, 28))
        return normalize(y, 0, 1)

    def predict(self, x):
        if self.mode == "production":
            raise Exception('production mode not implemented')
        elif self.mode == 'development':
            return self.model.predict(np.expand_dims(x, axis=0)) # insert batch axis
        else:
            raise Exception('invalid mode')

    def postprocess(self, x, orig):
        one_hot = self.softmax_to_one_hot(x)
        return self.one_hot_to_label(one_hot)