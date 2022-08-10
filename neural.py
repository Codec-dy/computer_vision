from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.python.keras.callbacks import TensorBoard
import pickle
import numpy as np
import time

NAME = 'dogs-vs-co-cnn-64x2-{}'.format(int(time.time()))

tensorboard = TensorBoard(log_dir='logs/{}'.format(NAME))

X = pickle.load(open("X.pickle", 'rb'))
Y = pickle.load(open("Y.pickle", 'rb'))

X = X/255.0
X = np.array(X)
Y = np.array(Y)

model = Sequential()

model.add(Conv2D(64, (3, 3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))


model.add(Dense(1))
model.add(Activation('sigmoid'))


# setting epochs refers to the number of times you wish to train the model, the higher the more accurate but comprimses speed
# in creating the model  and validation_split sets the ram percentage for doing the training
model.compile(loss="binary_crossentropy",
              optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, batch_size=1, epochs=5,
          validation_split=0.4, callbacks=[tensorboard])
model.save('CNN.model')
