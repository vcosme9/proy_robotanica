from PIL import Image
import cv2
import numpy as np
import keras

"""
Script para testear la predicción del modelo. Los posibles resultados son "Nada", "Tomate" y "Pepino"
model = ruta al model (.h5)
path = ruta a la imagen a testear
"""

model = keras.models.load_model('C:/Users/User/Desktop/GTI/3/3b/ProyectoR/Reconocimiento/modelo_tpn.h5')

path = r"C:\Users\User\Desktop\GTI\3\3b\ProyectoR\Reconocimiento\test_tomate.jpg"

img = cv2.imread(path)
img = cv2.resize(img, (250, 250))
img = np.expand_dims(img, axis=0)
prediction = model.predict_on_batch((img))
prediction_result = np.argmax(prediction[0])

if prediction_result == 0:
    res = "Nada"
elif prediction_result == 1:
    res = "Tomate"
elif prediction_result == 2:
    res = "Pepino"

print(res)