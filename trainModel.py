import numpy as np
import cv2
import os
import random
import pickle


# Directories for training model and folder categories
# DATADIR = "F:/Projects/open_vision/PetImages/PetImages"
DATADIR = os.getcwd() + '\PetImages'
datasets_dir = os.listdir(DATADIR)
CATEGORIES = ['Dog', 'Cat']

# Resize the image to 250px. The smaller the number, the lower the pixels
IMG_SIZE = 250

# Will contain an array of trained data
training_data = []

# Function to train data


def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        for img in path:
            # fpath = os.path.join(path, img)
            # try:
            #     fobj = open(fpath, "rb")
            #     is_jfif = tf.compat.as_bytes("JFIF") in fobj.peek(10)
            # finally:
            #     fobj.close()
            #
            # if not is_jfif:
            #     os.remove(fpath)
            try:
                print(os.path.join(path, img))
                # img_array = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
                # img_array = cv2.imread(os.path.join(
                #     path, img), cv2.IMREAD_GRAYSCALE)
                # new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                # print(new_array)
                # training_data.append([new_array, class_num])
            except Exception as e:
                pass

# def create_training_data():
#     for category in CATEGORIES:
#         path


create_training_data()
# random.shuffle(training_data)

# X = []
# Y = []

# for features, label in training_data:
#     X.append(features)
#     Y.append(label)

# X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

# pickle_out = open("X.pickle", 'wb')
# pickle.dump(X, pickle_out)
# pickle_out.close()

# pickle_out = open("Y.pickle", 'wb')
# pickle.dump(Y, pickle_out)
# pickle_out.close()
