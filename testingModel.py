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
categories = ['Bicycle','Car','Laptop','Phone']

#Function for turning our image into an array and correcting its size
def prepare(filepath):
    img_size = 250
    img = image.load_img(filepath, target_size=(img_size,img_size))
    X = image.img_to_array(img)
    X = np.expand_dims(X,axis=0)
    return np.vstack([X])



try:
    user_image = 'car.jpg'
    value = model.predict(prepare(user_image))
    index = value[0].tolist().index(1)
    print('This is a ' + categories[index])
    orb = cv.ORB_create(nfeatures=4000)
    databaseImages = os.getcwd() + '\DatabaseImages' + '\%s' %categories[index]

    for image_to_search in os.listdir(databaseImages):
        print('DatabaseImages/%s/%s' % (categories[index], image_to_search))

        img_from_database = cv.imread('DatabaseImages/%s/%s' % (categories[index], image_to_search), 0)

        user_image_gray = cv.read(user_image,0)
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
        print(len(good_keypoint))
        compared_images = cv.drawMatchesKnn(user_image_resized, keypoints_1, img_from_database_resized,
                                            keypoints_2, good_keypoint, None, flags=2)


        cv.imshow('img3', compared_images)

except:
    print('The product does not exist')
    
finally:
    print(value)

