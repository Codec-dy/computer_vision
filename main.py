# include opencv
import os
import cv2 as cv
import mysql.connector as sql
from mysql.connector import Error

# Initializing sql database variables
host = "localhost"
user = 'root'
password = ''
database = 'test'

# loading image names from images folder
img_dir_path = os.getcwd() + '\images'
image_files = []
images_in_folder = os.listdir(img_dir_path)
print(images_in_folder)

try:
    connection = sql.connect(host=host, user=user,
                             password=password, database=database)
    cursor = connection.cursor()

    """ Inserting products into db """

    # for img in images_in_folder:
    #     get_imagename = img.split(".")[0];
    #     insert = """insert into products (productName, picture ) values (%s,%s)"""
    #     value = (get_imagename, img)
    #     cursor.execute(insert, value)
    #     connection.commit()

    select = "select * from products"
    cursor.execute(select)
    result = cursor.fetchmany(size=12)  # Retrieving data from the database
    print(result)
except Error as e:
    print("error occurred at ", e)

finally:
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print('connection is close')


# read images
image_to_search = cv.imread('img.png', 0)

"""  initialize orb detection
    # Detection with Orb
"""
orb = cv.ORB_create(nfeatures=4000)

# Looping through images in the database to find the best fit
for data in result:
    img_from_database = cv.imread('images/'+data[2], 0)

    img_from_database_resized = cv.resize(img_from_database, (400, 400))

    """ keypoints finding && """
    keypoints_1, descriptor_1 = orb.detectAndCompute(image_to_search, None)
    keypoints_2, descriptor_2 = orb.detectAndCompute(img_from_database, None)

    bf = cv.BFMatcher()
    matches = bf.knnMatch(descriptor_1, descriptor_2, k=2)

    """ matches occuring"""
    good_keypoint = []

    for m, n in matches:
        if m.distance < 0.75*n.distance:
            good_keypoint.append([m])
    print(len(good_keypoint))
    compared_images = cv.drawMatchesKnn(image_to_search, keypoints_1, img_from_database,
                                        keypoints_2, good_keypoint, None, flags=2)

    # display images and draw keypoints
    # cv.imshow('img1', image_to_search)
    # cv.imshow('img2', img_from_database)

    cv.imshow('img3', compared_images)
    cv.waitKey(0)
