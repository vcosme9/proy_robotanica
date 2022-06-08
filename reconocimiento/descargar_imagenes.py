from os import makedirs
from imutils import paths
import requests
import cv2
import os
import shutil

"""
Descarga imágenes a partir del archivo "urls.txt".
inputFile = ruta a "urls.txt"
outputDir = ruta a la carpeta donde ses guardarán todas las imágenes de una clase.

Al final del documento se hace una llamada a la función proporcionando el nombre de la subcarpeta ("original")
y el nombre de la clase para una nueva subcarpeta
"""

def descargar_imagenes(nombre):
    # Parámetros de entrada
    inputFile = r"C:\Users\User\Desktop\GTI\3\3b\ProyectoR\Reconocimiento\urls.txt"
    outputDir  = r"C:\Users\User\Desktop\GTI\3\3b\ProyectoR\Reconocimiento\images\\" + nombre

    if os.path.exists(outputDir):  #Si exite la carpeta
        shutil.rmtree(outputDir)   #la borramos
    makedirs(outputDir, exist_ok=True) #creamos carpeta para guardar fotos

    # obtén la lista de URLs del fichero
    rows = open(inputFile).read().strip().split("\n")
    print(rows[0])
    total = 0         # Número de imagenes descargadas

    for url in rows:  # para cada URL 
        try:        		# intenta descargar el fichero
            r = requests.get(url, timeout=60) # descarga imagen
            p = os.path.sep.join([outputDir, "{}.jpg".format(
                str(total).zfill(8))])    # nombre del fichero de descarga
            f = open(p, "wb")
            f.write(r.content)          # escribimos imagen en fichero
            f.close()
            print("[INFO] descargado: {}".format(p))
            total += 1
        except:
            print("[ERROR] descarganco {}...skipping".format(p))
    
    for imagePath in paths.list_images(outputDir):
        delete = False                # ¿la imagen ha de ser borrada?
        try:                          # intentamos leerla usando OpenCV  
            image = cv2.imread(imagePath)
            if image is None:           # si no ha sido cargada correctamente
                delete = True             # marcamos que hay que borrarla
        except:                       # si hay problemas con la imagen
            delete = True               # marcamos que hay que borrarla
            print("Except")             
        if delete:                    # si hay que borrarla
            print("[INFO] deleting {}".format(imagePath))
            os.remove(imagePath)        # la borramos


descargar_imagenes("original\\pimenton")