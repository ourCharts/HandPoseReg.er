import os
import cv2
from camera import *
number = [i for i in range(0,10)] 
for num in number:
    filepath = './Sign-Language-Digits-Dataset/Dataset/{}'.format(num)
    
    folder = './Preprocess/{}'.format(num)
    judge = os.path.exists(folder)
    if not judge:
        os.makedirs(folder)
    files = os.listdir(filepath)
    
    for f in files:
        print(f)
        name =filepath+'/'+f
        print(name)
        img = process_photo(name)
        cv2.imwrite('./Preprocess/{}/{}'.format(num,f),img)       