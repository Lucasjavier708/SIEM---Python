# ============================================================
# Aca se muestran las alertas detectadas por el
#                    analizer 
# ============================================================


def alertar(alertas):
    """
    Recibe la lista de alertas y las muestra en consola.
    Si no hay alertas, avisa que todo está bien.
    """

    print("=" * 55)
    print("            🚨  SISTEMA DE ALERTAS")
    print("=" * 55)

    # Si la lista está vacía, todo tranquilo ,  no pasa nada 
    if len(alertas) == 0:
        print("✅ Sin alertas. Todo parece normal.")
        return

    # Si hay alertas se muestra una por una 
    print(f"⚠️  Se encontraron {len(alertas)} alerta(s):\n")

    for alerta in alertas:

        # se elige el  ícono según el tipo de alerta
        if alerta["tipo"] == "FUERZA_BRUTA":
            icono = "🔴"
        elif alerta["tipo"] == "ERROR_CRITICO":
            icono = "💀"
        else:
            icono = "⚠️ "

        # Mostramos la alerta ya echa 
        print(f"{icono} ALERTA: {alerta['tipo']}")
        print(f"   IP      : {alerta['ip']}")
        print(f"   Detalle : {alerta['mensaje']}")
        print()
