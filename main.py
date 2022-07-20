#include opencv
import cv2 as cv

#read images
img1 = cv.imread('img.png',0)
img2 = cv.imread('img_1.png',0)

#initialize orb detection
orb = cv.ORB_create(nfeatures=1000)

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
cv.imshow('img1',img1)
cv.imshow('img2',img2)
cv.imshow('img3',img3)
cv.waitKey(0)