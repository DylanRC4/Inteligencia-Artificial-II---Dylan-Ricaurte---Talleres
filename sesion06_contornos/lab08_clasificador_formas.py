"""Clasificador de formas: pipeline completo de grises a caracteristicas geometricas.

Encadena las etapas de las sesiones anteriores (grises, umbralizacion, limpieza
morfologica) para extraer contornos y clasificar cada objeto por su area.
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

RUTA_IMAGEN = "img/monedas.jpg"
RUTA_SALIDA = "img/lab08_objetos.png"
KERNEL = np.ones((5, 5), np.uint8)
BLOQUE = 51       # vecindad para el umbral local, impar y mayor que una moneda
CONSTANTE = 10    # margen que se resta a la media local
AREA_MINIMA = 300      # descarta motas de ruido, no objetos reales
AREA_GRANDE = 5000  # punto medio del salto entre 4336 y 6161 px
AZUL = (255, 0, 0)
ROJO = (0, 0, 255)


def segmentar(imagen: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """Binariza con umbral adaptativo y limpia el resultado con una apertura."""
    # Un umbral global falla: el fondo tiene un degradado, asi que ningun valor
    # unico separa las monedas claras sin recoger la zona inferior mas oscura.
    binaria = cv2.adaptiveThreshold(
        imagen, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, BLOQUE, CONSTANTE,
    )
    return cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, kernel)


def centroide(contorno: np.ndarray) -> tuple[int, int] | None:
    """Centro de masa a partir de los momentos espaciales."""
    momentos = cv2.moments(contorno)
    if momentos["m00"] == 0:
        return None
    return int(momentos["m10"] / momentos["m00"]), int(momentos["m01"] / momentos["m00"])


if __name__ == "__main__":
    gris = cv2.imread(RUTA_IMAGEN, cv2.IMREAD_GRAYSCALE)
    if gris is None:
        raise FileNotFoundError(RUTA_IMAGEN)

    binaria = segmentar(gris, KERNEL)
    contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    anotada = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
    objetos = 0

    for contorno in contornos:
        area = cv2.contourArea(contorno)
        if area < AREA_MINIMA:
            continue

        objetos += 1
        x, y, ancho, alto = cv2.boundingRect(contorno)
        color = AZUL if area > AREA_GRANDE else ROJO
        cv2.rectangle(anotada, (x, y), (x + ancho, y + alto), color, 2)

        centro = centroide(contorno)
        if centro:
            cv2.circle(anotada, centro, 4, (0, 255, 0), -1)

        tamano = "grande" if area > AREA_GRANDE else "pequeño"
        print(f"Objeto {objetos}: area {area:.0f} px, box {ancho}x{alto}, {tamano}")

    print(f"\nTotal de objetos detectados: {objetos}")

    plt.figure(figsize=(12, 8))
    plt.imshow(cv2.cvtColor(anotada, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(RUTA_SALIDA, dpi=120)
    plt.close()
    print(f"Imagen anotada guardada en {RUTA_SALIDA}")