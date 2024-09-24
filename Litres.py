 def litres(time):
    # Calcular la cantidad de litros, redondeando hacia abajo
    return int(time * 0.5)

# Ejemplo de uso
time = 3  # Nathan ha estado pedaleando por 3 horas
print(litres(time))  # Devolverá 1 litro

time = 6.7  # Nathan ha estado pedaleando por 6.7 horas
print(litres(time))  # Devolverá 3 litros