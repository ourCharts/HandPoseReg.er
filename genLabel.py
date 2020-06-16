import os
import pickle
import numpy as np
import cv2 as cv
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split

dataRootFolder = './data/'
dataLeafFolders = os.listdir(dataRootFolder)

data = []
labels = []

for subFolder in dataLeafFolders:
    path = dataRootFolder + subFolder + '/'
    for sampleFolder in os.listdir(path):
        samplePath = path + sampleFolder + '/'
        for imageName in os.listdir(samplePath):
            print('reading ' + samplePath + imageName)
            image = cv.imread(samplePath + imageName)
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
            image = cv.resize(image, (128, 128))
            image = np.expand_dims(image, axis=2)
            data.append(image)
            labels.append(int(subFolder))

data = np.array(data, dtype=float)
data = data / 255.0
labels = np.array(labels)

xtrain, xtest, ytrain, ytest = train_test_split(data, labels, test_size=0.2, random_state=0)
binary = LabelBinarizer().fit(ytrain)
ytrain = binary.transform(ytrain)
ytest = binary.transform(ytest)

with open('./xtrain.pickle', 'wb') as xtrainFile:
    pickle.dump(xtrain, xtrainFile)

with open('./xtest.pickle', 'wb') as xtestFile:
    pickle.dump(xtest, xtestFile)

with open('./ytrain.pickle', 'wb') as ytrainFile:
    pickle.dump(ytrain, ytrainFile)

with open('./ytest.pickle', 'wb') as ytestFile:
    pickle.dump(ytest, ytestFile)
