"""Clasificador KNN sobre un dataset de clientes y efecto de la dimensionalidad.

Entrena el modelo con tres caracteristicas, compara la prediccion para distintos
valores de K y mide como se comportan las distancias al aumentar las dimensiones.
"""

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Edad, salario en miles, numero de hijos
X_ENTRENAMIENTO = np.array([
    [20, 30, 0],
    [22, 32, 0],
    [25, 28, 1],
    [30, 40, 1],
    [33, 38, 2],
    [35, 45, 2],
    [38, 52, 1],
    [40, 50, 2],
    [45, 60, 3],
    [50, 65, 2],
    [55, 70, 3],
    [60, 75, 1],
])

# 0 = NO COMPRA, 1 = COMPRA
Y_ENTRENAMIENTO = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])

CLIENTE_NUEVO = np.array([[32, 42, 1]])
VALORES_K = [1, 3, 5]
DIMENSIONES = [2, 10, 100, 1000]
SEMILLA = 42


def clasificar(k: int) -> tuple[int, np.ndarray]:
    """Entrena con K vecinos y devuelve la prediccion y las distancias usadas."""
    modelo = KNeighborsClassifier(n_neighbors=k)
    modelo.fit(X_ENTRENAMIENTO, Y_ENTRENAMIENTO)
    distancias, _ = modelo.kneighbors(CLIENTE_NUEVO)
    return int(modelo.predict(CLIENTE_NUEVO)[0]), distancias[0]


def contraste_de_distancias(dimensiones: int, semilla: int) -> float:
    """Mide que tan lejos quedan entre si el vecino mas cercano y el mas lejano.

    Un valor alto significa que las distancias discriminan; uno cercano a cero,
    que todos los puntos estan practicamente a la misma distancia.
    """
    rng = np.random.default_rng(semilla)
    puntos = rng.random((500, dimensiones))
    consulta = rng.random(dimensiones)

    distancias = np.linalg.norm(puntos - consulta, axis=1)
    return (distancias.max() - distancias.min()) / distancias.min()


if __name__ == "__main__":
    print("Prediccion para el cliente (32 años, 42k, 1 hijo):\n")
    for k in VALORES_K:
        clase, distancias = clasificar(k)
        etiqueta = "COMPRA" if clase == 1 else "NO COMPRA"
        vecinos = ", ".join(f"{d:.2f}" for d in distancias)
        print(f"K = {k}: {etiqueta}  (distancias: {vecinos})")

    print("\nContraste entre el vecino mas lejano y el mas cercano:\n")
    for dimensiones in DIMENSIONES:
        contraste = contraste_de_distancias(dimensiones, SEMILLA)
        print(f"{dimensiones:>5} dimensiones: {contraste:.2f}")