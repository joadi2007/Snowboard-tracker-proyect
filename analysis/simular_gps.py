import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(7)

# --- Sesión: (tipo de tramo, duración en segundos) ---
tramos =[('parada', 60), ('subida', 300), ('bajada', 240),
        ('subida', 300), ('bajada', 200), ('parada', 120),
        ('subida', 300), ('bajada', 260)]

velocidad = []      # km/h, una muestra por segundo
tipos = []          # etiqueta real de cada muestra (para verificar después)
altitud = []        # metros, una muestra por segundo
alt_actual = 1700   # altitud de la base al empezar

for tipo, dur in tramos:
    tl = np.arange(dur)
    if tipo == 'parada':
        v = np.abs(rng.normal(0, 0.5, dur))
    elif tipo == 'subida':
        v = rng.normal(11, 0.7, dur)
    else:   # bajada
        fase = rng.uniform(0, 2 * np.pi)
        v = 35 + 20 * np.sin(2 * np.pi * tl / 45 + fase) + rng.normal(0, 2, dur)
        v = np.clip(v, 0, None)
    velocidad.extend(v)
    tipos.extend([tipo] * dur)

    # Altitud: sube en la aerosilla, baja en la bajada, constante en la parada
    delta = {"parada": 0, "subida": 300, "bajada": -300}[tipo]
    a = alt_actual + delta * tl / dur + rng.normal(0, 2, dur)
    altitud.extend(a)
    alt_actual += delta

velocidad = np.array(velocidad)
t = np.arange(len(velocidad))

velocidad = np.array(velocidad)
altitud = np.array(altitud)
t = np.arange(len(velocidad))

# --- Guardar en CSV ---
datos = np.column_stack((t, velocidad, altitud))
np.savetxt("analysis/sesion_gps_simulada.csv", datos,
           delimiter=",", header="t,velocidad,altitud", comments="", fmt="%.2f")

# --- Gráfico ---
fig, (eje1, eje2) = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
eje1.plot(t / 60, velocidad, linewidth=0.8)
eje1.set_ylabel("Velocidad (km/h)")
eje1.set_title("Sesión GPS simulada")
eje2.plot(t / 60, altitud, linewidth=0.8, color="green")
eje2.set_ylabel("Altitud (m)")
eje2.set_xlabel("Tiempo (min)")
plt.show()