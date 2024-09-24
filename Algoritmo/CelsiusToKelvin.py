def total_pressure(M1, M2, m1, m2, V, T_Celsius):
    # Constante de gases ideales en atm·dm³/mol·K
    R = 0.0821

    # Convertir temperatura de Celsius a Kelvin
    T = T_Celsius + 273.15

    # Calcular la presión total
    P_total = ((m1 / M1) + (m2 / M2)) * R * T / V

    return P_total


# Ejemplo de uso
M1 = 32  # Masa molar del primer gas en g/mol (por ejemplo, oxígeno O2)
M2 = 28  # Masa molar del segundo gas en g/mol (por ejemplo, nitrógeno N2)
m1 = 10  # Masa del primer gas en gramos
m2 = 20  # Masa del segundo gas en gramos
V = 10  # Volumen del recipiente en dm³
T_Celsius = 25  # Temperatura en grados Celsius

print(total_pressure(M1, M2, m1, m2, V, T_Celsius))  # Devolverá la presión total en atm