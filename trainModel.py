from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense,Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.optimizers import RMSprop



train = ImageDataGenerator(rescale = 1/255)
validation = ImageDataGenerator(rescale = 1/255)

#This specifies the directory for the training and validation dataset which are literally the same
train_dataset = train.flow_from_directory('media/TrainingImages/', target_size=(250,250), batch_size=4, class_mode="categorical")

validation_dataset = validation.flow_from_directory('media/TrainingImages/',target_size=(250,250), batch_size=4, class_mode="categorical")



#This is the creation of the model
model = Sequential()

model.add(Conv2D(16,(3,3), input_shape=(250,250,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(32,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(64,(3,3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))


model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))

model.add(Dense(4))
model.add(Activation('softmax'))
#
model.compile(loss="categorical_crossentropy", optimizer=RMSprop(learning_rate=0.001), metrics=['accuracy'])
model.fit(train_dataset,epochs=30, batch_size=8, shuffle=True,verbose=1, validation_split=0.1, validation_data=validation_dataset)

model.save('CNN.model')