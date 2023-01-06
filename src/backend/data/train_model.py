# Script to train model
# python -m data.train_model

import os
import numpy as np
import pandas as pd
import tensorflow as tf
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
    model.add(keras.layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(keras.layers.MaxPooling2D((2, 2)))
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(256, activation='relu'))
    model.add(keras.layers.Dropout(0.2))
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

    print('\nSaving model')
    keras.models.save_model(model, MODEL_PATH)
    history_df = pd.DataFrame(history.history) 
    history_df.to_parquet(MODEL_PATH + 'history.parquet')

    print('\nTesting model')
    train_loss, train_acc = model.evaluate(train_x, train_y, verbose=1)
    test_loss, test_acc = model.evaluate(test_x, test_y, verbose=1)
    test_predictions = np.rint(model.predict(test_x))
    confusion_matrix = tf.math.confusion_matrix(labels=test_y, predictions=test_predictions).numpy()
    precision = confusion_matrix[1][1] / (confusion_matrix[1][1] + confusion_matrix[0][1])
    recall = confusion_matrix[1][1] / (confusion_matrix[1][1] + confusion_matrix[1][0])

    plt.rcParams['figure.figsize'] = [8.0, 8.0]
    plt.subplot(3, 1, 1)
    plt.title('Loss\nTrain: {:.4f}, Test: {:.4f}'.format(train_loss, test_loss))
    plt.plot(history.history['loss'], label='train')
    plt.plot(history.history['val_loss'], label='test')
    plt.legend(loc='upper right')

    plt.subplot(3, 1, 2)
    plt.title('Accuracy\nTrain: {:.4f}, Test: {:.4f}'.format(train_acc, test_acc))
    plt.plot(history.history['accuracy'], label='train')
    plt.plot(history.history['val_accuracy'], label='test')
    plt.legend(loc='upper right')

    plt.subplot(3, 1, 3)
    plt.title('Confusion Matrix\nPrecision: {:.4f}, Recall: {:.4f}'.format(precision, recall))
    plt.xticks([0, 1])
    plt.xlabel('Predicted')
    plt.yticks([0, 1])
    plt.ylabel('Actual')
    plt.imshow(confusion_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(confusion_matrix.shape[0]):
        for j in range(confusion_matrix.shape[1]):
            plt.text(x=j, y=i, s=confusion_matrix[i, j], va='center', ha='center')

    plt.tight_layout(pad=1.0)
    plt.savefig(MODEL_PATH + 'test-result-plots.png')
    plt.show()


if __name__ == "__main__":
    main()
