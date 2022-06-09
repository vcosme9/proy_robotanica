"""
Quita las url repetidas en el archivo "urls.txt" resultante de la función dada en el último colab de Tensorflow
"""


filename = r"C:\Users\User\Desktop\GTI\3\3b\ProyectoR\Reconocimiento\urls.txt"
lista_lineas = []
n_lista = []
repetidos = 0

with open(filename, mode="rt", encoding="utf-8") as f:
    lista_lineas = f.readlines()
    for linea in lista_lineas:
        if n_lista.count(linea.split("\n")[0]) == 0:
            n_lista.append(linea.split("\n")[0])
        else:
            repetidos += 1
    f.close()

with open(filename, mode="wt", encoding="utf-8") as f:
    res = ""
    for url in n_lista:
        res += str(url) + "\n"
    print("repetidos: " + str(repetidos))
    f.write(str(res))
    f.close()