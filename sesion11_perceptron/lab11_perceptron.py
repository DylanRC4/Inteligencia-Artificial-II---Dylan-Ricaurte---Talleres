import numpy as np


# 1. Definir la Funcion de Activacion (Escalon)
def funcion_escalon(z):
    if z >= 0:
        return 1
    else:
        return 0


# 2. Definir la Estructura de la Neurona
def perceptron(X, W, b):
    # Producto punto (Combinacion lineal)
    Z = np.dot(X, W) + b

    # Activacion
    salida = funcion_escalon(Z)
    return salida


# 3. Evaluar la neurona en las cuatro combinaciones de dos entradas binarias
def probar_compuerta(nombre, pesos, sesgo):
    print(f"Compuerta {nombre}  (pesos = {pesos}, sesgo = {sesgo})")
    for entradas in [[0, 0], [0, 1], [1, 0], [1, 1]]:
        resultado = perceptron(np.array(entradas), pesos, sesgo)
        print(f"  {entradas} -> {resultado}")
    print()


# 4. Compuerta AND: solo dispara si ambas entradas son 1
probar_compuerta("AND", np.array([0.5, 0.5]), -0.8)

# 5. Compuerta OR: basta con que una entrada sea 1
# Mismos pesos que el AND, solo cambia el sesgo
probar_compuerta("OR", np.array([0.5, 0.5]), -0.2)