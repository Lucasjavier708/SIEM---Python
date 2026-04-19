# ============================================================
# database.py — ETAPA 4 actualizada
# Agrega verificación de duplicados antes de guardar.
# ============================================================

import sqlite3

RUTA_DB = "data/siem.db"


def conectar():
    conexion = sqlite3.connect(RUTA_DB)
    return conexion


def inicializar():
    try:
        conexion = conectar()
        cursor   = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha    TEXT,
                hora     TEXT,
                nivel    TEXT,
                usuario  TEXT,
                ip       TEXT,
                accion   TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alertas (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo     TEXT,
                ip       TEXT,
                cantidad INTEGER,
                mensaje  TEXT
            )
        """)

        conexion.commit()
        conexion.close()
        print("[ Database ] Base de datos inicializada correctamente")

    except Exception as e:
        print(f"[ Database ] Error al inicializar: {e}")


def evento_existe(cursor, evento):
    """
    Verifica si un evento ya está guardado en la BD.
    Compara fecha, hora, usuario y accion.
    """
    cursor.execute("""
        SELECT id FROM eventos
        WHERE fecha = ? AND hora = ? AND usuario = ? AND accion = ?
    """, (evento["fecha"], evento["hora"], evento["usuario"], evento["accion"]))

    return cursor.fetchone() is not None


def alerta_existe(cursor, alerta):
    """
    Verifica si una alerta ya está guardada en la BD.
    Compara tipo e ip.
    """
    cursor.execute("""
        SELECT id FROM alertas
        WHERE tipo = ? AND ip = ? AND mensaje = ?
    """, (alerta["tipo"], alerta["ip"], alerta["mensaje"]))

    return cursor.fetchone() is not None


def guardar_eventos(eventos):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()

        nuevos = 0
        for evento in eventos:
            # Solo guardamos si el evento NO existe ya
            if not evento_existe(cursor, evento):
                cursor.execute("""
                    INSERT INTO eventos (fecha, hora, nivel, usuario, ip, accion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    evento["fecha"], evento["hora"], evento["nivel"],
                    evento["usuario"], evento["ip"], evento["accion"]
                ))
                nuevos += 1

        conexion.commit()
        conexion.close()

        if nuevos > 0:
            print(f"[ Database ] {nuevos} eventos nuevos guardados")
        else:
            print(f"[ Database ] Sin eventos nuevos")

    except Exception as e:
        print(f"[ Database ] Error al guardar eventos: {e}")


def guardar_alertas(alertas):
    try:
        conexion = conectar()
        cursor   = conexion.cursor()

        nuevas = 0
        for alerta in alertas:
            # Solo guardamos si la alerta NO existe ya
            if not alerta_existe(cursor, alerta):
                cursor.execute("""
                    INSERT INTO alertas (tipo, ip, cantidad, mensaje)
                    VALUES (?, ?, ?, ?)
                """, (
                    alerta["tipo"], alerta["ip"],
                    alerta["cantidad"], alerta["mensaje"]
                ))
                nuevas += 1

        conexion.commit()
        conexion.close()

        if nuevas > 0:
            print(f"[ Database ] {nuevas} alertas nuevas guardadas")
        else:
            print(f"[ Database ] Sin alertas nuevas")

    except Exception as e:
        print(f"[ Database ] Error al guardar alertas: {e}")
