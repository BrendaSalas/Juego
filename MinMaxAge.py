 def dating_age_range(age):
    # Calcular la edad mínima y máxima
    min_age = age // 2 + 7
    max_age = (age - 7) * 2
    return min_age, max_age

# Ejemplo de uso
my_age = 30
min_age, max_age = dating_age_range(my_age)
print(f"La edad recomendada para alguien de {my_age} años es entre {min_age} y {max_age} años.")