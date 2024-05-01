import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras import *
import numpy as np
import model
import data_prep
import open_face
from pathlib import Path
from tensorflow.keras.callbacks import ModelCheckpoint
import time



optimizer = tf.keras.optimizers.Adam()


def triplet_loss(y_true, y_pred, alpha = 0.2):
   
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,positive)),axis=-1)
    
    neg_dist = tf.reduce_sum( tf.square(tf.subtract(anchor,negative)),axis=-1)
    basic_loss =(tf.add(tf.subtract(pos_dist,neg_dist),alpha))
    loss = tf.reduce_sum(tf.maximum(basic_loss,0))
    
    return loss

def train_step(x):
    with tf.GradientTape() as tape:
        anc = face_model(x[0],training=True)
        pos = face_model(x[1],training=True)
        neg = face_model(x[2],training=True)
        ypred = (anc,pos,neg)
        loss_value = triplet_loss(None,ypred)
    
    grads = tape.gradient(loss_value,face_model.trainable_weights)
    optimizer.apply_gradients(zip(grads, face_model.trainable_weights))
    return loss_value


def test_step(x):
    
    anchor = face_model(x[0],training=False)
    positive = face_model(x[1],training=False)
    negative = face_model(x[2],training=False)
    
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,positive)),axis=-1)
    neg_dist = tf.reduce_sum( tf.square(tf.subtract(anchor,negative)),axis=-1)
    return (pos_dist,neg_dist)

def testing(x):
    results=[]
    for i in x:
        results.append(test_step(x))
    return results


data_dir = Path('/home/pranav/Code/facevgg/face_data')

print('creating model...')
face_model = model.create_model(model.input_shape)
print('splitting data...')
train,test = data_prep.split_dataset(data_dir)
print('train data size is ',len(train))


tf_train_step=tf.function(train_step,autograph=True)
tf_test_step=tf.function(test_step,autograph=True)


model_dir = '/home/pranav/Code/facevgg/weights/best_weights.keras'

epochs = 2
min_loss = 10**5

print('Starting training...\n\n')
for epoch in range(epochs):
    epoch_time=time.time()
    for step,x in enumerate(data_prep.encode_batches(train,batch_size=32)):
        start_time = time.time()

        loss_value = tf_train_step((x[0],x[1],x[2]))

        print(f"It took {round(time.time()-start_time,1)} sec for a training batch...")
        if step%10==0:
            print(f"Loss for {step}th example =",loss_value)
    print(f"epoch {epoch}/{epochs} done...\n",f"Time taken was {time.time()-epoch_time} sec\n\n\n")
    
    if loss_value<min_loss:
        face_model.save(model_dir, overwrite=True, save_format=None)
        print('Got a better model...')
        
print('\n\ntraining process completed...')

print(testing(test))

