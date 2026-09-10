"""Taller de Laboratorio Final — Simulador basico de convolucion.

Calcula el valor que produce un kernel de realce 3x3 al superponerse sobre una
seccion de imagen, usando unicamente NumPy.
"""

import numpy as np


def aplicar_kernel(seccion: np.ndarray, kernel: np.ndarray) -> float:
    """Superpone el kernel sobre la seccion y devuelve el valor central.

    Args:
        seccion: Vecindario de la imagen, del mismo tamaño que el kernel.
        kernel: Filtro a aplicar.

    Returns:
        Valor resultante para el pixel central.

    Raises:
        ValueError: Si las formas no coinciden.
    """
    if seccion.shape != kernel.shape:
        raise ValueError(
            f"Las formas no coinciden: {seccion.shape} vs {kernel.shape}"
        )

    # El operador * multiplica posicion contra posicion, que es lo que
    # necesitamos: cada pixel debe cruzarse con el coeficiente que le queda
    # encima. Despues sumamos los nueve productos en un solo numero.
    return float(np.sum(seccion * kernel))


def main() -> None:
    seccion = np.array([
        [100, 100, 100],
        [100, 200, 100],
        [100, 100, 100],
    ], dtype=np.float32)

    kernel_realce = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0],
    ], dtype=np.float32)

    resultado = aplicar_kernel(seccion, kernel_realce)

    print("Seccion de imagen (I):", seccion, sep="\n")
    print("\nKernel de realce (K):", kernel_realce, sep="\n")
    print(f"\nPixel central original:   {seccion[1, 1]:.0f}")
    print(f"Pixel central resultante: {resultado:.0f}")


if __name__ == "__main__":
    main()