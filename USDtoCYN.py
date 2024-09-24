def usd_to_cny(usd):
    # Tasa de conversión de USD a CNY (puedes actualizarla según sea necesario)
    conversion_rate = 6.75

    # Convertir USD a CNY
    cny = usd * conversion_rate

    # Formatear la salida como un string que indica la cantidad de yuanes
    return f"{cny:.2f} Chinese Yuan"


# Ejemplo de uso
usd_amount = 100
print(usd_to_cny(usd_amount))