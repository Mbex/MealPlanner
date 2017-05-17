
def parse_ingredients(ingredients):

    """
    Takes a string of ingredients and quantities separated by new lines
    and parses into a dictionary with key ingredients and quantity values.
    """

    meal_ingredients = {}
    for i, line in enumerate(ingredients):
        line = line.split(' ')
        ingredient_key = ''
        ingredient_value = ''
        for word in line:
            try:
                ingredient_value = float(word)
            except ValueError:
                ingredient_key = ingredient_key+' '+word
        if ingredient_key == '': pass
        meal_ingredients[str(ingredient_key).strip()] = str(ingredient_value)
    meal_ingredients.pop('', None)

    return meal_ingredients
