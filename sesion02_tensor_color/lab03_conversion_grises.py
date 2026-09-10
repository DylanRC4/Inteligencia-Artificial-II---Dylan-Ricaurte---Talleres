"""Conversión de BGR a escala de grises mediante producto punto ponderado."""

import cv2
import numpy as np

# Pesos de luminancia (ITU-R BT.601) reordenados a BGR, porque OpenCV
# carga los canales en ese orden y el vector debe coincidir.
PESOS_BGR = np.array([0.114, 0.587, 0.299])
RUTA_IMAGEN = "img/muestra.jpg"


def a_gris(bgr: np.ndarray) -> np.ndarray:
    """Aplica el producto punto ponderado sobre el último eje (los canales)."""
    return np.dot(bgr, PESOS_BGR)


if __name__ == "__main__":
    # Puntos 1 a 3: el amarillo puro paso a paso.
    amarillo = np.array([0, 255, 255])
    print(f"Pixel BGR de prueba: {amarillo}")
    print(f"Valor en escala de grises: {a_gris(amarillo):.2f}")

    # Punto 4: la misma función sobre un tensor completo, contra cvtColor.
    imagen = cv2.imread(RUTA_IMAGEN)
    gris_manual = a_gris(imagen)
    gris_opencv = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    diferencia = np.abs(gris_manual - gris_opencv).max()
    print(f"Diferencia maxima contra cvtColor: {diferencia:.2f}")