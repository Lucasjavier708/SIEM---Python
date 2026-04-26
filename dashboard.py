from flask import Flask, render_template
import sqlite3

#  aplicación Flask
app = Flask(__name__)

RUTA_DB = "data/siem.db"


def obtener_datos():
    """
    Lee todos los eventos y alertas de la base de datos
    y los devuelve como diccionarios para mostrar en el dashboard.
    """
    try:
        conexion = sqlite3.connect(RUTA_DB)
        conexion.row_factory = sqlite3.Row  # permite acceder por nombre de columna
        cursor = conexion.cursor()

        # Traemos todos los eventos ordenados por fecha y hora
        cursor.execute("SELECT * FROM eventos ORDER BY fecha DESC, hora DESC")
        eventos = cursor.fetchall()

        # Traemos todas las alertas
        cursor.execute("SELECT * FROM alertas ORDER BY id DESC")
        alertas = cursor.fetchall()

        conexion.close()

        return eventos, alertas

    except Exception as e:
        print(f"[ Dashboard ] Error al leer la base de datos: {e}")
        return [], []


def obtener_estadisticas(eventos):
    """
    Calcula estadísticas básicas para mostrar en el dashboard.
    """
    total        = len(eventos)
    exitosos     = sum(1 for e in eventos if e["accion"] == "LOGIN_EXITOSO")
    fallidos     = sum(1 for e in eventos if e["accion"] == "LOGIN_FALLIDO")
    errores      = sum(1 for e in eventos if e["nivel"]  == "ERROR")

    return {
        "total":    total,
        "exitosos": exitosos,
        "fallidos": fallidos,
        "errores":  errores
    }


# Ruta principal — cuando entrás a http://localhost:5000
@app.route("/")
def index():
    eventos, alertas = obtener_datos()
    stats = obtener_estadisticas(eventos)

    return render_template(
        "index.html",
        eventos  = eventos,
        alertas  = alertas,
        stats    = stats
    )


import webbrowser

if __name__ == "__main__":
    webbrowser.open("http://localhost:5000")
    app.run(host="0.0.0.0", port= 5000, debug=True)
