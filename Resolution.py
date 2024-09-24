import math

def convert_to_16_9(x_res, y_res):
    # Calcular el nuevo ancho manteniendo la misma altura y ajustando la relación a 16:9
    new_x_res = math.ceil(y_res * 16 / 9)
    return new_x_res, y_res

# Ejemplo de uso
x_res = 1440  # Ancho original
y_res = 1080  # Altura original

new_x_res, new_y_res = convert_to_16_9(x_res, y_res)
print(f"La nueva resolución ajustada a 16:9 es {new_x_res}x{new_y_res}")