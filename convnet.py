import numpy as np
import cv2
import tensorflow as tf
mnist = tf.keras.datasets.mnist

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Reshape, InputLayer
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import LeakyReLU, Dropout
from tensorflow.keras.optimizers import Adam

class ConvNet:
    def __init__(self, img_rows=28, img_cols=28):

        self.img_rows = img_rows
        self.img_cols = img_cols
        self.input_shape = (self.img_rows,self.img_cols,1)
        self.model = None
        
        depth = 16
        dropout = 0.4
        self.model = Sequential()
        self.model.add(Conv2D(depth,3,strides=1,padding='same',activation='relu',input_shape=self.input_shape))
        self.model.add(Dropout(dropout))

        self.model.add(MaxPooling2D())
        
        self.model.add(Conv2D(depth*2,3,strides=1,padding='same',activation='relu'))
        self.model.add(Dropout(dropout))
        
        self.model.add(MaxPooling2D())

        self.model.add(Conv2D(depth*4,3,strides=1,padding='same',activation='relu'))
        self.model.add(Dropout(dropout))

        self.model.add(Flatten())
        
        self.model.add(Dense(10,activation='softmax'))

        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train(self, train_steps=20, epochs=1):
        (x_train,y_train), _ = mnist.load_data()
        x_train = x_train.reshape(x_train.shape[0], self.img_rows,self.img_cols,1)
        y_train = tf.keras.utils.to_categorical(y_train, 10)
        self.model.fit(x_train,y_train,epochs=epochs)
                           
    def prediction(self,image):
        print(image.shape)
        image = image.reshape(1,image.shape[0], image.shape[1],1)
        res = self.model.predict(image)
        return np.argmax(res)
