# ============================================================
# agente_linux.py
# Corre en Ubuntu Server / Debian
# Lee logs del sistema y los manda al SIEM en Kali
# ============================================================

import subprocess
import requests
import time

# ── Configuración ──────────────────────────────────────────
IP_SIEM    = "192.168.1.XXX"   # IP de Kali Linux con el SIEM
PUERTO     = 5000
INTERVALO  = 10                # segundos entre cada envío
CANTIDAD   = 20                # cuántos logs leer por ciclo


def leer_logs():
    """
    Lee los últimos logs del sistema con journalctl.
    """
    try:
        resultado = subprocess.run(
            ["journalctl", "-n", str(CANTIDAD), "--no-pager", "-o", "short"],
            capture_output=True,
            text=True
        )
        lineas = []
        for linea in resultado.stdout.split("\n"):
            linea = linea.strip()
            if linea != "" and not linea.startswith("--"):
                lineas.append(linea)
        return lineas

    except Exception as e:
        print(f"[ Agente Linux ] Error leyendo logs: {e}")
        return []


def parsear_linea(linea):
    """
    Convierte una línea de log en diccionario.
    """
    try:
        partes  = linea.split()
        fecha   = partes[0] + " " + partes[1]
        hora    = partes[2]
        mensaje = " ".join(partes[4:]).lower()

        if "error" in mensaje or "failed" in mensaje:
            nivel = "ERROR"
        elif "warn" in mensaje:
            nivel = "WARNING"
        else:
            nivel = "INFO"

        if "session opened" in mensaje:
            accion = "LOGIN_EXITOSO"
        elif "session closed" in mensaje:
            accion = "LOGOUT"
        elif "authentication failure" in mensaje or "failed password" in mensaje:
            accion = "LOGIN_FALLIDO"
        elif "sudo" in mensaje:
            accion = "SUDO"
        elif "error" in mensaje:
            accion = "ERROR_CRITICO"
        else:
            accion = "EVENTO_SISTEMA"

        usuario = "sistema"
        if "user" in mensaje:
            partes_msg = mensaje.split("user")
            if len(partes_msg) > 1:
                usuario = partes_msg[1].strip().split()[0].strip()

        return {
            "fecha":   fecha,
            "hora":    hora,
            "nivel":   nivel,
            "usuario": usuario,
            "ip":      "ubuntu-server",
            "accion":  accion
        }

    except:
        return {
            "fecha":   "desconocida",
            "hora":    "00:00:00",
            "nivel":   "INFO",
            "usuario": "sistema",
            "ip":      "ubuntu-server",
            "accion":  "EVENTO_SISTEMA"
        }


def enviar_al_siem(eventos):
    """
    Manda los eventos al receptor en Kali via HTTP POST.
    """
    try:
        url      = f"http://{IP_SIEM}:{PUERTO}/recibir"
        respuesta = requests.post(url, json={"eventos": eventos}, timeout=5)

        if respuesta.status_code == 200:
            print(f"[ Agente Linux ] {len(eventos)} eventos enviados al SIEM ✅")
        else:
            print(f"[ Agente Linux ] Error al enviar: {respuesta.status_code}")

    except Exception as e:
        print(f"[ Agente Linux ] No se pudo conectar al SIEM: {e}")


def main():
    print("=" * 50)
    print("  🐧 Agente Linux arrancado")
    print(f"  Enviando logs a {IP_SIEM}:{PUERTO}")
    print(f"  Intervalo: {INTERVALO} segundos")
    print("=" * 50)

    while True:
        try:
            lineas  = leer_logs()
            eventos = [parsear_linea(l) for l in lineas]
            enviar_al_siem(eventos)
            time.sleep(INTERVALO)

        except KeyboardInterrupt:
            print("\n🛑 Agente detenido.")
            break


if __name__ == "__main__":
    main()