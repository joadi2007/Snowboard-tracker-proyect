import numpy as np 
import matplotlib.pyplot as plt

# --- Parametros ---
FS = 100            # muestras por segundo
G = 9.81            # gravedad en m/s²
UMBRAL = 3.0        # por debajo de esta magnitud se considera caída libre
MIN_VUELO = 0.2     # segundos; tramos más cortos se ignoran

# --- Leer el CSV ---
datos = np.loadtxt('analysis/sesion_simulada.csv', delimiter=',', skiprows=1)
t = datos[:, 0]
ax, ay , az = datos[:, 1], datos[:, 2], datos[:, 3]

magnitud = np.sqrt(ax**2 + ay**2 + az**2)

# --- Detectar caida libre ---
en_vuelo = magnitud < UMBRAL            # arreglo de True/False

cambios = np.diff(en_vuelo.astype(int))
inicios = np.where(cambios == 1)[0] + 1
finales = np.where(cambios == -1)[0] + 1

# --- Reportar cada salto ---

saltos = []
for i_ini, i_fin in zip(inicios, finales):
    duracion = (i_fin - i_ini) / FS
    if duracion < MIN_VUELO:
        continue
    altura = G * duracion**2 / 8
    saltos.append((t[i_ini], t[i_fin], altura))
    print(f"Salto en t={t[i_ini]:.2f} s | aire: {duracion:.2f} s | altura: {altura:.2f} m")

plt.figure(figsize=(12, 4))
plt.plot(t, magnitud, linewidth= 0.8)
plt.axhline(G, color='gray', linestyle='--', label='1 g (9.81)')
plt.axhline(UMBRAL, color="red", linestyle=":", label="Umbral de vuelo")

for t_ini, t_fin, altura in saltos:
    plt.axvspan(t_ini, t_fin, color='orange', alpha=0.3)
    plt.text((t_ini + t_fin) / 2, magnitud.max() * 0.6,
             f"{altura:.1f} m", ha="center")
  

plt.xlabel("Tiempo (s)")
plt.ylabel("Magnitud de aceleración (m/s²)")
plt.title("Saltos detectados")
plt.legend()
plt.show()

