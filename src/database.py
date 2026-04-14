# ============================================================
# database.py
# Responsabilidad: crear la base de datos, guardar eventos
# y alertas para que no se pierdan al cerrar el programa.
# ============================================================

import sqlite3
import os

RUTA_DB = "data/siem.db"


def conectar():
    """
    Crea la conexión con la base de datos.
    Si el archivo siem.db no existe, SQLite lo crea solo.
    """
    conexion = sqlite3.connect(RUTA_DB)
    return conexion


def inicializar():
    """
    Crea las tablas si no existen todavía.
    Se ejecuta cada vez que arranca el programa.
    Si las tablas ya existen no hace nada.
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        # Tabla eventos — guarda todo lo que recolecta collector.py
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

        # Tabla alertas — guarda todo lo que detecta analyzer.py
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


def guardar_eventos(eventos):
    """
    Recibe la lista de eventos de collector.py
    y los guarda todos en la tabla eventos.
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        for evento in eventos:
            cursor.execute("""
                INSERT INTO eventos (fecha, hora, nivel, usuario, ip, accion)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                evento["fecha"],
                evento["hora"],
                evento["nivel"],
                evento["usuario"],
                evento["ip"],
                evento["accion"]
            ))

        conexion.commit()
        conexion.close()

        print(f"[ Database ] {len(eventos)} eventos guardados")

    except Exception as e:
        print(f"[ Database ] Error al guardar eventos: {e}")


def guardar_alertas(alertas):
    """
    Recibe la lista de alertas de analyzer.py
    y las guarda todas en la tabla alertas.
    """
    try:
        conexion = conectar()
        cursor = conexion.cursor()

        for alerta in alertas:
            cursor.execute("""
                INSERT INTO alertas (tipo, ip, cantidad, mensaje)
                VALUES (?, ?, ?, ?)
            """, (
                alerta["tipo"],
                alerta["ip"],
                alerta["cantidad"],
                alerta["mensaje"]
            ))

        conexion.commit()
        conexion.close()

        print(f"[ Database ] {len(alertas)} alertas guardadas")

    except Exception as e:
        print(f"[ Database ] Error al guardar alertas: {e}")
