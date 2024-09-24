def animal_ages(humanYears):
    # Calculamos los años de gato
    if humanYears == 1:
        catYears = 15
        dogYears = 15
    elif humanYears == 2:
        catYears = 15 + 9
        dogYears = 15 + 9
    else:
        catYears = 15 + 9 + (humanYears - 2) * 4
        dogYears = 15 + 9 + (humanYears - 2) * 5

    # Retornamos una lista con los años humanos, años de gato y años de perro
    return [humanYears, catYears, dogYears]

# Ejemplo de uso
print(animal_ages(3))  # Resultado: [3, 28, 29]
