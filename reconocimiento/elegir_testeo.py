from os import makedirs
from imutils import paths
import requests
import random
import os
import shutil
from PIL import Image
import PIL


"""
    elegir_testeo.py

    Dada una carpeta con todas las imagenes, se crearan una de training y otra de validacion con contenido aleatorio.
"""

"""
    crear_carpetas()

    Se crean y rellenan 2 carpetas: una con muestras de entrenamiento y otra con muestras de testeo.
    Solo se necesita de una carpeta con todas las imagenes.
"""

"""
clases = lista con el nombre de todas las clases
"""



def crear_carpetas(path_root, clase, validation_weight):
    
    #ruta con todas las imagenes
    path_og = path_root + "\\original\\" + clase
    #ruta de training
    path_from = path_root + "\\training\\" + clase
    #ruta de validacion
    path_to = path_root + "\\validation\\" + clase

    #si las carpetas de entrenamiento y testeo ya existen, las borro
    if os.path.exists(path_from):
            shutil.rmtree(path_from)
    if os.path.exists(path_to):
            shutil.rmtree(path_to)

    #creo la carpeta de testeo
    makedirs(path_to, exist_ok=True)

    #creo la carpeta de entrenamiento con todo el contenido
    shutil.copytree(path_og, path_from)

    #me hago una copia de los nombres de las fotos encontradas
    files = os.listdir(path_from).copy()

    #se cogen como testeo un 20% de las imagenes (y como minimo habra 1)
    n_samples = max([int(len(files) * validation_weight), 1])

    for i in range(0, n_samples):
        #elijo una al azar
        selected = random.choice(files)
        #la quito de la lista para que no pueda volver a salir aleatoriamente
        files.remove(selected)
        #abro la imagen seleccionada
        img = Image.open(path_from + "\\" + selected)
        
        try:
            #la guardo en la nueva carpeta
            img.save(path_to + "\\" + selected)
        except:
            #si falla la convierto a RGB (le quito la transparencia) y la guardo
            
            try:
                img = img.convert('RGB')
                img.save(path_to + "\\" + selected)
            except:
                print("nah")

        #la borro de la anterior
        os.remove(path_from + "\\" + selected)


clases = ["tomate", "pepino", "nada"]
ruta = r"C:\Users\User\Desktop\GTI\3\3b\ProyectoR\Reconocimiento\images"

#esto si quiero darle el mismo peso a todos (en este caso el 20% de fotos iran al muestreo):
for clase in clases:
    crear_carpetas(ruta, clase, 0.2)
