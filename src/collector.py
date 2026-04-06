
# En este modulo se leen los logs y convierte cada linea en un diccionario 
# separando la informacion



# RUTA al archivo de logs
RUTA_LOGS = "logs/sample.log"


def leer_logs():
    """
    Lee el archivo de logs línea por línea.
    Devuelve una lista de strings, una por cada línea.
    """
    lineas = []

    # Abrimos el archivo en modo lectura
    archivo = open(RUTA_LOGS, "r")
    contenido = archivo.readlines()
    archivo.close()

    # Recorremos cada línea y eliminamos espacios/saltos de línea
    for linea in contenido:
        linea_limpia = linea.strip()

        # sacamos líneas vacías
        if linea_limpia != "":
            lineas.append(linea_limpia)

    return lineas


def parsear_evento(linea):
    """
    Convierte una línea de log en un diccionario con sus partes.

    Ejemplo de línea:
    "2024-01-15 08:23:11 INFO usuario:admin IP:192.168.1.10 accion:LOGIN_EXITOSO"

    Devuelve:
    {
        "fecha": "2024-01-15",
        "hora": "08:23:11",
        "nivel": "INFO",
        "usuario": "admin",
        "ip": "192.168.1.10",
        "accion": "LOGIN_EXITOSO"
    }
    """

    # Separamos la línea en partes usando el espacio como divisor
    partes = linea.split(" ")

    # Extraemos cada campo
    fecha   = partes[0]
    hora    = partes[1]
    nivel   = partes[2]

    # Los campos usuario, IP y accion tienen formato "clave:valor"
    # Usamos split(":") y tomamos el índice [1] para quedarnos con el valor
    usuario = partes[3].split(":")[1]
    ip      = partes[4].split(":")[1]

    # La IP puede tener dos ":" entonces juntamos todo después del primer ":"
    ip_completa = partes[4].split(":", 1)[1]

    accion  = partes[5].split(":")[1]

    # Armamos y devolvemos el diccionario del evento
    evento = {
        "fecha":   fecha,
        "hora":    hora,
        "nivel":   nivel,
        "usuario": usuario,
        "ip":      ip_completa,
        "accion":  accion
    }

    return evento

# Funcion 
def obtener_eventos():
    """
    Función principal del módulo.
    Lee el archivo y devuelve todos los eventos ya parseados
    como una lista de diccionarios.
    """
    lineas = leer_logs()
    eventos = []

    for linea in lineas:
        evento = parsear_evento(linea)
        eventos.append(evento)

    return eventos
