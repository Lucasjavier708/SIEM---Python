
from src.collector import obtener_eventos


def mostrar_bienvenida():
    print("=" * 55)
    print("          🛡️  SIEM PYTHON  -  Etapa 1")
    print("=" * 55)
    print()


def mostrar_eventos(eventos):
    """
    Muestra en consola todos los eventos recolectados
    de forma legible.
    """
    print(f"📋 Se encontraron {len(eventos)} eventos en el log:")
    print("-" * 55)

    for evento in eventos:
        # Elegimos un ícono según el nivel del evento
        if evento["nivel"] == "INFO":
            icono = "✅"
        elif evento["nivel"] == "WARNING":
            icono = "⚠️ "
        elif evento["nivel"] == "ERROR":
            icono = "🔴"
        else:
            icono = "❓"

        # informacion del evento 
        print(f"{icono} [{evento['fecha']} {evento['hora']}]")
        print(f"   Usuario : {evento['usuario']}")
        print(f"   IP      : {evento['ip']}")
        print(f"   Acción  : {evento['accion']}")
        print()


def main():
    mostrar_bienvenida()

    # --- ETAPA 1: Recolección ---
    print("🔍 Leyendo logs...")
    print()
    eventos = obtener_eventos()
    mostrar_eventos(eventos)

    # --- ETAPA 3: Análisis (a desarrollar) ---
    # alertas = analizar(eventos)

    # --- ETAPA 5: Alertas (a desarrollar) ---
    # alertar(alertas)

    print("=" * 55)
    print("  ✔  Etapa 1 completada. ¡El SIEM está en marcha!")
    print("=" * 55)



if __name__ == "__main__":
    main()
