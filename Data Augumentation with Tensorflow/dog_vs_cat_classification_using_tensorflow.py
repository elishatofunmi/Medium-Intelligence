# -*- coding: utf-8 -*-
"""Dog vs Cat classification using tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MlHGxe-vVtB10xq1Iwm-PfmoCpXchMsj
"""

# Colab library to upload files to notebook
from google.colab import files
import os, sys
# Install Kaggle library
!pip install -q kaggle

os.chdir('/root/.kaggle')

# Upload kaggle API key file
uploaded = files.upload()

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import os
!kaggle datasets download -d tongpython/cat-and-dog

import os, sys
import tensorflow as tf
os.listdir()

#!unzip cat-and-dog.zip

os.getcwd()

os.listdir()

os.chdir('/root/.kaggle/training_set/training_set')

os.listdir()

train_dir = '/root/.kaggle/training_set/training_set'
test_dir = '/root/.kaggle/test_set/test_set'
default_dir = '/root/.kaggle'

train_cat, train_dog, test_cat, test_dog = [], [],[],[]
def get_data():
    os.chdir(default_dir)
    # get data's on training cat
    current_dir = train_dir+'/cats'
    os.chdir(current_dir)
    train_data_cat = os.listdir()
    train_cat.extend(train_data_cat)
    
    # get data's on training dog
    current_dir = train_dir +'/dogs'
    os.chdir(current_dir)
    train_data_dog = os.listdir()
    train_dog.extend(train_data_dog)
    
    # get data's on test cat
    current_dir = test_dir+'/cats'
    os.chdir(current_dir)
    test_data_cat = os.listdir()
    test_cat.extend(test_data_cat)
    
    # get data's on test dog
    current_dir = test_dir +'/dogs'
    os.chdir(current_dir)
    test_data_dog = os.listdir()
    os.chdir(default_dir)
    test_dog.extend(test_data_dog)
    return

get_data()

print('Number of cats in our train data is: ', len(train_cat))
print('Number of dog in our train data is: ', len(train_dog))
print('Number of cats in our test data is: ', len(test_cat))
print('Number of dogs in our test data is: ', len(test_dog))
print('Total training data is: ', len(train_cat)+len(train_dog))
print('Total test data is: ', len(test_cat)+len(test_dog))

import numpy as np
np.random.seed(100)

import keras
from keras.preprocessing import image

train_images = []
train_target = []
test_images = []
test_target = []


for i in train_cat:
    try:
        directory = train_dir + '/cats/' + i
        img = image.load_img(directory, target_size = (224,224), grayscale = False)
        img=image.img_to_array(img)
        img = img/255
        train_images.append(img)
        os.chdir(default_dir)
        train_target.append(0)
    except OSError as err:
        continue

for i in train_dog:
    try:
        directory = train_dir + '/dogs/' + i
        img = image.load_img(directory, target_size = (224,224), grayscale = False)
        img=image.img_to_array(img)
        img = img/255
        train_images.append(img)
        os.chdir(default_dir)
        train_target.append(1)
    
    except OSError as err:
        continue

for i in test_cat:
    try:
        directory = test_dir + '/cats/' + i
        img = image.load_img(directory, target_size = (224,224), grayscale = False)
        img=image.img_to_array(img)
        img = img/255
        test_images.append(img)
        os.chdir(default_dir)
        test_target.append(0)
    except OSError as err:
        continue

for i in test_dog:
    try:
        directory = test_dir + '/dogs/' + i
        img = image.load_img(directory, target_size = (224,224), grayscale = False)
        img=image.img_to_array(img)
        img = img/255
        test_images.append(img)
        os.chdir(default_dir)
        test_target.append(1)
    
    except OSError as err:
        pass

train_images = np.array(train_images)
test_images = np.array(test_images)
train_target = np.array(train_target)
test_target = np.array(test_target)
train_images.shape, test_images.shape, train_target.shape, test_target.shape

import tensorflow as tf

from tensorflow.keras import layers, models
import matplotlib.pyplot as plt

model = models.Sequential()
model.add(layers.Conv2D(32, (7,7), activation='relu', input_shape=(224,224, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(16, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(8, (2, 2), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(300, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(2, activation = 'softmax'))

model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

history = model.fit(train_images, train_target, epochs=10, 
                    validation_data=(test_images, test_target))

plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')

test_loss, test_acc = model.evaluate(test_images,  test_target, verbose=2)

print(test_acc)

"""# data image generators"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os
import numpy as np
import matplotlib.pyplot as plt

train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

batch_size = 100
target_size = (224,224)
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=target_size,
                                                           class_mode='binary')

val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=test_dir,
                                                              target_size=target_size,
                                                              class_mode='binary')

"""# visualize training image"""

sample_training_images, _ = next(train_data_gen)

def plotImages(images_arr):
    fig, axes = plt.subplots(1, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

plotImages(sample_training_images[:5])

model = models.Sequential()
model.add(layers.Conv2D(32, (7,7), activation='relu', input_shape=(224,224, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(16, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(8, (2, 2), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(300, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(2, activation = 'softmax'))
model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs = 10
history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=8005// batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=2023// batch_size
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss=history.history['loss']
val_loss=history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(30, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

"""# Augumentation

### applying horizontal flip
"""

image_gen = ImageDataGenerator(rescale=1./255, horizontal_flip=True)
train_data_gen = image_gen.flow_from_directory(batch_size=batch_size,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=target_size)

"""### take one sample of the image and repeat augumentation 5 times"""

augmented_images = [train_data_gen[0][0][0] for i in range(5)]

# Re-use the same custom plotting function defined and used
# above to visualize the training images
plotImages(augmented_images)

"""### randomly rotate the image"""

image_gen = ImageDataGenerator(rescale=1./255, rotation_range=45)

train_data_gen = image_gen.flow_from_directory(batch_size=batch_size,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=target_size)

augmented_images = [train_data_gen[0][0][0] for i in range(5)]

plotImages(augmented_images)

"""# apply zoom augumentation"""

# zoom_range from 0 - 1 where 1 = 100%.
image_gen = ImageDataGenerator(rescale=1./255, zoom_range=0.5) #

train_data_gen = image_gen.flow_from_directory(batch_size=batch_size,
                                               directory=train_dir,
                                               shuffle=True,
                                               target_size=target_size)

augmented_images = [train_data_gen[0][0][0] for i in range(5)]

plotImages(augmented_images)

"""# putting it all together"""

image_gen_train = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=45,
                    width_shift_range=.15,
                    height_shift_range=.15,
                    horizontal_flip=True,
                    zoom_range=0.5
                    )

train_data_gen = image_gen_train.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     shuffle=True,
                                                     target_size=target_size,
                                                     class_mode='binary')

augmented_images = [train_data_gen[0][0][0] for i in range(5)]
plotImages(augmented_images)

"""# create validator data generator"""

image_gen_val = ImageDataGenerator(rescale=1./255)

val_data_gen = image_gen_val.flow_from_directory(batch_size=batch_size,
                                                 directory=test_dir,
                                                 target_size=target_size,
                                                 class_mode='binary')

model = models.Sequential()
model.add(layers.Conv2D(32, (7,7), activation='relu', input_shape=(224,224, 3)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(16, (5, 5), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(8, (2, 2), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(300, activation='relu'))
model.add(layers.Dense(100, activation='relu'))
model.add(layers.Dense(2, activation = 'softmax'))
model.summary()

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs = 10
history = model.fit_generator(
    train_data_gen,
    steps_per_epoch=8005// batch_size,
    epochs=epochs,
    validation_data=val_data_gen,
    validation_steps=2023// batch_size
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(30, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

