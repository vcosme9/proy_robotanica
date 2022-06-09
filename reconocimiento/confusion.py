import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from collections import Counter
from sklearn.metrics import confusion_matrix
import itertools
import numpy as np
import keras
from keras_preprocessing.image import ImageDataGenerator

"""
muestra la matriz de confusión para saber la exactitud del modelo.
model = ruta al modelo
hay que pasar la ruta a la carpeta de validación (linea 28)
"""


#importo modelo
model = keras.models.load_model('C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/modelo_tpn.h5')

BATCH_SIZE = 100
WIDTH      = 250
HEIGHT     = 250

validation_datagen = ImageDataGenerator(
      rescale = 1./255)

validation_generator = validation_datagen.flow_from_directory(
	  "C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/images/validation",
    batch_size=BATCH_SIZE,
    #color_mode="grayscale",
	  target_size=(WIDTH, HEIGHT))


def plot_confusion_matrix(cm, classes_map,
                          normalize=False,
                          title='Matriz de Confusión',
                          cmap=plt.cm.Blues):
    """
    Esta función visualiza la matriz de confusión.
    Usa el parámetro `normalize=True` para normalizar los resultados.
    Note, this code is taken straight from the SKLEARN website, an nice way of viewing confusion matrix.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes_map))
    inv_map = {v: k for k, v in classes_map.items()}
    labels = inv_map.values()
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)
    if normalize:
        cm = np.around(cm.astype('float') / cm.sum(axis=1)[:, np.newaxis], 2)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('Clase real')
    plt.xlabel('Clase predicha')

"""
Obtener la matriz de confusión de un corpus creado desde un ImageDataGenerator 
es algo más complejo que el último ejemplo estudiado. El problema está en que las 
muestras son extraidas por lotes (bath) y la función 
confusion_matrix(validation_classes, y_pred) espera que sus dos parámetros sean 
vectores. Para resolverlo recorremos todos los lotes el generador y vamos 
concatenando los vectores adecuados.
Otra solución alternativa en:
https://stackoverflow.com/questions/47907061/how-to-get-confusion-matrix-when-using-model-fit-generator
"""
validation_classes = []
validation_images = []
for i in range( -(-validation_generator.samples // validation_generator.batch_size)):  # número de veces que podemos sacar batch redondeado hacia arriba
   batch = validation_generator.next()
   expected = np.argmax(batch[1], axis=1) 
   validation_classes.extend(expected)
   validation_images.extend(batch[0])
validation_classes = np.array(validation_classes)
validation_images = np.array(validation_images)
Y_pred = model.predict(validation_images)
y_pred = np.argmax(Y_pred, axis=1)
my_confussion = confusion_matrix(validation_classes, y_pred)
plot_confusion_matrix(my_confussion, classes_map = validation_generator.class_indices)#, normalize=True)
plt.show()