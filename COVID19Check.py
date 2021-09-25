# import required libraries 
from keras.models import Sequential

#import the required layers
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

# create ur CNN Model 
network=Sequential()

#adding the layers

#first Conv layer
network.add(Conv2D(32,3,3,input_shape=(64,64,3),activation='relu'))

#Pooling layer
network.add(MaxPooling2D(pool_size=(2,2)))

#add second convolution and pooling layer.
network.add(Conv2D(32,3,3,activation='relu'))
network.add(MaxPooling2D(pool_size=(2,2)))

#Flattening layer
network.add(Flatten())

#Fully connected layers
network.add(Dense(256,activation='relu'))
network.add(Dense(1,activation='sigmoid'))

#let's see a summary of our model
network.summary()

#import ur optimizer
from keras.optimizers import Adam

#compiling the cnn
network.compile(optimizer=Adam(lr=0.001), loss='binary_crossentropy', metrics = ['accuracy'])

#download the dataset
!wget http://cb.lk/covid_19
!unzip covid_19

#prepare the data for training

#import required ibraries for imageprocessing
from keras.preprocessing.image import ImageDataGenerator #Generate batches of tensor image data with real-time data augmentation.

# keep in mind that it is very important to normalise ur image. the RGB values are between 0 and 255. so using rescale=1./255 will normalise the image. 
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1./255)

#generate ur training and testing dataset
training_set = train_datagen.flow_from_directory(
        '/content/CovidDataset/Train',
        target_size=(64,64),
        batch_size=32,
        class_mode='binary')

test_set = test_datagen.flow_from_directory(
        '/content/CovidDataset/Val',
        target_size=(64,64),
        batch_size=32,
        class_mode='binary')
#train the CNN model over the training dataset
results=network.fit(training_set,epochs=30)

# visualizing results
import matplotlib.pyplot as plt

def plot_acc_loss(results, epochs):
  acc = results.history['accuracy']
  loss = results.history['loss']
  
  plt.plot(range(1,epochs), acc[1:], label='Train_acc')
  plt.title('Accuracy over ' + str(epochs) + ' Epochs')
  plt.show()

  plt.plot(range(1,epochs), loss[1:], label='Train_loss')
  plt.title('loss over ' + str(epochs) + ' Epochs')
  plt.show()
  
 
plot_acc_loss(results, 30)

#lets evaluate our model over the testing dataset
network.evaluate(test_set)

#let's get an idea about our class indices to assess our model
print(test_set.class_indices)

from keras.preprocessing import image
import numpy as np

#let's choose an image form the covid dataset. what would the neural network predict
test_image = image.load_img('/content/CovidDataset/Val/Covid/16654_1_1.png', target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
print(network.predict(test_image)[0][0])


#let's choose an image from the covid dataset. what would the neural network predict
test_image = image.load_img('/content/CovidDataset/Val/Normal/NORMAL2-IM-0873-0001.jpeg', target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
print(network.predict(test_image)[0][0])

#let's choose an image from the covid dataset. what would the neural network predict
test_image = image.load_img('/content/CovidDataset/Val/Covid/16654_1_1.png', target_size = (64,64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
print(network.predict(test_image)[0][0])
