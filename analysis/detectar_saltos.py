import numpy as np 

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
for i_ini, i_fin in zip(inicios, finales):
    duracion = (i_fin - i_ini) / FS
    if duracion < MIN_VUELO:
        continue
    altura = G * duracion**2 / 8
    print(f"Salto en t={t[i_ini]:.2f} s | aire: {duracion:.2f} s | altura: {altura:.2f} m")