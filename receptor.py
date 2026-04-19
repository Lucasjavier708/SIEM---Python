# ============================================================
# receptor.py
# Corre en Kali Linux junto con el SIEM
# Recibe los logs que mandan los agentes via HTTP
# ============================================================

from flask import Flask, request, jsonify
from src.database  import guardar_eventos
from src.analizer  import analizar
from src.database  import guardar_alertas
from src.alertas   import alertar

app = Flask(__name__)


@app.route("/recibir", methods=["POST"])
def recibir():
    """
    Recibe los eventos de los agentes y los procesa.
    """
    try:
        datos   = request.get_json()
        eventos = datos.get("eventos", [])

        if not eventos:
            return jsonify({"status": "sin eventos"}), 200

        # Guardamos los eventos en la BD
        guardar_eventos(eventos)

        # Analizamos y guardamos alertas
        alertas = analizar(eventos)
        if alertas:
            guardar_alertas(alertas)
            alertar(alertas)

        print(f"[ Receptor ] {len(eventos)} eventos recibidos y procesados")

        return jsonify({"status": "ok", "eventos": len(eventos)}), 200

    except Exception as e:
        print(f"[ Receptor ] Error: {e}")
        return jsonify({"status": "error", "mensaje": str(e)}), 500


if __name__ == "__main__":
    print("=" * 50)
    print("  📡 Receptor SIEM arrancado")
    print("  Esperando eventos de los agentes...")
    print("  Puerto: 5000")
    print("=" * 50)
    # host 0.0.0.0 para recibir de toda la red
    app.run(host="0.0.0.0", port=5000, debug=False)