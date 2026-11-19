import serial
import time

PUERTO = "/dev/cu.usbserial-0001"
BAUDIOS = 115200
DURACION = 10                      # segundos a grabar
ARCHIVO = "analysis/sesion_serial.csv"
COLUMNAS = 7                       # t, ax, ay, az, gx, gy, gz

validas = 0
descartadas = 0

with serial.Serial(PUERTO, BAUDIOS, timeout=1) as ser, open(ARCHIVO, "w") as f:
    f.write("t,ax,ay,az,gx,gy,gz\n")
    time.sleep(2)                  # dejar que el puerto se estabilice
    ser.reset_input_buffer()       # tirar lo acumulado
    ser.readline()                 # descartar una línea que puede venir cortada

    inicio = time.time()
    t0 = None
    while time.time() - inicio < DURACION + 5:     # tope de seguridad
        linea = ser.readline().decode("utf-8", errors="ignore").strip()
        partes = linea.split(",")

        if len(partes) != COLUMNAS:
            descartadas += 1
            continue
        try:
            valores = [float(p) for p in partes]
        except ValueError:
            descartadas += 1
            continue

        if t0 is None:
            t0 = valores[0]                        # tiempo de la primera muestra
        if valores[0] - t0 >= DURACION:
            break                                  # ya grabamos DURACION segundos de la placa

        partes[0] = f"{valores[0] - t0:.3f}"
        linea = ",".join(partes)

        f.write(linea + "\n")
        validas += 1

print(f"Líneas válidas: {validas} | descartadas: {descartadas}")