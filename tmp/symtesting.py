from sympy import *
from math import pi as π

y, θ, ω, Vset, ks, ki, kt, kp = symbols('y θ ω Vset ks ki kt kp')

A = Matrix([
    [0, Vset * ks, 0],
    [0, 0, 1],
    [-ki * kt, (Vset * ks - ki), -kp]
    ])

A = A.subs([(ks, 0.54), (kt, π/2), (Vset, 1), (kp, 5), (ki, 10)])
λ = A.eigenvals()
real_parts = [val.as_real_imag()[0] for val in λ.keys()]

Reig = [None] * 3
for i in range(3): Reig[i] = real_parts[i].evalf()

print(Reig)
