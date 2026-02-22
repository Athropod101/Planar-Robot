from sympy import *

R, L, J, μ, k, t = symbols('R L J μ k t') # Declares them as symbolic variables.

A = Matrix([
    [-R/L, -k/L],
    [ k/J, -μ/J],
    ])

B = Matrix([1/L, 0])

X = ( (A * t).exp() - eye(2)) * A.inv() * B

# Finding Eigenvalues
λ = A.eigenvals()

for key, val in λ.items():
    pprint(key)

'''
# Substituting
Μ = 0.0065
j = 0.2000
K = 0.2604
r = 0.9470
l = 0.0020

X_subbed =(X.subs([
    (R, r),
    (k, K),
    (L, l),
    (J, j),
    (μ, Μ),
    ]))
#pprint(X_subbed[1])


λ_subbed = (A.subs([
    (R, r),
    (k, K),
    (L, l),
    (J, j),
    (μ, Μ),
    ])).eigenvals()

for key, val in λ_subbed.items():
    #print(f"{key:.4f}")
    pprint(key)
'''
