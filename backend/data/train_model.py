# Script to train model

import os
import numpy as np
import pandas as pd
from tensorflow import keras
from matplotlib import pyplot
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings


def read_dataset(path):
    df = pd.read_pickle(path)
    x, y = df['image'], df['is_ai_generated']
    return np.array([np.array(i) for i in x.to_numpy()]), y.to_numpy()


def main():
    print('Loading dataset')
    train_x, train_y = read_dataset(settings.TRAIN_SET_PATH)
    test_x, test_y = read_dataset(settings.TEST_SET_PATH)

    print('\nCreating model')
    model = keras.models.Sequential()
    model.add(keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=train_x[0].shape))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Conv2D(48, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation='relu'))
    model.add(keras.layers.Dense(1, activation='sigmoid'))

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy'],
    )
    callback = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True
    )
    
    print('\nTraining model')
    history = model.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=100, verbose=1, callbacks=callback)

    print('\Testing model')
    _, train_acc = model.evaluate(train_x, train_y, verbose=1)
    _, test_acc = model.evaluate(test_x, test_y, verbose=1)
    print('Train accuracy: {:.4f}, Test accuracy: {:.4f}'.format(train_acc, test_acc))

    pyplot.subplot(211)
    pyplot.title('Loss')
    pyplot.plot(history.history['loss'], label='train')
    pyplot.plot(history.history['val_loss'], label='test')
    pyplot.legend()

    pyplot.subplot(212)
    pyplot.title('Accuracy')
    pyplot.plot(history.history['accuracy'], label='train')
    pyplot.plot(history.history['val_accuracy'], label='test')
    pyplot.legend()

    pyplot.show()

    print('Saving model')
    keras.models.save_model(model, settings.MODELS_DIR + '{}'.format(datetime.now().strftime('%Y%m%d-%H%M%S')))


if __name__ == "__main__":
    main()
