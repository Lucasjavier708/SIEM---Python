# ============================================================
# Punto de entrada del SIEM.
# Desde acá se manejan todos los módulos.
# ============================================================

import time
from src.colector import obtener_eventos
from src.analizer  import analizar
from src.alertas   import alertar
from src.database  import inicializar, guardar_eventos, guardar_alertas

# Cada cuántos segundos revisa los logs
INTERVALO = 10


def mostrar_bienvenida():
    print("=" * 55)
    print("       🛡️  SIEM PYTHON  -  Tiempo Real")
    print("=" * 55)
    print(f"   Revisando logs cada {INTERVALO} segundos")
    print("   Presioná Ctrl+C para detener")
    print("=" * 55)
    print()


def main():
    mostrar_bienvenida()

    # Inicializamos la base de datos una sola vez
    inicializar()
    print()

    ciclo = 1

    # Bucle infinito — corre hasta que presionés Ctrl+C
    while True:
        try:
            print(f"🔍 Ciclo #{ciclo} — leyendo logs...")

            # Recolectamos los últimos 50 eventos
            eventos = obtener_eventos(50)
            print(f"   📋 {len(eventos)} eventos leídos")

            # Guardamos en BD
            guardar_eventos(eventos)

            # Analizamos
            alertas = analizar(eventos)

            # Guardamos alertas
            if len(alertas) > 0:
                guardar_alertas(alertas)
                alertar(alertas)
            else:
                print("   ✅ Sin alertas nuevas")

            print(f"   ⏳ Próxima revisión en {INTERVALO} segundos...\n")
            ciclo += 1

            # Esperamos antes del próximo ciclo
            time.sleep(INTERVALO)

        except KeyboardInterrupt:
            print("\n\n🛑 SIEM detenido por el usuario.")
            break


if __name__ == "__main__":
    main()
