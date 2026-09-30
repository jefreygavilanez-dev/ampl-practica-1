# ==========================================================================
# Práctica APE N.º 1 - Investigación de Operaciones
# Ejercicio 2: planificación de la producción (n productos, m plantas)
# Archivo: ej2.mod  (MODELO GENERAL: conjuntos y parámetros, sin números)
# ==========================================================================

set PRODUCTOS;                             # i = 1..n
set PLANTAS;                               # j = 1..m

param c {PRODUCTOS, PLANTAS} >= 0;         # coste unitario de fabricar i en j (USD/u)
param t {PRODUCTOS, PLANTAS} >= 0;         # horas para fabricar una unidad de i en j (h/u)
param T {PLANTAS} >= 0;                    # horas de trabajo disponibles en la planta j
param d {PRODUCTOS} >= 0;                  # demanda del producto i (u)

var x {PRODUCTOS, PLANTAS} >= 0;           # cantidad del producto i fabricada en j

# Minimizar el coste total de fabricación
minimize CosteTotal:
    sum {i in PRODUCTOS, j in PLANTAS} c[i,j] * x[i,j];

# Capacidad de cada planta
subject to Capacidad {j in PLANTAS}:
    sum {i in PRODUCTOS} t[i,j] * x[i,j] <= T[j];

# Satisfacer la demanda de cada producto
subject to Demanda {i in PRODUCTOS}:
    sum {j in PLANTAS} x[i,j] >= d[i];
