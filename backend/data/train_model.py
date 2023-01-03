# Script to train model
# python -m data.train_model

import os
import numpy as np
import pandas as pd
from tensorflow import keras
from matplotlib import pyplot as plt
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
from django.conf import settings


def read_dataset(path):
    df = pd.read_pickle(path)
    x, y = df['image'], df['is_ai_generated']
    return np.array([np.array(i) for i in x.to_numpy()]), y.to_numpy()


def main():
    MODEL_PATH = settings.MODELS_DIR + '{}/'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))

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
    train_loss, train_acc = model.evaluate(train_x, train_y, verbose=1)
    test_loss, test_acc = model.evaluate(test_x, test_y, verbose=1)

    print('Saving model')
    keras.models.save_model(model, MODEL_PATH)

    fig, ax = plt.subplots(2, 1)

    ax[0].set_title('Loss\ntrain: {:.4f}, test: {:.4f}'.format(train_loss, test_loss))
    ax[0].plot(history.history['loss'], label='train')
    ax[0].plot(history.history['val_loss'], label='test')
    ax[0].legend()

    ax[1].set_title('Accuracy\ntrain: {:.4f}, test: {:.4f}'.format(train_acc, test_acc))
    ax[1].plot(history.history['accuracy'], label='train')
    ax[1].plot(history.history['val_accuracy'], label='test')
    ax[1].legend()

    fig.tight_layout(pad=2)
    fig.savefig(MODEL_PATH + 'plt.png')
    fig.show()


if __name__ == "__main__":
    main()
