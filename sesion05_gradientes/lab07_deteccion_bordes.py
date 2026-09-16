"""Deteccion de bordes con los operadores de Sobel y el algoritmo de Canny.

Separa los bordes verticales de los horizontales, los combina en la magnitud
del gradiente y contrasta el resultado con Canny bajo tres pares de umbrales.
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

RUTA_IMAGEN = "img/ciudad.jpg"
RUTA_PANEL_SOBEL = "img/lab07_sobel.png"
RUTA_PANEL_CANNY = "img/lab07_canny.png"
UMBRALES = [(10, 50), (50, 150), (200, 250)]


def magnitud_gradiente(sobel_x: np.ndarray, sobel_y: np.ndarray) -> np.ndarray:
    """Combina ambas derivadas con el teorema de Pitagoras."""
    magnitud = np.sqrt(sobel_x**2 + sobel_y**2)
    return cv2.convertScaleAbs(magnitud)


def guardar_panel(resultados: dict[str, np.ndarray], ruta: str) -> None:
    """Guarda los resultados en una fila; por SSH no hay display."""
    _, ejes = plt.subplots(1, len(resultados), figsize=(8 * len(resultados), 6))
    for eje, (titulo, imagen) in zip(ejes, resultados.items()):
        eje.imshow(imagen, cmap="gray")
        eje.set_title(titulo)
        eje.axis("off")
    plt.tight_layout()
    plt.savefig(ruta, dpi=120)
    plt.close()  # matplotlib acumula figuras si no se cierran


if __name__ == "__main__":
    imagen = cv2.imread(RUTA_IMAGEN, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise FileNotFoundError(RUTA_IMAGEN)

    # CV_64F conserva los negativos y los valores por encima de 255 que produce
    # la derivada; en uint8 se perderian los bordes de claro a oscuro.
    sobel_x = cv2.Sobel(imagen, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(imagen, cv2.CV_64F, 0, 1, ksize=3)

    guardar_panel(
        {
            "Sobel X (bordes verticales)": cv2.convertScaleAbs(sobel_x),
            "Sobel Y (bordes horizontales)": cv2.convertScaleAbs(sobel_y),
            "Magnitud del gradiente": magnitud_gradiente(sobel_x, sobel_y),
        },
        RUTA_PANEL_SOBEL,
    )

    guardar_panel(
        {f"Canny {bajo}-{alto}": cv2.Canny(imagen, bajo, alto) for bajo, alto in UMBRALES},
        RUTA_PANEL_CANNY,
    )

    for bajo, alto in UMBRALES:
        bordes = cv2.Canny(imagen, bajo, alto)
        porcentaje = np.count_nonzero(bordes) / bordes.size * 100
        print(f"Canny {bajo}-{alto}: {porcentaje:.2f}% de pixeles marcados como borde")

    print(f"Paneles guardados en {RUTA_PANEL_SOBEL} y {RUTA_PANEL_CANNY}")