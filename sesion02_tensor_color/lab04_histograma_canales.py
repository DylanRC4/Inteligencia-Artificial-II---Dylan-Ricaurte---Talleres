"""Histogramas de los tres canales de color para analizar la iluminación."""

import cv2
import matplotlib.pyplot as plt

# Cada canal se grafica con su propio color para leer el gráfico de un vistazo.
# El orden sigue el de OpenCV: azul primero, rojo al final.
CANALES = [("Azul", "blue"), ("Verde", "green"), ("Rojo", "red")]
RUTA_IMAGEN = "img/muestra.jpg"
RUTA_GRAFICO = "img/lab04_histogramas.png"

imagen = cv2.imread(RUTA_IMAGEN)

for indice, (nombre, color) in enumerate(CANALES):
    histograma = cv2.calcHist([imagen], [indice], None, [256], [0, 256])
    plt.plot(histograma, color=color, label=nombre)

plt.title("Distribución de intensidades por canal")
plt.xlabel("Valor del píxel (0-255)")
plt.ylabel("Frecuencia (cantidad de píxeles)")
plt.legend()
plt.savefig(RUTA_GRAFICO)