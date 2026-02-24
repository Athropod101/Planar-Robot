from sympy import *

Vcap, θdot, Vdot, θ, V, γ, ki, kp, kd, u, θs = symbols('Vcap θdot Vdot θ V γ ki kp kd u θs')

A = Matrix([
    [  0,  γ  ,],
    [-ki, -γ*kp,],
    ])

B = Matrix([
    [0 ,   1],
    [ki, -kp],
    ])

X = Matrix([
    [θ],
    [V],
    ])


Xdot = Matrix([
    [θdot],
    [Vdot],
    ])

U = Matrix([
    [θs],
    [u],
    ])

Xo = Matrix([
    [0],
    [-Vcap],
    ])

sse = -A.inv() * B * U

pprint(sse)
print("\n")
pprint(A.eigenvals())
