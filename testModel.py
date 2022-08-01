from keras.models import load_model
import cv2

categories = ['Cat','Dog']

# Load the model
model = load_model('CNN.model')


def prepare(filepath):
    img_size = 250
    image_array = cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(image_array,(img_size,img_size))
    return new_array.reshape(-1,img_size,img_size,1)



# run the inference
prediction = model.predict([prepare('img.png')])
print(int(prediction))
