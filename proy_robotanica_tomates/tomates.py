from glob import glob1
from pickle import FALSE
import cv2
import numpy as np

"""
Funcion de debug que abre una imagen dada en un popup. Si se quieren mostrar todas las imagenes, se cambia el valor debug por defecto

- titulo: titulo de la ventana emergente que muestra la imagen
- img: imagen a mostrar
- debug: indica si se quiere mostrar la imagen. Por defecto esta desactivada
"""

def debug_mostrar_imagen(titulo, img, debug = False):
    if not debug:
        return

    cv2.imshow(titulo, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



"""
Indica el porcentaje de un color dado en una imagen. En este caso se usa para detectar la madurez (% de color rojizo)

- color: color base para deteccion
- diff: ayuda a establecer un rango de colores a partir de la base
- scaleParent: valor de reescalado (0 < n < 1)
- mask_def: mascara que indique las zonas en las que existe el color rojizo (se obtiene de detectar_tomates())
"""

def calcular_porcentaje_de_color(color, diff, scalePercent, img, mask_def):

    #intervalos aplicados + valores en orden (en cv2 es BGR, no RGB)
    rgbs = []

    rgbs.append(color[2])
    rgbs.append(color[1]-diff)
    rgbs.append(color[0]-diff)
    rgbs.append(color[2]+diff)
    rgbs.append(color[1]+diff)
    rgbs.append(color[0]+diff)

    for i in range(0, 6):
        if rgbs[i] > 255:
            rgbs[i] = 255
        elif rgbs[i] < 0:
            rgbs[i] = 0

    boundaries = [([rgbs[0], rgbs[1], rgbs[2]], [rgbs[3], rgbs[4], rgbs[5]])]
    
    #reescalado de la imagen y la mascara para un mejor resultado
    width = int(img.shape[1] * scalePercent)
    height = int(img.shape[0] * scalePercent)
    newSize = (width, height)
    img = cv2.resize(img, newSize, None, None, None, cv2.INTER_AREA)
    mask_def = cv2.resize(mask_def, newSize, None, None, None, cv2.INTER_AREA)

    #paso la mascara a escala de grises para poder distinguir los valores en negro
    gray_mask = cv2.cvtColor(mask_def, cv2.COLOR_BGR2GRAY)

    #aplico mascara a la imagen para que nunca pueda tener un numerador mayor al denominador
    img = cv2.bitwise_and(img, img, mask= gray_mask)

    for (lower, upper) in boundaries:

        #menor y mayor valor del color
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # mascara para obtener los pixeles de ese color
        mask = cv2.inRange(img, lower, upper)

        debug_mostrar_imagen("Mascara binaria", mask)
            
        #diferencia cantidad pixeles en la mascara y en el espacio obtenido con los contornos
        num = cv2.countNonZero(mask)
        den = cv2.countNonZero(gray_mask)
        if den < 1:
            den = 1

        if num > den:
            print("Error inesperado en la mascara")
            return

        ratio_color = num/den

        #un pequenyo ajuste de valores ya que puede que el borde no sea del todo exacto y arrastre valores que no debería arrastrar
        ratio_color += ratio_color / 12

        if ratio_color > 1:
            ratio_color = 1

        #paso a porcentaje con 2 decimales
        colorPercent = (ratio_color * 100)
        colorPercent = np.round(colorPercent, 2)

        print('porcentaje de rojo tomate: ' + str(colorPercent))

        debug_mostrar_imagen("Imagen", img)

    return colorPercent


"""
Funcion que se encarga de detectar los tomates en una imagen.
Para cada deteccion llama a la funcion calcular_porcentaje_de_color()

- upper_color, lower_color: rango de colores del tomate
- og_img: imagen original
- test: activo solo si estoy realizando un test
"""

def detectar_tomates(upper_color, lower_color, og_img, test = False):

    #pasamos la imagen a hsv
    hsv = cv2.cvtColor(og_img,cv2.COLOR_BGR2HSV)

    debug_mostrar_imagen("HSV", hsv)

    #se crea una mascara sobre los colores detectados
    mask = cv2.inRange(hsv, lower_color, upper_color)

    #se aplica la mascara
    res = cv2.bitwise_and(og_img, og_img, mask= mask)

    debug_mostrar_imagen("Mascara aplicada", res)

    #se pasa a gris
    img_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    #se desenfoca para suavizarla un poco. El ultimo valor es clave para evitar ruido dentro de la imagen
    imagen_desenfocada = cv2.GaussianBlur(img_gray,(65,65),5)

    debug_mostrar_imagen("Desenfocada", imagen_desenfocada)

    #se aplica Canny para detectar los bordes
    imagen_canny = cv2.Canny(imagen_desenfocada, 25, 25)

    debug_mostrar_imagen("Canny", imagen_canny)

    #se aplica un desenfoque al canny para identificar los bordes correctamente
    imagen_canny_desenfocada = cv2.GaussianBlur(imagen_canny,(15,15),0)

    debug_mostrar_imagen("Canny desenfocada", imagen_canny_desenfocada)

    #busqueda de contornos
    contornos, _ = cv2.findContours(imagen_canny_desenfocada.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

    #variable de testeo
    test_i = 0

    # Iteramos sobre los contornos
    # Si solo hay un tomate, deberia haber un unico contorno
    for contorno in contornos:

        img = og_img.copy()
        
        poligonoAproximado = cv2.approxPolyDP(contorno, 1, True)

        #mascara que mantendra el interior de los contornos. El resto se quedara en negro
        mask_def = np.zeros_like(img)

        # Basandonos en el numero de curvas poligonales determinamos de que
        # forma geometrica se trata en cada caso
        numeroCurvas = len(poligonoAproximado)
        
        #se le pone un minimo de curvas. Puede que sea importante en fotos con mas elementos (pero OJO, que puede dar problemas si no se conocen bien las dimensiones)
        if numeroCurvas >= 10 and poligonoAproximado.size > 20:

            #variable de testeo
            test_i += 1

            # Buscamos las coordenadas donde queremos escribir el nombre del elemento
            x = poligonoAproximado.ravel()[0]
            y = poligonoAproximado.ravel()[1] - 5

            #dibujo el contorno sobre la imagen original
            #cv2.drawContours(img, [poligonoAproximado], 0, (0,0,0), 5)
            
            #coloreo la mascara final
            cv2.drawContours(mask_def, [poligonoAproximado], 0, 255, -1)
            out = np.zeros_like(img)
            out[mask_def == 255] = 255

            debug_mostrar_imagen("Mascara final", out)

            #busco su porcentaje de color para ver la madurez
            porcentaje = calcular_porcentaje_de_color([200, 75, 17], 70, 0.4, img, mask_def)

            #pongo un texto encima del tomate en la imagen original
            txt = "Madurez: " + str(porcentaje) + "%"
            cv2.putText(og_img, txt, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0))

    if test:
        return (porcentaje, test_i)

    return og_img



def main(args=None):

    #importamos la imagen
    nombre_img = "lvl2"
    extension = ".png"
    archivo = nombre_img + extension
    img = cv2.imread(archivo)


    #se eligen los limites de color (en hsv)
    upper_color = np.array([110, 218, 229])
    lower_color = np.array([0, 0, 0])

    img_final = detectar_tomates(upper_color, lower_color, img)

    debug_mostrar_imagen("Imagen final", img_final)
    archivo = "resultado_" + archivo
    cv2.imwrite(archivo, img_final)



if __name__=='__main__':
    main()