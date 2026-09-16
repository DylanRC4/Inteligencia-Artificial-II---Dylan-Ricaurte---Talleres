"""Comparacion de tres estrategias de suavizado sobre ruido de sal y pimienta.

Genera ruido de impulso de forma controlada y aplica los filtros de media,
gaussiano y mediana con un kernel agresivo para contrastar sus efectos.
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np

RUTA_IMAGEN = "img/documento.jpg"
RUTA_PANEL_A = "img/lab06_ruido_y_media.png"
RUTA_PANEL_B = "img/lab06_gaussiano_y_mediana.png"
KERNEL = 7
PROPORCION_RUIDO = 0.05
SEMILLA = 42


def agregar_sal_y_pimienta(imagen: np.ndarray, proporcion: float, semilla: int) -> np.ndarray:
    """Corrompe una fraccion de pixeles al azar con los valores 0 y 255."""
    rng = np.random.default_rng(semilla)
    ruidosa = imagen.copy()  # sin copia se modificaria la imagen original

    cantidad = int(imagen.size * proporcion)
    filas = rng.integers(0, imagen.shape[0], size=cantidad)
    columnas = rng.integers(0, imagen.shape[1], size=cantidad)

    mitad = cantidad // 2
    ruidosa[filas[:mitad], columnas[:mitad]] = 0
    ruidosa[filas[mitad:], columnas[mitad:]] = 255
    return ruidosa


def guardar_pareja(resultados: dict[str, np.ndarray], ruta: str) -> None:
    """Guarda dos resultados lado a lado; por SSH no hay display."""
    _, ejes = plt.subplots(1, 2, figsize=(16, 5))
    for eje, (titulo, imagen) in zip(ejes, resultados.items()):
        eje.imshow(imagen, cmap="gray")
        eje.set_title(titulo)
        eje.axis("off")
    plt.tight_layout()
    plt.savefig(ruta, dpi=150)
    plt.close()  # matplotlib acumula figuras: sin cerrar, la segunda se dibuja encima


if __name__ == "__main__":
    imagen = cv2.imread(RUTA_IMAGEN, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        raise FileNotFoundError(RUTA_IMAGEN)

    ruidosa = agregar_sal_y_pimienta(imagen, PROPORCION_RUIDO, SEMILLA)
    resultados = {
        "Con ruido": ruidosa,
        "Media": cv2.blur(ruidosa, (KERNEL, KERNEL)),
        "Gaussiano": cv2.GaussianBlur(ruidosa, (KERNEL, KERNEL), 0),
        "Mediana": cv2.medianBlur(ruidosa, KERNEL),
    }

    for titulo, resultado in resultados.items():
        diferencia = np.abs(resultado.astype(np.int16) - imagen.astype(np.int16))
        print(f"{titulo}: error medio de {diferencia.mean():.2f} contra la original")

    guardar_pareja({k: resultados[k] for k in ("Con ruido", "Media")}, RUTA_PANEL_A)
    guardar_pareja({k: resultados[k] for k in ("Gaussiano", "Mediana")}, RUTA_PANEL_B)
    print(f"Paneles guardados en {RUTA_PANEL_A} y {RUTA_PANEL_B}")