from keras.models import load_model
from keras_preprocessing import image
import numpy as np

#Load our Model created using trainingModel.py
model = load_model('CNN.model')

#List of Available products
categories = ['Bicycle','Car','Laptop','Phone']

#Function for turning our image into an array and correcting its size
def prepare(filepath):
    img_size = 250
    img = image.load_img(filepath, target_size=(img_size,img_size))
    X = image.img_to_array(img)
    X = np.expand_dims(X,axis=0)
    return np.vstack([X])



try:
    value = model.predict(prepare('kente/kente.jpg'))
    index = value[0].tolist().index(1)
    print('This is a ' + categories[index])

except:
    print('The product does not exist')

finally:
    print(value)

