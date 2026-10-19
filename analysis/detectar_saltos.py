import numpy as np 
import matplotlib.pyplot as plt

# --- Parametros ---
FS = 100               # muestras por segundo
G = 9.81               # gravedad en m/s²
UMBRAL = 3.0           # por debajo de esta magnitud se considera caída libre
MIN_VUELO = 0.2        # segundos; tramos más cortos se ignoran
LIMITE_GIRO = 2000     # °/s, rango configurado en el sensor
MIN_SECUNDARIO = 90    # grados minimos en el segundo eje 
RATIO_SECUNDARIO = 0.3 # fraccion minima respecto del giro principal

# --- Leer el CSV ---
datos = np.loadtxt('analysis/sesion_simulada.csv', delimiter=',', skiprows=1)
t = datos[:, 0]
ax, ay , az = datos[:, 1], datos[:, 2], datos[:, 3]
gx, gy, gz = datos[:, 4], datos[:, 5], datos[:, 6]

magnitud = np.sqrt(ax**2 + ay**2 + az**2)

# --- Detectar caida libre ---
en_vuelo = magnitud < UMBRAL            # arreglo de True/False

cambios = np.diff(en_vuelo.astype(int))
inicios = np.where(cambios == 1)[0] + 1
finales = np.where(cambios == -1)[0] + 1

# --- Reportar cada salto ---

saltos = []     # guarda los saltos detectados

for i_ini, i_fin in zip(inicios, finales):
    duracion = (i_fin - i_ini) / FS
    if duracion < MIN_VUELO:
        continue
    altura = G * duracion**2 / 8

    # Giro aacumulado en cada eje durante el vuelo
    giros= {
        'x': np.sum(gx[i_ini:i_fin]) / FS,
        'y': np.sum(gy[i_ini:i_fin]) / FS,
        'z': np.sum(gz[i_ini:i_fin]) / FS
    }
    eje = max(giros, key=lambda k: abs(giros[k]))   # eje dominante
    giro = giros[eje]
    giro_redondeado = round(abs(giro) / 180) * 180

    # Clasificar la maniobra
    if giro_redondeado == 0:
        tipo = 'sin giro'
    elif eje == 'z':
        tipo ='spin'
    elif eje == 'y':
        tipo = 'backflip' if giro > 0 else "frontflip"
    else:
        tipo = 'flip lateral'

    # Si otro eje tambien giro bastante, es una maniobra combinada
    secundario = max(abs(v) for k, v in giros.items() if k != eje)
    if secundario >= MIN_SECUNDARIO and secundario >= RATIO_SECUNDARIO * abs(giro):
        tipo += " (combinado)"

    # Aviso de saturacion
    saturado = max(np.max(np.abs(g[i_ini:i_fin])) for g in (gx, gy, gz)) >= LIMITE_GIRO * 0.98
    aviso = "  ⚠ giro posiblemente saturado" if saturado else ""
    saltos.append((t[i_ini], t[i_fin], altura, giro, tipo))    
    print(f"Salto en t={t[i_ini]:.2f} s | aire: {duracion:.2f} s | altura: {altura:.2f} m | {tipo} {giro_redondeado}° (medido {giro:.0f}°){aviso}")

plt.figure(figsize=(12, 4))
plt.plot(t, magnitud, linewidth= 0.8)
plt.axhline(G, color='gray', linestyle='--', label='1 g (9.81)')
plt.axhline(UMBRAL, color="red", linestyle=":", label="Umbral de vuelo")

for i, (t_ini, t_fin, altura, giro, tipo) in enumerate(saltos):
    plt.axvspan(t_ini, t_fin, color="orange", alpha=0.3)
    y = magnitud.max() * (0.7 if i % 2 == 0 else 0.45)
    plt.text((t_ini + t_fin) / 2, y,
             f"{altura:.1f} m\n{tipo}\n{abs(giro):.0f}°",
             ha="center", fontsize=8)
    
plt.xlabel("Tiempo (s)")
plt.ylabel("Magnitud de aceleración (m/s²)")
plt.title("Saltos detectados")
plt.legend()
plt.show()

