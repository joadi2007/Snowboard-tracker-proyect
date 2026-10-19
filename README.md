# Tracker de sesiones de snowboard

Proyecto personal que une electrónica, programación y snowboard: una placa chica con un sensor de movimiento (acelerómetro + giroscopio) y un módulo GPS que va en la tabla o en el bolsillo y registra la sesión. Después los datos se analizan en la compu para detectar saltos, giros, bajadas y velocidades.

> **Estado:** el análisis en Python ya funciona de punta a punta con **datos simulados**. Los componentes ya están comprados y el hardware se arma en cuanto lleguen; recién ahí se valida todo con datos reales.

## Objetivo

- Medir saltos (tiempo en el aire y altura estimada) y clasificar los giros según el eje (spin, backflip, frontflip, flip lateral, combinado).
- Detectar bajadas y calcular velocidad máxima y velocidad media mientras se baja.
- Guardar los datos y visualizarlos en un dashboard.
- Terminar con una PCB propia, diseñada en KiCad, y una carcasa resistente al frío y la humedad.

## Cómo funciona

```
[MPU6050] --I2C--> [ESP32 + firmware] --USB--> [Python en la compu]
[GPS NEO-6M] -serie->                          guarda, grafica,
                                               detecta saltos y bajadas
```

El ESP32 solo lee los sensores y manda los datos por USB. Todo el análisis lo hace Python en la compu.

## Hardware (etapa 1)

- ESP32 DevKit (WROOM-32)
- Módulo MPU6050 GY-521 (IMU de 6 ejes)
- Módulo GPS NEO-6M con antena
- Protoboard y cables dupont

Conexión del IMU (I2C):

| ESP32 | MPU6050 |
|---|---|
| 3V3 | VCC |
| GND | GND |
| GPIO21 | SDA |
| GPIO22 | SCL |

## Análisis en Python

Todo corre sobre sesiones simuladas, con el mismo formato de CSV que va a generar el sensor real.

| Script | Qué hace |
|---|---|
| `analysis/simular_sesion.py` | Genera una sesión de saltos y giros a 100 Hz (`t, ax, ay, az, gx, gy, gz`). |
| `analysis/detectar_saltos.py` | Detecta los saltos por caída libre, estima altura y tiempo en el aire, mide el giro en cada eje y clasifica la maniobra. Avisa si el giroscopio pudo saturarse. |
| `analysis/simular_gps.py` | Genera una sesión GPS a 1 Hz (`t, velocidad, altitud`) con subidas, bajadas y paradas. |
| `analysis/detectar_gps.py` | Separa subida, bajada y parada usando la velocidad vertical, y calcula velocidad máxima y media en bajada. |

Para correrlo (con Python, `numpy` y `matplotlib` instalados), desde la raíz del repo:

```bash
python analysis/simular_sesion.py
python analysis/detectar_saltos.py
python analysis/simular_gps.py
python analysis/detectar_gps.py
```

### Decisiones de diseño

- **Salto:** se detecta cuando la magnitud de la aceleración cae cerca de cero (caída libre). La altura se estima como `g·T²/8`, asumiendo que se aterriza al mismo nivel del despegue, así que es una aproximación.
- **Giros:** se integra la velocidad angular de cada eje durante el vuelo. Se usa una convención provisoria de ejes (x a lo largo de la tabla, y de canto a canto, z vertical) que hay que verificar con el sensor real.
- **Rangos del sensor:** ±2000 °/s para el giroscopio y ±16 g para el acelerómetro, porque los rangos por defecto se saturan con giros rápidos.
- **Velocidad media:** se calcula solo mientras se baja. Promediar toda la sesión mete la aerosilla y las paradas y el número no representa la bajada.

## Etapas

- [ ] 1. Leer el sensor con el ESP32 y ver los datos en tiempo real
- [ ] 2. Guardar los datos (microSD o por WiFi/Bluetooth)
- [x] 3. Analizar en Python: saltos, giros, bajadas y velocidad (hecho con datos simulados, falta validar con datos reales)
- [ ] 4. Visualizar los resultados en un dashboard
- [ ] 5. Diseñar la PCB y la carcasa
- [ ] 6. Probar en la nieve y calibrar

## Estructura del repo

```
tracker-snowboard/
├── firmware/    código del ESP32
├── analysis/    scripts de Python para simular y analizar los datos
├── hardware/    proyecto de KiCad (esquemático y PCB)
└── docs/        resumen del proyecto y lista de compras
```

## Tecnologías

C++ (Arduino IDE o PlatformIO) para el firmware, Python (`numpy`, `matplotlib`) para el análisis y KiCad para el diseño electrónico.

## Autor

Joaco ([@joadi2007](https://github.com/joadi2007)), estudiante de electrónica e informática.

## Licencia

MIT. Ver el archivo `LICENSE`.