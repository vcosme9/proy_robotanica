import tensorflow as tf
import keras_preprocessing
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator

"""
Script que entrenará el modelo, que se guardará en formato .h5 (también dentro de una carpeta por si acaso).
Hay que pasar las rutas de entrenamiento (linea 26) y de validación (linea 35)
"""

BATCH_SIZE = 100
WIDTH      = 250
HEIGHT     = 250

training_datagen = ImageDataGenerator(
      rescale = 1./255,
      rotation_range=5,
      width_shift_range=0.05,
      height_shift_range=0.05,
      zoom_range=0.3,
      horizontal_flip=True,
      shear_range=4,
      fill_mode='nearest')

train_generator = training_datagen.flow_from_directory(
	  "C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/images/training",
      batch_size=BATCH_SIZE,
      #color_mode="grayscale",
      target_size=(WIDTH, HEIGHT))

validation_datagen = ImageDataGenerator(
      rescale = 1./255)

validation_generator = validation_datagen.flow_from_directory(
	  "C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/images/validation",
      batch_size=BATCH_SIZE,
      #color_mode="grayscale",
      target_size=(WIDTH, HEIGHT))

##########################################################################

model = tf.keras.models.Sequential([
    #cambiar el último valor si es gris(1) o a color(3)
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(WIDTH, HEIGHT, 3)), 
    tf.keras.layers.MaxPooling2D(2, 2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.summary()

model.compile(loss = 'categorical_crossentropy', 
              optimizer='rmsprop', 
              metrics=['accuracy'])

history = model.fit(
    train_generator, 
    batch_size = BATCH_SIZE,
    epochs=25, #100
    validation_data = validation_generator,
    validation_batch_size = BATCH_SIZE)

model.save('C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/modelo_tpn.h5')
model.save('C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/modelo_tpn')