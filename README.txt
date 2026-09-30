PRÁCTICA APE N.º 1 - INVESTIGACIÓN DE OPERACIONES
Programación lineal: método símplex (dos fases), modelado en AMPL y análisis de sensibilidad

ampl/
  ej1.mod  ej1.dat  ej1.run   -> Ejercicio 1 (minimización, 4 variables, 3 restricciones "<=")
  ej2.mod  ej2.dat  ej2.run   -> Ejercicio 2 (producción: n productos en m plantas + sensibilidad)
verificacion/
  simplex_exacto_ej1.py         -> símplex de dos fases con fracciones exactas (genera las tablas del informe)
  sensibilidad_exacta_ej2.py    -> base óptima, precios sombra y rangos de validez (aritmética exacta)
  leer_dat_y_resolver.py        -> lee los .dat y resuelve con HiGHS (comprobación cruzada)

Ejecución en AMPL (Community Edition):
  ampl: include ej1.run;
  ampl: include ej2.run;      (requiere un solver con sensibilidad, p. ej. CPLEX; ver comentarios del .run)
Ejecución de la verificación en Python 3:  pip install scipy sympy ;  python verificacion/<archivo>.py
