import requests
import urllib.request
import os
URL = 'https://fabamall.com/api/product/'

request_data = requests.get(URL)

data = request_data.json()


results = data['results']
#
#this code is used to pull the images from their database into the folders so dont run it again else it will create duplicates
for result in results:
    categories = result['shop']['categories_names']
    images = result['images']
    category_name = result['category_name']
    if category_name.find('/') != -1:
        category_name = category_name.split('/')[-1]
    if category_name.find(' ') != -1:
        category_name = category_name.replace(' ','_')


    for image in images:
        if image != '' or image != None:
            name = image['image'].split('/')[-1]
            if os.path.isfile('media/TrainingImages/'+category_name+'/'+name) == False:
                if os.path.isdir('media/TrainingImages/'+category_name) == False:
                    makedir = os.mkdir('media/TrainingImages/'+category_name)
                fullPathName = os.path.join('media/TrainingImages/'+category_name,name)
                urllib.request.urlretrieve(
                    image['image'],
                    fullPathName)

