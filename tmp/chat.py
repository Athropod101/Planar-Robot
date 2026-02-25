import numpy as np
import matplotlib.pyplot as plt
import math as m

# Stable 2nd-order system
A = np.array([[0, 1],
              [-1, -1]])
B = np.array([[0],
              [-m.pi]])

# Ramp input
m = 1.0
b = 1.0

# Time vector
t_vals = np.linspace(0, 10, 1000)
dt = t_vals[1] - t_vals[0]

# Initial condition
x = np.array([[0.0],
              [0.0]])

x1_vals = []

# Simple Euler integration (rough visualization)
for t in t_vals:
    u = m*t + b
    x_dot = A @ x + B * u
    x = x + x_dot * dt
    x1_vals.append(x[0,0])

plt.plot(t_vals, x1_vals)
plt.xlabel("Time (t)")
plt.ylabel("x1(t)")
plt.title("x1(t) for Stable 2nd-Order System with Ramp Input")
plt.grid(True)
plt.show()
