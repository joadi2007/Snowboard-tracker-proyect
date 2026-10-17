import numpy as np
import matplotlib.pyplot as plt

# --- Parametros de la simulacion ---

FS = 100             # muestras por segundo (Hz)
DURACION = 60        # duración de la sesión en segundos
G = 9.81             # gravedad en m/s²
LIMITE_GIRO = 2000   # °/s, rango por defecto del giroscopio del MPU6050

rng = np.random.default_rng(42)         # generador de numeros aleatorios

# --- Eje de tiempo --- 
n = FS * DURACION               # cantidad total de muestras 
t =  np.arange(n) / FS          # 0, 0.01, 0.02, ..., 59.99

# --- Señal base: andando normal, sin saltos ---
ax = rng.normal(0, 0.3, n)        # ruido alrededor de 0
ay = rng.normal(0, 0.3, n)
az = G + rng.normal(0, 0.3, n)    # la gravedad se mide en el eje z

# --- Giroscopio (grados por segundo): casi quieto, con ruido ---
gx = rng.normal(0, 2, n)
gy = rng.normal(0,2, n)
gz = rng.normal(0, 2, n)

# --- Saltos: (instante de despegue en s, tiempo en el aire en s) ---
saltos = [(10.0, 1.3, 180), (25.0, 1.6, 360), (42.0, 2.0, 540),
          (50.0, 1.1, 360), (55.0, 0.8, 360)] 
for t_despegue, t_vuelo, giro in saltos:
    i_ini = int(t_despegue * FS)        # muestra del despegue
    i_fin = i_ini + int(t_vuelo * FS)   # muestra el aterrizaje 
    pico = int(0.1 * FS)                # 0.1 s de pico = 10 muestras

    # Despegue: la tabla empuja hacia arriba (~2 g)
    az[i_ini - pico:i_ini] = 2 * G + rng.normal(0, 0.3, pico)

    # Vuelo: caída libre, el sensor mide casi 0 en los tres ejes
    n_vuelo = i_fin - i_ini
    ax[i_ini:i_fin] = rng.normal(0, 0.2, n_vuelo)
    ay[i_ini:i_fin] = rng.normal(0, 0.2, n_vuelo)
    az[i_ini:i_fin] = rng.normal(0, 0.2, n_vuelo)

    # Giro en el aire: velocidad angular constante en el eje z
    velocidad_giro = giro / t_vuelo             # grados por segundo
    gz[i_ini:i_fin] = velocidad_giro + rng.normal(0, 2, n_vuelo)

    # Aterrizaje: impacto fuerte (~3 g)
    az[i_fin:i_fin + pico] = 5 * G + rng.normal(0, 0.3, pico)
    

# --- Magnitud total de la aceleración ---
magnitud = np.sqrt(ax**2 + ay**2 + az**2)

# --- Saturación: el giroscopio no puede medir más allá de su rango ---
gx = np.clip(gx, -LIMITE_GIRO, LIMITE_GIRO)
gy = np.clip(gy, -LIMITE_GIRO, LIMITE_GIRO)
gz = np.clip(gz, -LIMITE_GIRO, LIMITE_GIRO)

# --- Guardar en CSV ---
datos = np.column_stack((t,ax,ay,az,gx,gy,gz))
np.savetxt('analysis/sesion_simulada.csv', datos,
           delimiter=',', header="t,ax,ay,az,gx,gy,gz", comments='', fmt='%.4f')

# --- Gráfico ---
plt.figure(figsize=(12, 4))
plt.plot(t, magnitud, linewidth=0.8)
plt.axhline(G, color='gray', linestyle='--', label='1 g (9.81)')
plt.xlabel('Tiempo (s)')
plt.ylabel('Magnitud de aceleracion (m/s²)')
plt.title('Sesion simulada')
plt.legend()
plt.show()
