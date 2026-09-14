"""Segmentacion por umbralizacion y limpieza con morfologia matematica.

Binariza una fotografia con iluminacion despareja usando un umbral fijo y
compara dos formas de limpiar el resultado: apertura y cierre.
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

RUTA_IMAGEN = "img/documento.jpg"
RUTA_SALIDA = "img/lab05_comparacion.png"
UMBRAL = 127
KERNEL = np.ones((3, 3), np.uint8)


def binarizar(imagen: np.ndarray, umbral: int) -> np.ndarray:
    """Binariza dejando el texto en blanco y el papel en negro."""
    # INV porque la morfologia opera sobre los pixeles blancos: el objeto
    # de interes (el texto, que es oscuro) tiene que quedar en 255.
    _, binaria = cv2.threshold(imagen, umbral, 255, cv2.THRESH_BINARY_INV)
    return binaria


def apertura(binaria: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Erosion seguida de dilatacion: borra el ruido blanco del fondo."""
    erosionada = cv2.erode(binaria, kernel, iterations=1)
    return cv2.dilate(erosionada, kernel, iterations=1)


def cierre(binaria: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Dilatacion seguida de erosion: rellena los huecos del objeto."""
    dilatada = cv2.dilate(binaria, kernel, iterations=1)
    return cv2.erode(dilatada, kernel, iterations=1)


def guardar_panel(resultados: dict[str, np.ndarray], ruta: str) -> None:
    """Guarda las tres binarias lado a lado; por SSH no hay display."""
    _, ejes = plt.subplots(1, 3, figsize=(15, 5))
    for eje, (titulo, imagen) in zip(ejes, resultados.items()):
        eje.imshow(imagen, cmap="gray")
        eje.set_title(titulo)
        eje.axis("off")
    plt.tight_layout()
    plt.savefig(ruta)


if __name__ == "__main__":
    imagen = cv2.imread(RUTA_IMAGEN, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise FileNotFoundError(RUTA_IMAGEN)

    binaria = binarizar(imagen, UMBRAL)
    resultados = {
        "Binarizada": binaria,
        "Apertura": apertura(binaria, KERNEL),
        "Cierre": cierre(binaria, KERNEL),
    }

    for titulo, resultado in resultados.items():
        print(f"{titulo}: {np.count_nonzero(resultado)} pixeles blancos")

    guardar_panel(resultados, RUTA_SALIDA)
    print(f"Panel guardado en {RUTA_SALIDA}")
