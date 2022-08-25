import requests
import random
from PIL import Image
import cv2 as cv
import urllib.request
URL = 'https://fabamall.com/api/product/'

request_data = requests.get(URL)

data = request_data.json()

results = data['results']



#this code is used to pull the images from their database into the folders so dont run it again else it will create duplicates
for result in results:
    categories = result['shop']['categories_names']
    images = result['images']
    print(categories)
    for category in categories:
        i = ['Barber']
        val = any( a in category for a in i )
        if val == True:
            for image in images:
                if image != '' or image != None:
                    id = random.randint(1,5)
                    name = 'image%s.png' %id
                    urllib.request.urlretrieve(
                        image['image'],
                        name)

