# ============================================================
# agente_windows.py
# Corre en Windows Server
# ============================================================

import subprocess
import requests
import time

# ── Configuración ──────────────────────────────────────────
IP_SIEM   = "192.168.3.163"   # IP de Kali Linux con el SIEM
PUERTO    = 5001
INTERVALO = 10                # segundos entre cada envío
CANTIDAD  = 20                # cuántos logs leer por ciclo


def leer_logs_windows():
    try:
        comando = f"""
        Get-EventLog -LogName Security -Newest {CANTIDAD} |
        Select-Object TimeGenerated, EntryType, Message |
        ConvertTo-Csv -NoTypeInformation
        """
        resultado = subprocess.run(
            ["powershell", "-Command", comando],
            capture_output=True,
            text=True
        )
        lineas = resultado.stdout.strip().split("\n")
        return lineas[1:] if len(lineas) > 1 else []

    except Exception as e:
        print(f"[ Agente Windows ] Error leyendo logs: {e}")
        return []


def parsear_linea_windows(linea):
    try:
        partes  = linea.replace('"', '').split(",")
        fecha   = partes[0].split(" ")[0] if len(partes) > 0 else "desconocida"
        hora    = partes[0].split(" ")[1] if len(partes) > 0 else "00:00:00"
        nivel   = partes[1].strip()       if len(partes) > 1 else "INFO"
        mensaje = partes[2].lower()       if len(partes) > 2 else ""

        if nivel in ["Error", "FailureAudit"]:
            nivel = "ERROR"
        elif nivel in ["Warning"]:
            nivel = "WARNING"
        else:
            nivel = "INFO"

        if "logon" in mensaje and "failed" not in mensaje:
            accion = "LOGIN_EXITOSO"
        elif "failed" in mensaje or "failure" in mensaje:
            accion = "LOGIN_FALLIDO"
        elif "logoff" in mensaje:
            accion = "LOGOUT"
        elif "error" in mensaje:
            accion = "ERROR_CRITICO"
        else:
            accion = "EVENTO_SISTEMA"

        return {
            "fecha":   fecha,
            "hora":    hora,
            "nivel":   nivel,
            "usuario": "windows-user",
            "ip":      "windows-server",
            "accion":  accion
        }

    except:
        return {
            "fecha":   "desconocida",
            "hora":    "00:00:00",
            "nivel":   "INFO",
            "usuario": "sistema",
            "ip":      "windows-server",
            "accion":  "EVENTO_SISTEMA"
        }


def enviar_al_siem(eventos):
    try:
        url       = f"http://{IP_SIEM}:{PUERTO}/recibir"
        respuesta = requests.post(url, json={"eventos": eventos}, timeout=5)

        if respuesta.status_code == 200:
            print(f"[ Agente Windows ] {len(eventos)} eventos enviados al SIEM ✅")
        else:
            print(f"[ Agente Windows ] Error al enviar: {respuesta.status_code}")

    except Exception as e:
        print(f"[ Agente Windows ] No se pudo conectar al SIEM: {e}")


def main():
    print("=" * 50)
    print("  🪟 Agente Windows arrancado")
    print(f"  Enviando logs a {IP_SIEM}:{PUERTO}")
    print(f"  Intervalo: {INTERVALO} segundos")
    print("=" * 50)

    while True:
        try:
            lineas  = leer_logs_windows()
            eventos = [parsear_linea_windows(l) for l in lineas]

            if eventos:
                enviar_al_siem(eventos)
            else:
                print("[ Agente Windows ] Sin eventos nuevos")

            time.sleep(INTERVALO)

        except KeyboardInterrupt:
            print("\n🛑 Agente detenido.")
            break


if __name__ == "__main__":
    main()