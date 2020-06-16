import tensorflow as tf
import numpy as np
import cv2 as cv
import pickle

xtrainFile = open('./xtrain.pickle', 'rb')
xtrain = pickle.load(xtrainFile)
xtrainFile.close()

ytrainFile = open('./ytrain.pickle', 'rb')
ytrain = pickle.load(ytrainFile)
ytrainFile.close()

xtestFile = open('./xtest.pickle', 'rb')
xtest = pickle.load(xtestFile)
xtestFile.close()

ytestFile = open('./ytest.pickle', 'rb')
ytest = pickle.load(ytestFile)
ytestFile.close()

def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(128, 128, 1)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(9, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer=tf.optimizers.RMSprop(learning_rate=0.0001), metrics=['accuracy'])
    return model


model = create_model()
model.summary()
model.fit(xtrain, ytrain, epochs=10, batch_size=32)
model.save('new_model.h5')
model.evaluate(xtest, ytest, verbose=2)
# probability_model = tf.keras.Sequential([model, 
#                                          tf.keras.layers.Softmax()])

print('done')

def get_real_photo(path):
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    image = cv.resize(image, (128, 128))
    image = np.expand_dims(image, axis=2)
    np.array(image, dtype=float)
    image = image / 255.0
    image = (np.expand_dims(image,0))
    return image


# print(probability_model.predict(get_real_photo('./data/king/000.png')))

# print(xtrain.shape)
# print(ytrain.shape)