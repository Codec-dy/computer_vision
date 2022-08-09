from keras.models import load_model
from keras_preprocessing import image
import numpy as np
import os
import cv2 as cv
import mysql.connector as sql
from mysql.connector import Error

#Load our Model created using trainingModel.py
model = load_model('CNN.model')

#List of Available products

tr = os.getcwd() +'\TrainingImages'
categories = os.listdir(tr)

#Function for turning our image into an array and correcting its size
def prepare(filepath):
    img_size = 250
    img = image.load_img(filepath, target_size=(img_size,img_size))
    X = image.img_to_array(img)
    X = np.expand_dims(X,axis=0)
    return np.vstack([X])



try:
    print(categories)
    arry = []
    user_image = 'TrainingImages/Clothing/img_2.png'
    value = model.predict(prepare(user_image))
    index = value[0].tolist().index(1)
    print('This is a ' + categories[index+1])
    orb = cv.ORB_create(nfeatures=4000)
    databaseImages = os.listdir('TrainingImages/%s' %categories[index+1])
    for image_to_loop in databaseImages:

        img_from_database = cv.imread('TrainingImages/%s/%s' % (categories[index+1], image_to_loop), 0)
        user_image_gray = cv.imread(user_image,0)
        img_from_database_resized = cv.resize(img_from_database, (400, 400))
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
        compared_images = cv.drawMatchesKnn(user_image_resized, keypoints_1, img_from_database_resized,
                                            keypoints_2, good_keypoint, None, flags=2)

        arry.append([len(good_keypoint), image_to_loop])
    arry.sort(key=lambda row:(row[0]), reverse=True)
    print(arry)
  
                  

except:
    print('The product does not exist')

finally:
    print(value)
    cv.waitKey(0)

