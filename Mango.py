def mango_cost(quantity, price_per_mango):
    # Calcular cuántos grupos de 3 hay y cuántos mangos sobran
    groups_of_three = quantity // 3
    remaining_mangoes = quantity % 3

    # Calcular el costo total: pagamos solo por 2 mangos en cada grupo de 3
    total_cost = (groups_of_three * 2 + remaining_mangoes) * price_per_mango

    return total_cost


# Ejemplo de uso
quantity = 9  # Nathan compra 9 mangos
price_per_mango = 5  # Cada mango cuesta 5 unidades de dinero
print(mango_cost(quantity, price_per_mango))  # Devolverá 30

quantity = 10  # Nathan compra 10 mangos
price_per_mango = 5  # Cada mango cuesta 5 unidades de dinero
print(mango_cost(quantity, price_per_mango))  # Devolverá 35