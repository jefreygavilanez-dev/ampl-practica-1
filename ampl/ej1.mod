# ==========================================================================
# Práctica APE N.º 1 - Investigación de Operaciones
# Ejercicio 1: problema de minimización (método símplex de dos fases)
# Archivo: ej1.mod  (MODELO: estructura algebraica, sin datos numéricos)
# ==========================================================================

set VARS;                        # índices de las variables de decisión (1..4)
set REST;                        # índices de las restricciones (1..3)

param c {VARS};                  # coeficientes de la función objetivo
param a {REST, VARS};            # matriz de coeficientes de las restricciones
param b {REST};                  # términos independientes

var x {VARS} >= 0;               # x1, ..., x4 >= 0

# Función objetivo: minimizar z = c1*x1 + ... + c4*x4
minimize Coste: sum {j in VARS} c[j] * x[j];

# Restricciones de tipo "<=": sum_j a[i,j]*x[j] <= b[i]
subject to Restr {i in REST}:
    sum {j in VARS} a[i,j] * x[j] <= b[i];
