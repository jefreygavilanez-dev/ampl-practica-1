"""Verificación cruzada: lee ej1.dat / ej2.dat (formato AMPL simple) y resuelve con HiGHS (SciPy)."""
import re, sys, os
import numpy as np
from scipy.optimize import linprog

def limpiar(txt):
    return re.sub(r'#.*', '', txt)

def bloques(txt):
    """Devuelve dict nombre -> lista de tokens del bloque 'param|set nombre ... ;'."""
    out = {}
    for m in re.finditer(r'(param|set)\s+(\w+)\s*(:(?!=))?(.*?);', limpiar(txt), flags=re.S):
        out[m.group(2)] = (m.group(3) is not None, m.group(4).split())
    return out

def vector(tokens):
    d = {}
    for k in range(0, len(tokens), 2):
        d[int(tokens[k])] = float(tokens[k + 1])
    return d

def tabla(tokens):
    i = tokens.index(':=')
    cols = [int(v) for v in tokens[:i]]
    resto = tokens[i + 1:]
    M = {}
    for r in range(0, len(resto), len(cols) + 1):
        fila = int(resto[r])
        for cidx, col in enumerate(cols):
            M[(fila, col)] = float(resto[r + 1 + cidx])
    return M

base = os.path.dirname(os.path.abspath(__file__)) + '/../ampl/'
# ---------- Ejercicio 1 ----------
b1 = bloques(open(base + 'ej1.dat', encoding='utf8').read())
c = vector([t for t in b1['c'][1] if t != ':='])
A = tabla(b1['a'][1]); b = vector([t for t in b1['b'][1] if t != ':='])
n, m = len(c), len(b)
res = linprog([c[j] for j in range(1, n + 1)],
              A_ub=[[A[(i, j)] for j in range(1, n + 1)] for i in range(1, m + 1)],
              b_ub=[b[i] for i in range(1, m + 1)], bounds=[(0, None)] * n, method='highs')
print('Ej1  x* =', np.round(res.x, 6), ' z* =', round(res.fun, 6), ' rc =', np.round(res.lower.marginals, 6))

# ---------- Ejercicio 2 ----------
b2 = bloques(open(base + 'ej2.dat', encoding='utf8').read())
C = tabla(b2['c'][1]); Tt = tabla(b2['t'][1])
Tj = vector([t for t in b2['T'][1] if t != ':=']); di = vector([t for t in b2['d'][1] if t != ':='])
P = [1, 2, 3]; L = [1, 2]; V = [(i, j) for i in P for j in L]
cost = [C[v] for v in V]
Aub = [[Tt[(i, jj)] if jj == j else 0 for (i, jj) in V] for j in L] + \
      [[-1 if ii == i else 0 for (ii, jj) in V] for i in P]
bub = [Tj[j] for j in L] + [-di[i] for i in P]
r2 = linprog(cost, A_ub=Aub, b_ub=bub, bounds=[(0, None)] * 6, method='highs')
print('Ej2  z* =', round(r2.fun, 6))
for v, xv, rc in zip(V, r2.x, r2.lower.marginals):
    print(f'   x{v[0]}{v[1]} = {xv:9.4f}   rc = {rc:.4f}')
print('   precios sombra (Capacidad1, Capacidad2, Demanda1..3) =',
      np.round([r2.ineqlin.marginals[0], r2.ineqlin.marginals[1],
                -r2.ineqlin.marginals[2], -r2.ineqlin.marginals[3], -r2.ineqlin.marginals[4]], 6))
print('   holguras de capacidad =', np.round(r2.slack[:2], 4))
