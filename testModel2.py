from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import cv2 as cv
import os

# Load the model
model = load_model('keras_model.h5')

categories = os.listdir('media/TrainingImages')
def figureOut(filepath):
    arry = []
    try:
        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1.
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        # Replace this with the path to your image
        image = Image.open(filepath)
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)

        #turn the image into a numpy array
        image_array = np.asarray(image)
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        value = prediction[0]
        value = [round(x) for x in value]
        print(value)
        print(max(value))
        index = value.index(max(value))
        print(index)
        print('This is a ' + categories[index])
        orb = cv.ORB_create(nfeatures=4000)
        databaseImages = os.listdir('media/TrainingImages/%s' %categories[index])
        for image_to_loop in databaseImages:
            img_from_database = cv.imread('media/TrainingImages/%s/%s' % (categories[index], image_to_loop), 0)
            user_image_gray = cv.imread(filepath,0)
            user_image_resized = cv.resize(user_image_gray,(400,400))

            """ keypoints finding && """
            keypoints_1, descriptor_1 = orb.detectAndCompute(user_image_resized, None)
            keypoints_2, descriptor_2 = orb.detectAndCompute(img_from_database, None)

            bf = cv.BFMatcher()
            matches = bf.knnMatch(descriptor_1, descriptor_2, k=2)

            """ matches occuring"""
            good_keypoint = []

            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good_keypoint.append([m])
            arry.append([len(good_keypoint), image_to_loop, categories[index]])
        arry.sort(key=lambda row:(row[0]), reverse=True)
        return ['Product found ('+categories[index]+')',arry, categories[index]]
    except:
        print('The product does not exist')
        orb = cv.ORB_create(nfeatures=4000)
        for category in categories:
            index = categories.index(category)
            databaseImages = os.listdir('media/TrainingImages/%s' %categories[index])
            for image_to_loop in databaseImages[0:5]:
                img_from_database = cv.imread('media/TrainingImages/%s/%s' % (categories[index], image_to_loop), 0)
                user_image_gray = cv.imread(filepath,0)
                user_image_resized = cv.resize(user_image_gray,(400,400))

                """ keypoints finding && """
                keypoints_1, descriptor_1 = orb.detectAndCompute(user_image_resized, None)
                keypoints_2, descriptor_2 = orb.detectAndCompute(img_from_database, None)

                bf = cv.BFMatcher()
                matches = bf.knnMatch(descriptor_1, descriptor_2, k=2)

                """ matches occuring"""
                good_keypoint = []

                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good_keypoint.append([m])
                arry.append([len(good_keypoint), image_to_loop, categories[index]])
            arry.sort(key=lambda row:(row[0]), reverse=True)
        return ['Product not found but similar products are displayed below',arry]
    finally:
        print('done')

