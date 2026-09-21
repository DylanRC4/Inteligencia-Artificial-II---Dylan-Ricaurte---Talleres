import numpy as np


# Funcion de Activacion: Sigmoide (devuelve un valor entre 0 y 1)
def sigmoide(x):
    return 1 / (1 + np.exp(-x))


# CAPA OCULTA (4 Neuronas)
# Matriz W1 de (3 entradas x 4 neuronas)
W1 = np.array([
    [0.1, 0.2, -0.3, 0.4],
    [-0.5, 0.6, 0.7, -0.8],
    [0.9, -0.1, 0.2, 0.3],
])
b1 = np.array([0.1, -0.2, 0.3, -0.4])  # 4 Sesgos

# CAPA DE SALIDA (1 Neurona)
# Matriz W2 de (4 entradas ocultas x 1 neurona final)
W2 = np.array([0.5, -0.6, 0.7, 0.8])
b2 = np.array([-0.1])


# Propagacion hacia adelante: la misma funcion sirve para 1 cliente o para un lote
def propagacion(X):
    Z1 = np.dot(X, W1) + b1
    A1 = sigmoide(Z1)  # Salida de la capa oculta

    Z2 = np.dot(A1, W2) + b2
    salida = sigmoide(Z2)
    return Z1, A1, salida


# 1. UN CLIENTE con 3 caracteristicas
X = np.array([0.5, 0.8, 0.2])
Z1, A1, salida = propagacion(X)

print("Un cliente")
print("  Z1 (valores puros):  ", np.round(Z1, 4))
print("  A1 (tras sigmoide):  ", np.round(A1, 4))
print("  Probabilidad:        ", np.round(salida, 4))

# 2. LOTE de 2 clientes al mismo tiempo, sin tocar las matrices de pesos
X_lote = np.array([
    [0.5, 0.8, 0.2],
    [0.1, 0.9, 0.9],
])
Z1, A1, salida = propagacion(X_lote)

print("\nLote de 2 clientes")
print("  Forma de X:  ", X_lote.shape)
print("  Forma de Z1: ", Z1.shape)
print("  Probabilidades:", np.round(salida, 4))