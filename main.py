# ============================================================
# Punto de entrada del SIEM.
# Desde acá se manejan todos los módulos.
# ============================================================

from src.colector import obtener_eventos
from src.analizer  import analizar
from src.alertas   import alertar
from src.database  import inicializar, guardar_eventos, guardar_alertas



def mostrar_bienvenida():
    print("=" * 55)
    print("          🛡️  SIEM PYTHON  -  Etapa 4")
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

    # ETAPA 4: Base de datos ---
    print("🗄️  Inicializando base de datos...")
    inicializar()
    print()

    #  ETAPA 1: Recolección ---
    print("🔍 Leyendo logs...")
    print()
    eventos = obtener_eventos()
    mostrar_eventos(eventos)

    # ETAPA 4: Guardar eventos ---
    guardar_eventos(eventos)
    print()

    #  ETAPA 3: Análisis ---
    print("🧠 Analizando eventos...")
    print()
    alertas = analizar(eventos)

    # ETAPA 4: Guardar alertas ---
    guardar_alertas(alertas)
    print()

    #  ETAPA 3: Mostrar alertas ---
    alertar(alertas)

    print("=" * 55)
    print("  ✔  Todo guardado en la base de datos.")
    print("=" * 55)


if __name__ == "__main__":
    main()
