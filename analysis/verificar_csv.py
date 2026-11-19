import numpy as np

datos = np.loadtxt("analysis/sesion_serial.csv", delimiter=",", skiprows=1)
t = datos[:, 0]
dt = np.diff(t)

print("Filas:", len(t))
print("t inicial:", t[0], "| t final:", t[-1], "| duración:", round(t[-1] - t[0], 2), "s")
print("Paso mínimo:", dt.min(), "| paso máximo:", dt.max())
print("Pasos de ~0.010 s:", np.sum(np.isclose(dt, 0.01, atol=0.0015)))
print("Pasos repetidos o hacia atrás:", np.sum(dt <= 0))