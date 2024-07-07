

def read_ingredients():
    """ read ingredients from file """

    file_path = 'top_1000_ingredients.txt'

    ingredients = []
    with open(file_path, 'r') as file:
        for line in file:
            ingredient = line.strip()
            ingredients.append(ingredient)

    print(ingredients)
    return ingredients


read_ingredients()