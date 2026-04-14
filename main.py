# ============================================================
# Punto de entrada del SIEM.
# Desde acá se manejan todos los módulos.
# ============================================================

from src.colector import obtener_eventos
from src.analizer  import analizar
from src.alertas   import alertar


def mostrar_bienvenida():
    print("=" * 55)
    print("          🛡️  SIEM PYTHON  -  Etapa 3")
    print("=" * 55)
    print()


def mostrar_eventos(eventos):
    print(f"📋 Se encontraron {len(eventos)} eventos en el log:")
    print("-" * 55)

    for evento in eventos:
        if evento["nivel"] == "INFO":
            icono = "✅"
        elif evento["nivel"] == "WARNING":
            icono = "⚠️ "
        elif evento["nivel"] == "ERROR":
            icono = "🔴"
        else:
            icono = "❓"

        print(f"{icono} [{evento['fecha']} {evento['hora']}]")
        print(f"   Usuario : {evento['usuario']}")
        print(f"   IP      : {evento['ip']}")
        print(f"   Acción  : {evento['accion']}")
        print()


def main():
    mostrar_bienvenida()

    # ---  Recolección ---
    print("🔍 Leyendo logs...")
    print()
    eventos = obtener_eventos()
    mostrar_eventos(eventos)

    # --- Análisis ---
    print("🧠 Analizando eventos...")
    print()
    alertas = analizar(eventos)

    # --- Alertas ---
    alertar(alertas)

    print("=" * 55)
    print("  ✔  Análisis completado.")
    print("=" * 55)


if __name__ == "__main__":
    main()
