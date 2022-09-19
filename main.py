import requests
import random
from PIL import Image
import cv2 as cv
import urllib.request
import os
URL = 'https://fabamall.com/api/product/'

request_data = requests.get(URL)

data = request_data.json()

results = data['results']


#this code is used to pull the images from their database into the folders so dont run it again else it will create duplicates
for result in results:
    categories = result['shop']['categories_names']
    images = result['images']
    category_name = result['category_name']
    if category_name.find('/') != -1:
        category_name = category_name.split('/')[-1]
    print(category_name)
    for image in images:
        if image != '' or image != None:
            name = image['image'].split('/')[-1]
            if os.path.isfile('static/TrainingImages/'+category_name+'/'+name) == False:
                if os.path.isdir('static/TrainingImages/'+category_name) == False:
                    makedir = os.mkdir('static/TrainingImages/'+category_name)
                fullPathName = os.path.join('static/TrainingImages/'+category_name,name)
                urllib.request.urlretrieve(
                    image['image'],
                    fullPathName)

