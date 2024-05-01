import tensorflow as tf
import tensorflow.keras as keras
from tensorflow.keras.layers import *
from tensorflow.keras.applications import VGG19



input_shape=(224,224,3)
img_rows=224
img_cols=224


def create_model(input_shape):
    base_model = VGG19(
    include_top=False,
    weights="imagenet",
    input_shape=input_shape)

    for i in base_model.layers:
        i.trainable=False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024,activation='relu')(x)
    x = Dense(1024,activation='relu')(x)
    x = Dense(512,activation='relu')(x)

    model = keras.Model(inputs=base_model.inputs,outputs=x)


    print("model summary is as follows:")
    model.summary()
    return model

if __name__=='__main__':
    m = create_model(input_shape=input_shape)