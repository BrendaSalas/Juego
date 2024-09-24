def points_per_48(ppg, mpg):
    if mpg == 0:
        return 0
    # Calcular la extrapolación de puntos por 48 minutos
    ppg_per_48 = (ppg / mpg) * 48
    # Redondear a la décima más cercana
    return round(ppg_per_48, 1)

# Ejemplo de uso
ppg = 25  # puntos por juego
mpg = 30  # minutos por juego
print(points_per_48(ppg, mpg))  # Devolverá 40.0

ppg = 0  # si el jugador no anota puntos
mpg = 0  # y no juega minutos
print(points_per_48(ppg, mpg))  # Devolverá 0