# Tracker de sesiones de snowboard

Proyecto personal que une electrónica, programación y snowboard: una placa chica con un sensor de movimiento (acelerómetro + giroscopio) que va en la tabla o en el bolsillo y registra cómo me muevo. Después los datos se analizan en la compu para detectar saltos, giros y curvas.

> **Estado:** en preparación. Todavía no hay hardware armado; el proyecto arranca en cuanto lleguen los componentes.

## Objetivo

- Medir saltos (tiempo en el aire y altura estimada), giros y curvas durante una sesión.
- Guardar los datos y visualizarlos en un dashboard.
- Terminar con una PCB propia, diseñada en KiCad, y una carcasa resistente al frío y la humedad.

## Cómo funciona

```
[MPU6050] --I2C--> [ESP32 + firmware] --USB--> [Python en la compu]
  mide                lee y envía               guarda, grafica,
                                                detecta saltos
```

El ESP32 solo lee el sensor y manda los datos por USB. Todo el análisis lo hace Python en la compu.

## Hardware (etapa 1)

- ESP32 DevKit (38 pines, USB-C)
- Módulo MPU6050 GY-521 (IMU de 6 ejes)
- Protoboard y cables dupont

Conexiones (I2C):

| ESP32 | MPU6050 |
|---|---|
| 3V3 | VCC |
| GND | GND |
| GPIO21 | SDA |
| GPIO22 | SCL |

## Etapas

- [ ] 1. Leer el sensor con el ESP32 y ver los datos en tiempo real
- [ ] 2. Guardar los datos (microSD o por WiFi/Bluetooth)
- [ ] 3. Analizar en Python: filtrar ruido y detectar saltos y giros
- [ ] 4. Visualizar los resultados en un dashboard
- [ ] 5. Diseñar la PCB y la carcasa
- [ ] 6. Probar en la nieve y calibrar

## Estructura del repo

```
tracker-snowboard/
├── firmware/    código del ESP32
├── analysis/    scripts de Python para analizar los datos
├── hardware/    proyecto de KiCad (esquemático y PCB)
└── docs/        resumen del proyecto y lista de compras
```

## Tecnologías

C++ (Arduino IDE o PlatformIO) para el firmware, Python (`pyserial`, `matplotlib`) para el análisis y KiCad para el diseño electrónico.

## Autor

Joaco ([@joadi2007](https://github.com/joadi2007)), estudiante de electrónica e informática.

## Licencia

MIT. Ver el archivo `LICENSE`.
