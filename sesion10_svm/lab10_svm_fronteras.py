"""Frontera de maximo margen con SVM y limites del kernel lineal.

Reproduce el taller analitico con scikit-learn, comprueba que agregar un punto
lejano no mueve la frontera y contrasta el kernel lineal con el RBF cuando un
punto queda rodeado por la clase contraria.
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC

X_BASE = np.array([[2, 2], [3, 3], [4, 2], [6, 6], [7, 8], [8, 7]])
Y_BASE = np.array([0, 0, 0, 1, 1, 1])

RUTA_SALIDA = "img/lab10_fronteras.png"
GAMMA_RBF = 1.0


def agregar(punto: list[int], clase: int) -> tuple[np.ndarray, np.ndarray]:
    """Devuelve el dataset base con un punto extra de la clase indicada."""
    return np.vstack([X_BASE, punto]), np.append(Y_BASE, clase)


def entrenar(X: np.ndarray, y: np.ndarray, kernel: str) -> SVC:
    """Ajusta un SVM; el RBF usa un gamma fijo para no depender del heuristico."""
    gamma = GAMMA_RBF if kernel == "rbf" else "scale"
    return SVC(kernel=kernel, gamma=gamma).fit(X, y)


def ecuacion(modelo: SVC) -> str:
    """Escribe la frontera lineal en la forma x + y = c."""
    (w1, w2), b = modelo.coef_[0], modelo.intercept_[0]
    return f"x + {w2 / w1:.2f}y = {-b / w1:.2f}"


def dibujar(eje, modelo: SVC, X: np.ndarray, y: np.ndarray, titulo: str) -> None:
    """Colorea la region de decision evaluando el modelo sobre una malla del plano."""
    malla_x, malla_y = np.meshgrid(np.linspace(0, 10, 300), np.linspace(0, 10, 300))
    zonas = modelo.predict(np.c_[malla_x.ravel(), malla_y.ravel()]).reshape(malla_x.shape)

    eje.contourf(malla_x, malla_y, zonas, alpha=0.25, cmap="coolwarm")
    eje.scatter(X[y == 0][:, 0], X[y == 0][:, 1], s=90, c="tab:blue", label="Clase A")
    eje.scatter(X[y == 1][:, 0], X[y == 1][:, 1], s=90, c="tab:red", marker="x", label="Clase B")
    eje.scatter(modelo.support_vectors_[:, 0], modelo.support_vectors_[:, 1],
                s=280, facecolors="none", edgecolors="black", label="Vectores de soporte")
    eje.set(title=titulo, xlim=(0, 10), ylim=(0, 10))
    eje.legend(loc="upper left", fontsize=8)


if __name__ == "__main__":
    casos = {
        "Lineal, dataset original": (X_BASE, Y_BASE, "linear"),
        "Lineal + punto (1,1) lejano": (*agregar([1, 1], 0), "linear"),
        "Lineal + punto (7,7) rodeado": (*agregar([7, 7], 0), "linear"),
        "RBF + punto (7,7) rodeado": (*agregar([7, 7], 0), "rbf"),
    }

    modelos = {}
    for titulo, (X, y, kernel) in casos.items():
        modelo = entrenar(X, y, kernel)
        aciertos = int((modelo.predict(X) == y).sum())
        frontera = ecuacion(modelo) if kernel == "linear" else "curva (no lineal)"
        print(f"{titulo}")
        print(f"  aciertos: {aciertos}/{len(y)}   frontera: {frontera}")
        print(f"  vectores de soporte: {modelo.support_vectors_.tolist()}\n")
        modelos[titulo] = (modelo, X, y)

    _, ejes = plt.subplots(2, 2, figsize=(13, 11))
    for eje, (titulo, (modelo, X, y)) in zip(ejes.flat, modelos.items()):
        dibujar(eje, modelo, X, y, titulo)

    plt.tight_layout()
    plt.savefig(RUTA_SALIDA, dpi=120)
    plt.close()
    print(f"Panel guardado en {RUTA_SALIDA}")