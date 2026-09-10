# Sesión 02 — Tensor de Color y Análisis Estadístico

Tensores RGB, slicing por canal, conversión a escala de grises e histogramas.

## Taller Analítico 1 — Operaciones con tensores

![Taller analítico 1 resuelto a mano](img/taller01_analitico.png)

### Punto 1

`recorte = imagen[100:200, 300:400, 1]` sobre una imagen de 1920×1080.

El shape resultante es **(100, 100)**. Las dimensiones salen de restar los
límites de cada rango: 200 − 100 = 100 filas y 400 − 300 = 100 columnas. El
tercer índice es fijo y no un rango, así que la dimensión de color desaparece
y queda una matriz 2D.

El recorte contiene las intensidades del canal **verde**, porque OpenCV carga
los canales en orden BGR y el índice 1 cae en la G. Espacialmente es un parche
cuadrado que va de la fila 100 a la 199 y de la columna 300 a la 399.

### Punto 2

¿Por qué aislar un canal con slicing le gana a dos `for` anidados?

**Menos trabajo para el intérprete.** Un ciclo `for` obliga a Python a procesar
la imagen píxel por píxel, millones de operaciones. El slicing manda una sola
instrucción en bloque a código interno en C y resuelve todo en un paso.

**Eficiencia de memoria.** La imagen está guardada como un bloque de memoria
continuo. Al usar slicing no se copian ni se mueven datos: solo se crea una
vista sobre esa misma memoria, por eso la operación es casi instantánea.

**Aprovechamiento de la CPU.** Al leer los datos de forma continua, el slicing
saca todo el potencial de la memoria caché del procesador. Los ciclos `for` la
desperdician porque crean y destruyen variables temporales en cada vuelta.

## Taller de Laboratorio 1 — Transformación de espacios

`lab03_conversion_grises.py`

Un amarillo puro en BGR es `[0, 255, 255]`. Aplicando la fórmula ponderada:

    Y = 0.299(255) + 0.587(255) + 0.114(0) = 225.93

El amarillo arroja un gris **casi blanco (226)**. Tiene sentido: el verde
aporta el 58.7 % de la luminancia percibida y el rojo el 29.9 %, así que
entre los dos suman el 88.6 %. Lo único que le falta al amarillo es el azul,
que apenas pesa un 11.4 %.

Los pesos van en el vector como `[0.114, 0.587, 0.299]` porque OpenCV carga
los canales en orden BGR, no RGB. Si se dejaran en el orden de la fórmula, el
código correría igual pero estaría ponderando el azul como si fuera rojo.

El cálculo del punto 2 se hizo solo con NumPy, como pide el enunciado. OpenCV
aparece únicamente en el punto 4, que pide corroborar contra `cv2.cvtColor()`.
Sobre la fotografía completa la diferencia máxima entre ambos métodos es de
**0.50** en un rango de 0 a 255. No es un error de fórmula sino de redondeo:
`cvtColor` devuelve enteros y la versión manual trabaja en punto flotante.

## Taller de Laboratorio 2 — Analisis estadistico

`lab04_histograma_canales.py`

![Histogramas de los tres canales](img/lab04_histogramas.png)

La imagen es de un atardecer donde se ven los arboles oscuros y el pasto en la
parte de abajo. En este ejercicio mire los tres canales por separado para ver
que tanto aparece cada color en la imagen.

El color dominante es el rojo. Es el unico que se dispara cerca del 250, que
es la parte del cielo donde hay bastante luz. El verde tambien aparece
bastante, pero se concentra en la mitad del grafico, es como una montaña o 
joroba alrededor de 150 que corresponde al pasto y los arboles iluminados. 
El azul por otro lado tiene un pico muy alto en 0, o sea que aporta sobre 
todo a las partes oscuras, y en las zonas claras casi no aparece.

Viendo los tres histogramas juntos se puede entender mejor porque la imagen
tiene unas partes muy oscuras y otras bastante claras. Tambien se puede ver
que hay colores repartidos por casi todo el rango de 0 a 255, lo que hace que
la imagen tenga buen contraste y se puedan diferenciar bien sus diferentes
zonas.