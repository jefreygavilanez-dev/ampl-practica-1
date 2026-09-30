from fractions import Fraction as F
import json

def fr(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"

class Tab:
    def __init__(self, names, A, b, basis, cost):
        self.names = names; self.A = [[F(v) for v in r] for r in A]; self.b = [F(v) for v in b]
        self.basis = basis[:]; self.cost = [F(v) for v in cost]
    def reduced(self):
        m = len(self.A); n = len(self.names)
        cb = [self.cost[j] for j in self.basis]
        d = [self.cost[j] - sum(cb[i]*self.A[i][j] for i in range(m)) for j in range(n)]
        z = sum(cb[i]*self.b[i] for i in range(m))
        return d, z
    def snapshot(self, title, enter=None, leave=None, ratios=None):
        d, z = self.reduced()
        return dict(title=title, names=self.names, basis=[self.names[j] for j in self.basis],
                    rows=[[fr(v) for v in r]+[fr(bb)] for r, bb in zip(self.A, self.b)],
                    d=[fr(v) for v in d], z=fr(z), enter=enter, leave=leave,
                    ratios=ratios, cb=[fr(self.cost[j]) for j in self.basis], c=[fr(v) for v in self.cost])
    def pivot(self, r, c):
        p = self.A[r][c]
        self.A[r] = [v/p for v in self.A[r]]; self.b[r] /= p
        for i in range(len(self.A)):
            if i != r and self.A[i][c] != 0:
                f = self.A[i][c]
                self.A[i] = [a - f*b for a, b in zip(self.A[i], self.A[r])]
                self.b[i] -= f*self.b[r]
        self.basis[r] = c

def run(tab, allowed, label, log):
    it = 0
    while True:
        d, z = tab.reduced()
        cand = [(d[j], j) for j in allowed if j not in tab.basis and d[j] < 0]
        if not cand:
            log.append(tab.snapshot(f"{label} - Tabla {it} (óptima)"))
            return
        dmin = min(c[0] for c in cand)
        e = min(j for (v, j) in cand if v == dmin)
        ratios = []
        for i in range(len(tab.A)):
            if tab.A[i][e] > 0: ratios.append(tab.b[i]/tab.A[i][e])
            else: ratios.append(None)
        valid = [(q, i) for i, q in enumerate(ratios) if q is not None]
        if not valid:
            log.append(tab.snapshot(f"{label} - Tabla {it} (NO ACOTADO)")); return
        qmin = min(q for q, i in valid)
        r = min(i for q, i in valid if q == qmin)
        log.append(tab.snapshot(f"{label} - Tabla {it}", enter=tab.names[e],
                                leave=tab.names[tab.basis[r]],
                                ratios=[fr(q) if q is not None else "—" for q in ratios])
                   | dict(pivot_row=r, pivot_col=e, pivot=fr(tab.A[r][e])))
        tab.pivot(r, e); it += 1

names = ["x1","x2","x3","x4","s1","s2","s3","a1"]
# R1: -3x1 + x2 - x3 - x4 + s1 = 15 ; R2 (x -1): -4x1 + x2 -4x3 + x4 - s2 + a1 = 2 ; R3: 15x1+3x2+5x3-2x4+s3 = 13
A = [[-3,1,-1,-1,1,0,0,0],[-4,1,-4,1,0,-1,0,1],[15,3,5,-2,0,0,1,0]]
b = [15,2,13]
log = []
# Fase I
t = Tab(names, A, b, [4,7,6], [0,0,0,0,0,0,0,1])
run(t, list(range(8)), "Fase I", log)
phaseI_w = t.reduced()[1]
# Fase II: quitar artificial, restaurar costos
t.cost = [F(v) for v in [1,-2,1,2,0,0,0,0]]
# eliminar columna artificial
t.names = t.names[:7]; t.A = [r[:7] for r in t.A]; t.cost = t.cost[:7]
run(t, list(range(7)), "Fase II", log)
sol = {t.names[j]: t.b[i] for i, j in enumerate(t.basis)}
print("w =", fr(phaseI_w)); print({k: fr(v) for k, v in sol.items()}, "z =", fr(t.reduced()[1]))
print("d final:", dict(zip(t.names,[fr(v) for v in t.reduced()[0]])))
for s in log:
    print("\n", s["title"], "| entra:", s["enter"], "| sale:", s["leave"], "| ratios:", s["ratios"], "| z:", s["z"])
    print("   base:", s["basis"], " d:", s["d"])
    for r in s["rows"]: print("   ", r)
json.dump(log, open("simplex_log.json","w"), ensure_ascii=False, indent=1)
