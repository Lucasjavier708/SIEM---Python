
# En este modulo se leen los logs y convierte cada linea en un diccionario 
# separando la informacion



# RUTA al archivo de logs
import subprocess


def leer_logs(cantidad=50):
    """
    Lee los últimos N eventos del sistema usando journalctl.
    Devuelve una lista de strings, una por cada línea.
    """
    lineas = []

    try:
        # Ejecutamos journalctl como si fuera un comando en la terminal
        resultado = subprocess.run(
            ["journalctl", "-n", str(cantidad), "--no-pager", "-o", "short"],
            capture_output=True,
            text=True
        )

        # Separamos el resultado en líneas
        for linea in resultado.stdout.split("\n"):
            linea_limpia = linea.strip()
            if linea_limpia != "" and not linea_limpia.startswith("--"):
                lineas.append(linea_limpia)

    except Exception as e:
        print(f"[ Collector ] Error al leer logs: {e}")

    return lineas


def parsear_evento(linea):
    """
    Convierte una línea de journalctl en un diccionario.

    Ejemplo de línea:
    "Apr 17 04:17:46 debianl sudo[2479]: lucasuser : TTY=pts/0"

    Devuelve:
    {
        "fecha":   "Apr 17",
        "hora":    "04:17:46",
        "nivel":   "INFO",
        "usuario": "lucasuser",
        "ip":      "local",
        "accion":  "SUDO"
    }
    """
    try:
        partes = linea.split()

        # Fecha y hora
        fecha = partes[0] + " " + partes[1]
        hora  = partes[2]

        # El mensaje es todo lo que viene después del host
        mensaje = " ".join(partes[4:]).lower()

        # Detectamos el nivel según palabras clave en el mensaje
        if "error" in mensaje or "fail" in mensaje or "failed" in mensaje:
            nivel = "ERROR"
        elif "warn" in mensaje:
            nivel = "WARNING"
        else:
            nivel = "INFO"

        # Detectamos la acción según palabras clave
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

        # Intentamos extraer el usuario del mensaje
        usuario = "sistema"
        if "user" in mensaje:
            partes_msg = mensaje.split("user")
            if len(partes_msg) > 1:
                usuario = partes_msg[1].strip().split()[0].replace("(uid=0)", "").strip()

        evento = {
            "fecha":   fecha,
            "hora":    hora,
            "nivel":   nivel,
            "usuario": usuario,
            "ip":      "local",
            "accion":  accion
        }

        return evento

    except Exception as e:
        # Si no podemos parsear la línea devolvemos un evento genérico
        return {
            "fecha":   "desconocida",
            "hora":    "00:00:00",
            "nivel":   "INFO",
            "usuario": "sistema",
            "ip":      "local",
            "accion":  "EVENTO_SISTEMA"
        }


def obtener_eventos(cantidad=50):
    """
    Función principal del módulo.
    Lee los logs y devuelve todos los eventos parseados.
    """
    lineas  = leer_logs(cantidad)
    eventos = []

    for linea in lineas:
        evento = parsear_evento(linea)
        eventos.append(evento)

    return eventos
