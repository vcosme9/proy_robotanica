from tomates import *

"""
Tests del script "tomates.py"

Casos testeados:
    - Se le pasa un tomate inmaduro
    - Se le pasa un tomate maduro
"""


# Si le paso un tomate verdoso, el porcentaje de madurez deberia ser bajo (y solo debe detectar un tomate)
def test_tomate_verde():

    #importamos la imagen
    img = cv2.imread("lvl1.png")

    #se eligen los limites de color (en hsv)
    upper_color = np.array([110, 218, 229])
    lower_color = np.array([0, 0, 0])

    porcentaje, n = detectar_tomates(upper_color, lower_color, img, True)

    assert n == 1
    assert porcentaje < 40

# Si le paso un tomate rojizo, el porcentaje de madurez deberia ser alto (y solo debe detectar un tomate)
def test_tomate_rojo():

    #importamos la imagen
    img = cv2.imread("lvl6.png")

    #se eligen los limites de color (en hsv)
    upper_color = np.array([110, 218, 229])
    lower_color = np.array([0, 0, 0])

    porcentaje, n = detectar_tomates(upper_color, lower_color, img, True)

    assert n == 1
    assert porcentaje > 90

# Si le paso una imagen con varios tomates, los debe poder detectar todos
def test_varios_tomates():

    #importamos la imagen
    img = cv2.imread("seis_tomates.png")

    #se eligen los limites de color (en hsv)
    upper_color = np.array([110, 218, 229])
    lower_color = np.array([0, 0, 0])

    _, cantidad = detectar_tomates(upper_color, lower_color, img, True)

    assert cantidad == 6