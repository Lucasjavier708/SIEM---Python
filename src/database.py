# ============================================================
# database.py Tramo final Database 
# ============================================================



import pyodbc

# ── Configuración de conexión ──────────────────────────────
SERVIDOR = "192.168.3.10"
BASE     = "siem_db"
USUARIO  = "sa"
PASSWORD  = "lucas1025."

CADENA_CONEXION = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVIDOR};"
    f"DATABASE={BASE};"
    f"UID={USUARIO};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;"
)


def conectar():
    conexion = pyodbc.connect(CADENA_CONEXION)
    return conexion


def inicializar():
    try:
        conexion = conectar()
        cursor   = conexion.cursor()

        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='eventos')
            CREATE TABLE eventos (
                id       INT IDENTITY PRIMARY KEY,
                fecha    VARCHAR(20),
                hora     VARCHAR(10),
                nivel    VARCHAR(10),
                usuario  VARCHAR(100),
                ip       VARCHAR(50),
                accion   VARCHAR(50)
            )
        """)

        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='alertas')
            CREATE TABLE alertas (
                id       INT IDENTITY PRIMARY KEY,
                tipo     VARCHAR(50),
                ip       VARCHAR(50),
                cantidad INT,
                mensaje  VARCHAR(500)
            )
        """)

        conexion.commit()
        conexion.close()
        print("[ Database ] SQL Server inicializado correctamente")

    except Exception as e:
        print(f"[ Database ] Error al inicializar: {e}")


def evento_existe(cursor, evento):
    cursor.execute("""
        SELECT id FROM eventos
        WHERE fecha = ? AND hora = ? AND usuario = ? AND accion = ?
    """, (evento["fecha"], evento["hora"], evento["usuario"], evento["accion"]))
    return cursor.fetchone() is not None


def alerta_existe(cursor, alerta):
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
            print(f"[ Database ] {nuevos} eventos nuevos guardados en SQL Server")
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
            print(f"[ Database ] {nuevas} alertas nuevas guardadas en SQL Server")
        else:
            print(f"[ Database ] Sin alertas nuevas")

    except Exception as e:
        print(f"[ Database ] Error al guardar alertas: {e}")