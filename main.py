#include opencv
import cv2 as cv
import mysql.connector as sql
from mysql.connector import Error

#Initializing sql database variables
host = "localhost"
user = 'root'
password = ''
database = 'test'

#Items inserted into the database for testing
items = ['car1','car2','car3','car6','pen1','pen2','pen3','pen4','bottle1','bottle2','bottle3','bottle4']


try:
    connection = sql.connect(host=host,user=user,password=password,database=database)
    cursor = connection.cursor()
    # for x in items:
    #     insert = """insert into products (productName, picture ) values (%s,%s)"""
    #     value = (x,x+'.jpg')
    #     cursor.execute(insert,value)
    #     connection.commit()
    select = "select * from products"
    cursor.execute(select)
    result = cursor.fetchmany(size=12)   #Retrieving data from the database
    print(result)
except Error as e:
    print("error occurred at ", e)

finally:
    if(connection.is_connected()):
        cursor.close()
        connection.close()
        print('connection is close')



#read images
img1 = cv.imread('img.png',0)

#initialize orb detection
#Detection with Orb
orb = cv.ORB_create(nfeatures=4000)

#Looping through images in the database to find the best fit
for data in result:
    img2 = cv.imread('images/'+data[2],0)


    # keypoints finding &&
    keypoints_1, descriptor_1 = orb.detectAndCompute(img1,None)
    keypoints_2, descriptor_2 = orb.detectAndCompute(img2,None)


    bf = cv.BFMatcher()
    matches = bf.knnMatch(descriptor_1,descriptor_2,k=2)

    #matches occuring
    good_keypoint = []

    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good_keypoint.append([m])
    print (len(good_keypoint))
    img3 = cv.drawMatchesKnn(img1,keypoints_1,img2,keypoints_2,good_keypoint,None,flags=2)

#display images and draw keypoints
# cv.imshow('img1',img1)
# cv.imshow('img2',img2)
# cv.imshow('img3',img3)
# cv.waitKey(0)



