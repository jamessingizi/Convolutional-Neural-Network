import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator


tf.__version__


train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

training_set = train_datagen.flow_from_directory(
        'dataset/training_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')


test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory(
        'dataset/test_set',
        target_size=(64, 64),
        batch_size=32,
        class_mode='binary')


cnn = tf.keras.models.Sequential()


cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu',input_shape=[64,64,3]))


cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))


cnn.add(tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size=2, strides=2))


cnn.add(tf.keras.layers.Flatten())


#units refers to hidden neurons
cnn.add(tf.keras.layers.Dense(units=128, activation='relu'))


#units =1 because this is a binary classification
cnn.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))


cnn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


cnn.fit(x=training_set, validation_data=test_set, epochs=25)


import numpy as np
from keras.preprocessing import image
test_image = image.load_img('dataset/single_prediction/cat_or_dog_2.jpg', target_size=(64,64))
test_image = image.img_to_array(test_image)
#add the batch dimension to test image since images were trained in batches
test_image = np.expand_dims(test_image, axis=0)
result = cnn.predict(test_image)
print(training_set.class_indices)

#in result[0][0] the first index represents the batch and the second index represents the actual prediction
if result[0][0] > 0.5:
    prediction = 'dog'
else:
    prediction = 'cat'

print(prediction)



