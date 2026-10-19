import numpy as np
import matplotlib.pyplot as plt

# --- Parámetros ---
VENTANA = 15       # segundos de suavizado de la altitud (número impar)
UMBRAL_VZ = 0.3    # m/s; por encima sube, por debajo baja
MIN_BAJADA = 30    # segundos; tramos más cortos se ignoran

# --- Leer el CSV ---
datos = np.loadtxt('analysis/sesion_gps_simulada.csv', delimiter=',', skiprows=1)
t = datos[:, 1]
velocidad = datos[:, 1]
altitud = datos[:, 2]

# --- Suavizar la altitud (promedio móvil) ---
pad = VENTANA // 2
alt_pad = np.pad(altitud, pad, mode='edge')
alt_suave = np.convolve(alt_pad, np.ones(VENTANA) / VENTANA, mode='valid')

# --- Velocidad vertical (m/s) ---
vz = np.gradient(alt_suave)

# --- Clasificar cada segundo ---
estado = np.where(vz > UMBRAL_VZ, 'subida',
         np.where(vz < -UMBRAL_VZ, 'bajada', 'parada'))

for nombre in ('subida', 'bajada', 'parada'):
    print(nombre, np.sum(estado == nombre), 's')

# --- Bajadas: tramos continuos con estado "bajada" ---
en_bajada = np.concatenate(([False], estado == "bajada", [False]))
cambios = np.diff(en_bajada.astype(int))
inicios = np.where(cambios == 1)[0]
finales = np.where(cambios == -1)[0]

n_bajada = 0
for i_ini, i_fin in zip(inicios, finales):
    dur = i_fin - i_ini
    if dur < MIN_BAJADA:
        continue
    n_bajada += 1
    v = velocidad[i_ini:i_fin]
    desnivel = alt_suave[i_ini] - alt_suave[i_fin - 1]
    print(f"Bajada {n_bajada}: {dur / 60:.1f} min | desnivel: {desnivel:.0f} m | "
          f"vel. máx: {v.max():.1f} km/h | vel. media: {v.mean():.1f} km/h")

# --- Resumen de la sesión ---
mascara = estado == "bajada"
print(f"Velocidad máxima: {velocidad.max():.1f} km/h")
print(f"Velocidad media en bajada: {velocidad[mascara].mean():.1f} km/h")
print(f"Velocidad media de toda la sesión: {velocidad.mean():.1f} km/h")