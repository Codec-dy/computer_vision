
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import urllib.request
import requests

def upload(request):
    IMG_LIST = []
    info = {}
    shop=''
    if request.method == 'POST' and request.FILES['upload']:
        location = request.POST.get('location')
        upload = request.FILES['upload']
        fss = FileSystemStorage('media/static/')
        file = fss.save(upload.name, upload)
        print(upload.name)
        file_url = fss.url(file)
        import testModel2 as testModel
        URL = 'https://fabamall.com/api/product/'

        request_data = requests.get(URL)

        data = request_data.json()

        results = data['results']

        model = testModel.figureOut('media/static/' + upload.name)
        print(model)
        if len(model) != 0:
            IMG_LIST = []
            if model[0].find('Product found') == 0:
                if model[2].find('_') == 0:
                    model[2] = model[2].replace('_',' ')

                search_from = list(filter(lambda shop: shop['category_name'] == model[2],results))
            for img in model[1]:
                for result in search_from:
                    imags = result['images']

                    for imag in imags:
                        name = imag['image'].split('/')[-1]
                        cities = result['shop']['owner']['region']['cities']
                        location_search = list(filter(lambda city: city['name'] == location,cities))
                        print(location_search)
                        if img[1] == name and len(location_search) != 0:
                            shop = result['shop']
                            IMG_LIST.append([{'img': 'media/TrainingImages/' + img[2] + '/' + img[1], 'shop':shop}])

            info = model[0]
        return render(request, 'index.html', {'file_url': file_url,'info':info, 'images':IMG_LIST})
    return render(request, 'index.html', {'info':info, 'images':IMG_LIST})