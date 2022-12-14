# -*- coding: utf-8 -*-
"""cnn-image-recognition-iris.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/131FnN1D-Elm9JxH_LuV-08IJ_3MXilVZ
"""

import numpy as np
import tensorflow as tf

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense,Conv2D, MaxPool2D,Flatten
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import confusion_matrix, accuracy_score
from keras.preprocessing.image import ImageDataGenerator # This is deprecated, should use https://www.tensorflow.org/api_docs/python/tf/keras/utils/image_dataset_from_directory
from keras.utils import load_img
from keras.utils import img_to_array
from keras.preprocessing import image
from keras.backend import reverse
import matplotlib.pyplot as plt

!rm -R py-ml-mand-2-cnn-iris/
!git clone https://github.com/SirMeows/py-ml-mand-2-cnn-iris

target_size = 256
#input_img_size = 256
batch_size = 5
no_of_filters = 32
color = 'rgb'
class_mode ='categorical'
img_dir = '/content/py-ml-mand-2-cnn-iris/iris_images'
adam = Adam(learning_rate = 0.001)

datagen = ImageDataGenerator(
    rescale = 1./255, 
    shear_range = 0.2, 
    zoom_range = 0.2, 
    horizontal_flip = True, 
    validation_split = 0.1)

training_set = datagen.flow_from_directory(
        directory = img_dir,
        subset = 'training',
        shuffle = True,
        target_size = (target_size, target_size),
        batch_size = batch_size,
        class_mode = class_mode,
        color_mode= color)

class_names = training_set.class_indices.keys()
nr_of_classes = len(class_names)

validation_set = datagen.flow_from_directory(
        directory = img_dir,
        subset = 'validation',
        shuffle = True,
        target_size = (target_size, target_size),
        batch_size = batch_size,
        class_mode = class_mode,
        color_mode = color)

model = Sequential()

model.add(Conv2D(
    filters = no_of_filters,
    kernel_size = 3,
    activation = "relu",
    input_shape = [target_size, target_size, 3]))

model.add(MaxPool2D(pool_size = 2, strides = 2))

model.add(Flatten())

model.add(Dense(units = 512, activation = 'relu'))
model.add(Dense(units = 96, activation = 'relu'))

model.add(Dense(units = nr_of_classes, activation = "softmax"))

model.compile(
    optimizer =adam, 
    loss ='categorical_crossentropy', 
    metrics =['categorical_accuracy'])

history = model.fit(x = training_set, epochs = 25)

validation_result = model.evaluate(validation_set)
print('')
# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

def print_result(class_names, result):
  
  res_dict = dict(zip(class_names, result[0]))
  res_sorted = dict(sorted(res_dict.items(), key=lambda item: item[1], reverse=True))

  for k, v in res_sorted.items():
      print(f'{k.ljust(20)} : {v:.5f}')

@tf.autograph.experimental.do_not_convert
def single_img_predict(img_path):
  test_image = load_img(img_path, target_size=[target_size, target_size], color_mode=color)
  test_image = img_to_array(test_image)
  test_image = np.expand_dims(test_image,axis=0)

  result = model.predict(test_image/255.0)

  print_result(class_names, result)

print('setosa:')
single_img_predict('/content/py-ml-mand-2-cnn-iris/iris_images/iris-setosa/iris-793fe85ddd6a97e9c9f184ed20d1d216e48bf85aa71633eff6d27073e0825d54.jpg')
print('')
print('versicolour:')
single_img_predict('/content/py-ml-mand-2-cnn-iris/iris_images/iris-versicolour/iris-1ebcf1f677f52264e57ad6203b81034886a7427b943516f97d261ff7850b00eb.jpg')
print('')
print('virginica:')
single_img_predict('/content/py-ml-mand-2-cnn-iris/iris_images/iris-virginica/iris-3eed72bc2511f619190ce79d24a0436fef7fcf424e25523cb849642d14ac7bcf.jpg')

model.save('iris_model.h5')

# summarize history for accuracy
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()