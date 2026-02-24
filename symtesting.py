from sympy import *

α, β, kp, ki, kd, s = symbols('α β kp ki kd s')
Vset = Function('Vset')(s)
ΔV = Function('ΔV')(s)
Θe = Function('Θe')(s)
Θs = Function('Θs')(s)
Θ = Function('Θ')(s)
Ωset = Function('Ωset')(s)
Ω = Function('Ω')(s)




Eq1 = Eq(Θe, Θs - Θ)
Eq2 = Eq(ΔV, Θe * (kp + ki/s + kd*s))
Eq3 = Eq(Ω, β * (α * (ΔV + Vset) - Ωset))
Eq4 = Eq(Θ, Ω / s)

SOL = solve([Eq1, Eq2, Eq3, Eq4], [Θe, Θ, ΔV, Ω])

Θe = SOL[Θe]

SSError = limit(s * Θe, s, 0)

pprint(simplify(SSError))

print("================================================================")

pprint(simplify(together(SOL[Θ])))



print("================================================================")
vset, ωset = symbols('vset ωset')
Unit = SOL[Θ].subs([(Θs, 1/s), (Ωset, ωset/s), (Vset, vset/s)])
pprint(simplify(Unit))

UnitDenomEq = Eq(denom(together(Unit)), 0)
UnitPoles = solve([UnitDenomEq], [s])
print("POLES:")
pprint(UnitPoles)
