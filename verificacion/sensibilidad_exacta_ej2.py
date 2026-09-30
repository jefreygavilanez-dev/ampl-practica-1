import sympy as sp
from sympy import Rational as R, Matrix
P=[1,2,3]; L=[1,2]
c={(1,1):3,(2,1):6,(3,1):2,(1,2):4,(2,2):5,(3,2):3}
t={(1,1):4,(2,1):4,(3,1):3,(1,2):6,(2,2):5,(3,2):2}
T={1:767,2:650}; d={1:55,2:25,3:200}
V=[(1,1),(2,1),(3,1),(1,2),(2,2),(3,2)]
names=["x%d%d"%v for v in V]+["h1","h2","e1","e2","e3"]   # h: holgura capacidad, e: exceso demanda
cost=[c[v] for v in V]+[0]*5
# filas: cap1, cap2, dem1, dem2, dem3
A=sp.zeros(5,11)
for k,(i,j) in enumerate(V):
    A[j-1,k]=t[(i,j)]; A[2+i-1,k]=1
A[0,6]=1; A[1,7]=1; A[2,8]=-1; A[3,9]=-1; A[4,10]=-1
b=Matrix([T[1],T[2],d[1],d[2],d[3]])
basis=[names.index(n) for n in ["x11","x12","x22","x31","h2"]]
B=A[:,basis]; Binv=B.inv()
xB=Binv*b
print("xB",dict(zip([names[k] for k in basis],xB)))
cB=Matrix([cost[k] for k in basis]).T
y=cB*Binv     # duales (∂z/∂b)
print("duals y (cap1,cap2,dem1,dem2,dem3):",list(y))
z=(cB*xB)[0]; print("z=",z, float(z))
dred={names[j]:cost[j]-(y*A[:,j])[0] for j in range(11)}
print("reduced costs:",dred)
# RHS ranging
print("\nRHS ranging (b_k, min, max):")
for k,lab in enumerate(["Cap1(T1)","Cap2(T2)","Dem1(d1)","Dem2(d2)","Dem3(d3)"]):
    col=Binv[:,k]
    lo=-sp.oo; hi=sp.oo
    for r in range(5):
        if col[r]>0: lo=max(lo,-xB[r]/col[r])
        elif col[r]<0: hi=min(hi,-xB[r]/col[r])
    print(lab, b[k], b[k]+lo, b[k]+hi)
# cost ranging
print("\nCost ranging:")
nonb=[j for j in range(11) if j not in basis]
for j in range(6):
    if j in basis:
        r=basis.index(j)
        # d_n(delta)=dred_n - delta*(Binv A_n)[r]
        lo=-sp.oo; hi=sp.oo
        for n in nonb:
            a=(Binv*A[:,n])[r]
            if a>0: hi=min(hi,dred[names[n]]/a)
            elif a<0: lo=max(lo,dred[names[n]]/a)
        print(names[j],"cost",cost[j],"range",cost[j]+lo,cost[j]+hi)
    else:
        print(names[j],"cost",cost[j],"nonbasic: down=",cost[j]-dred[names[j]],"up=inf")
