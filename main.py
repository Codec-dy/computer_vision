import cv2 as cv

img1 = cv.imread('img.png',0)
img2 = cv.imread('img_1.png',0)

orb = cv.ORB_create(nfeatures=1000)

kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)

good = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good.append([m])
print (len(good))
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good,None,flags=2)

cv.imshow('img1',img1)
cv.imshow('img2',img2)
cv.imshow('img3',img3)
cv.waitKey(0)