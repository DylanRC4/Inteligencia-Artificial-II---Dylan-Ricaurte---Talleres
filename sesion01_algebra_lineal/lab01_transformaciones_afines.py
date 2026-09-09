"""Taller de Laboratorio 1 — Transformaciones afines sobre matrices de imagen.

Corrige una radiografía sobreexpuesta usando la transformación
A_nueva = alpha * A + beta y dejando los valores dentro del rango de 8 bits.
"""

import numpy as np

RANGO_8BITS = (0, 255)


def ajustar_contraste_brillo(
    imagen: np.ndarray, alpha: float, beta: float
) -> np.ndarray:
    """Aplica la formula A_nueva = alpha * A + beta."""

    resultado = alpha * imagen.astype(np.float32) + beta

    # Primero dejo todos los valores entre 0 y 255.
    resultado = np.clip(resultado, *RANGO_8BITS)

    # Despues convierto la matriz al tipo entero uint8.
    resultado = resultado.astype(np.uint8)

    return resultado


def main() -> None:
    # Uso una semilla fija para que la matriz salga igual cada vez que se ejecute.
    generador = np.random.default_rng(seed=42)

    # Genero valores altos para simular una radiografia sobreexpuesta.
    original = generador.integers(200, 255, size=(5, 5), dtype=np.uint8)

    # Con alpha reduzco el contraste y con beta bajo el brillo.
    procesada = ajustar_contraste_brillo(
        original, alpha=0.5, beta=-50.0
    )

    print("Matriz original (sobreexpuesta):", original, sep="\n")
    print("\nMatriz procesada:", procesada, sep="\n")

    # Comparo el rango de valores antes y despues de la transformacion.
    print(f"\nAmplitud original:  {np.ptp(original)}")
    print(f"Amplitud procesada: {np.ptp(procesada)}")


if __name__ == "__main__":
    main()