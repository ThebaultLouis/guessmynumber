import numpy as np
import cv2
import tensorflow as tf
#from random import choices
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
        
        depth = 32
        dropout = 0.25
        self.model = Sequential()
        self.model.add(Conv2D(depth,3,strides=1,padding='same',activation='relu',input_shape=self.input_shape))
        self.model.add(MaxPooling2D())
        self.model.add(Conv2D(depth*2,3,strides=1,padding='same',activation='relu'))
        self.model.add(MaxPooling2D())
        self.model.add(Dropout(dropout))
        self.model.add(Flatten())
        self.model.add(Dense(128,activation='relu'))
        self.model.add(Dropout(0.5))       
        self.model.add(Dense(10,activation='softmax'))

        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    def train(self, train_steps=20, epochs=20):
        (x_train,y_train), (x_test,y_test) = mnist.load_data()
        L = [i for i in range(len(x_train))]
        M = [i for i in range(len(x_test))]
        indexes = choices(L,k=5000)
        ind = choices(M,k=1000)
        
        x_train = np.array([cv2.resize(pic, (self.img_rows, self.img_cols)) for pic in x_train])
        x_train = x_train.reshape(x_train.shape[0], self.img_rows,self.img_cols,1)
        #x_train = np.array([x_train[k] for k in indexes])
        y_train = tf.keras.utils.to_categorical(y_train, 10)
        #y_train = np.array([y_train[k] for k in indexes])

        x_test = np.array([cv2.resize(pic, (self.img_rows, self.img_cols)) for pic in x_test])
        x_test = x_test.reshape(x_test.shape[0], self.img_rows,self.img_cols,1)
        #x_test = np.array([x_test[k] for k in ind])
        y_test = tf.keras.utils.to_categorical(y_test, 10)
        #y_test = np.array([y_test[k] for k in ind])
        
        print("training ...\n")
        self.model.fit(x_train,y_train,epochs=epochs,batch_size=128,verbose=1,validation_data=(x_test,y_test))

        model_json = self.model.to_json()
        with open("model.json","w") as json_file:
            json_file.write(model_json)

        self.model.save_weights("model.h5")
        print("model saved\n")
                           
    def prediction(self,image):
        image = image.reshape(1,image.shape[0], image.shape[1],1)
        res = self.model.predict(image)
        return np.argmax(res)
