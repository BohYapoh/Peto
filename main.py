import math
import matplotlib.pyplot as plt
import tkinter
import numpy as np
print("Hello world")

v_0 = 0
y_0 = 100
g = 9.81
C = 0.0022
dt = 0.01

t = np.linspace(0, 5, 501)
y = np.zeros((len(t)))
v = np.zeros((len(t)))
a = np.zeros((len(t)))
y[1]=1

def f(t, v):
    return -g-C*v*abs(v)

for i in range(len(t) - 1):
    k_1 = f(t[i], v[i])
    k_2 = f(t[i] + dt/2, v[i] + k_1 * dt/2)
    k_3 = f(t[i] + dt/2, v[i] + k_2 * dt/2)
    k_4 = f(t[i] + dt, v[i] + k_3 * dt)
    v [i+1] = v[i] + (dt/6) * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
    print(v[i])

print(v[1])
