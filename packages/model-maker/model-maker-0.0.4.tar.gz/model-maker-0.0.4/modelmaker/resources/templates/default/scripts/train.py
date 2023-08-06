import os
import sys
import numpy as np
from tensorflow import keras
file_path = os.path.abspath(__file__)
current_directory = os.path.dirname(file_path)
project_directory = os.path.dirname(current_directory)
sys.path.insert(0, project_directory)
from {{ package_name }}.models import SimpleClassification

######################################################################
# train SimpleClassification
######################################################################

# load model in training mode
simple_model = SimpleClassification(mode='training')

class DataGenerator(keras.utils.Sequence):

    def __init__(self, batch_size, mode='train'):
        # load mnist dataset
        train, test = keras.datasets.mnist.load_data(path="mnist.npz")

        if mode == 'train':
            self.xs, self.ys = train
        else:
            self.xs, self.ys = test

        self.total = self.xs.shape[0]
        self.batch_size = batch_size


    def __len__(self):
        return self.total // self.batch_size

    def __getitem__(self, idx):

        start = idx * self.batch_size
        end = self.batch_size + idx * self.batch_size

        if self.batch_size + idx * self.batch_size  > self.total:
            end = self.total
        
        xs = np.asarray([ simple_model.preprocess(x) for x in self.xs[start:end,:,:] ])
        ys = np.asarray([ simple_model.one_hot(y) for y in self.ys[start:end] ])

        return xs, ys

# training parameters
batch_size = 32
epochs = 5

# generate training data
train_data = DataGenerator(batch_size, mode='train')
val_data = DataGenerator(batch_size, mode='test')

# train model
keras.backend.clear_session()
model = simple_model.get_model()
model.compile(
    optimizer=keras.optimizers.Adam(),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)
model.fit(
    train_data,
    epochs=epochs,
    validation_data=val_data
)

# save model
model_folder = os.path.join(
    os.path.dirname(
        os.path.dirname(
            os.path.realpath(__file__)
        )
    ),
    "saved_models"
)
model.save(os.path.join(model_folder, 'simple_model'))