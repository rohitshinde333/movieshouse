from pathlib import Path
import os
from random import choice
import cv2
import tensorflow as tf
from tensorflow import keras
import numpy as np




def del_single(folder):
    for subdir in folder.iterdir():
        count=0
        for file in subdir.iterdir():
            count+=1
        if count<=1:
            for file in subdir.iterdir():
                file.unlink()
            subdir.rmdir()
    print('Folders removed...')


def split_dataset(dirc,train_split=0.9):
    nos = len(os.listdir(str(dirc.resolve())))
    tno = int(nos*train_split)
    train=[]
    test=[]

    
    for person in list(dirc.iterdir())[:tno]:
        for img in person.iterdir():
            negfolder = choice([ele for ele in list(dirc.iterdir()) if ele!=person])
            neg = choice(list(negfolder.iterdir()))
            pos = img
            anc = choice([ele for ele in list(person.iterdir()) if ele!= img])
            train.append((anc,pos,neg))
            

    for person in list(dirc.iterdir())[tno:]:
        for img in person.iterdir():
            negfolder = choice([ele for ele in list(dirc.iterdir()) if ele!=person])
            neg = choice(list(negfolder.iterdir()))
            pos = img
            anc = choice([ele for ele in list(person.iterdir()) if ele!= img])
            test.append((str(anc.resolve()),str(pos.resolve()),str(neg.resolve())))
    return train,test


def encode_single(img_path):
    img = keras.preprocessing.image.load_img(img_path,target_size=(224,224))
    img = np.array(img)
    img = np.around(img/255, decimals=15)
    
    return img


def encode_batches(x,batch_size=64):
    batches = len(x)//batch_size

    for i in range(batches):
        y=np.zeros((3,batch_size,224,224,3))
        print(f"we are at batch {i+1}/{batches}...")
        for j in range(i*batch_size, i*batch_size+batch_size):
            y[0][j-i*batch_size] = encode_single(x[i][0])
            y[1][j-i*batch_size] = encode_single(x[i][1])
            y[2][j-i*batch_size] = encode_single(x[i][2])
        yield y
    




if __name__=='__main__':
    p=Path.cwd().joinpath('face_data')
    split_dataset(p)