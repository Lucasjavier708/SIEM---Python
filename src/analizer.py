# ============================================================
# analyzer.py
# Responsabilidad: analizar los eventos y detectar patrones
# sospechosos aplicando reglas de seguridad.
# ============================================================

# Constante: cuántos intentos fallidos antes de considerar fuerza bruta
LIMITE_FUERZA_BRUTA = 5


def detectar_fuerza_bruta(eventos):
    """
    Regla 1: si una misma IP tiene LIMITE_FUERZA_BRUTA o más
    logins fallidos, se considera un ataque de fuerza bruta.

    Usamos un diccionario para contar los intentos por IP:
    {
        "10.0.0.99": 5,
        "192.168.1.55": 3
    }
    """
    alertas = []

    # Diccionario para contar intentos fallidos por IP
    conteo_por_ip = {}

    for evento in eventos:
        if evento["accion"] == "LOGIN_FALLIDO":

            ip = evento["ip"]

            # Si la IP ya está en el diccionario, sumamos 1
            # Si no está, la agregamos con valor 1
            if ip in conteo_por_ip:
                conteo_por_ip[ip] = conteo_por_ip[ip] + 1
            else:
                conteo_por_ip[ip] = 1

    # Ahora revisamos el diccionario y generamos alertas
    for ip, cantidad in conteo_por_ip.items():
        if cantidad >= LIMITE_FUERZA_BRUTA:

            # Creamos la alerta como diccionario
            alerta = {
                "tipo":     "FUERZA_BRUTA",
                "ip":       ip,
                "cantidad": cantidad,
                "mensaje":  f"La IP {ip} tuvo {cantidad} intentos fallidos de login"
            }
            alertas.append(alerta)

    return alertas


def detectar_errores_criticos(eventos):
    """
    Regla 2: si hay un evento de tipo ERROR_CRITICO
    se genera una alerta inmediatamente.
    """
    alertas = []

    for evento in eventos:
        if evento["nivel"] == "ERROR":

            alerta = {
                "tipo":     "ERROR_CRITICO",
                "ip":       evento["ip"],
                "cantidad": 1,
                "mensaje":  f"Error crítico detectado en IP {evento['ip']} usuario {evento['usuario']}"
            }
            alertas.append(alerta)

    return alertas


def analizar(eventos):
    """
    Función principal del módulo.
    Ejecuta todas las reglas y devuelve todas las alertas encontradas.
    """
    # Ejecutamos cada regla y combinamos los resultados
    alertas_fuerza_bruta = detectar_fuerza_bruta(eventos)
    alertas_errores      = detectar_errores_criticos(eventos)

    # Combinamos todas las alertas en una sola lista
    alertas = alertas_fuerza_bruta + alertas_errores

    return alertas
