def parse_ingredients(ingredients):

    """
    Takes a string of ingredients and quantities separated by new lines
    and parses into a dictionary with key ingredients and quantity values.
    """

    ingredients = filter(None, ingredients)
    meal_ingredients = {}

    for i, line in enumerate(ingredients):

        line = line.strip()

        # use the word 'of' as marker for key and value
        if "of" in line:
            line = line.split(' ')
            j = line.index("of")
            ingredient_key = " ".join(line[(j+1):]).replace(",","")
            if ingredient_key == "":
                ingredient_key = " ".join(line[0:j-1]).replace(",","")
            ingredient_value = line[j-1].replace(" a ", "")


        else:
            # otherwise, use ',' as the marker
            if "," in line:
                line = line.split(', ')
            # or a space
            else:
                line = line.split(' ')

            ingredient_value=""
            ingredient_key=""
            for word in line:
                try:
                    trip_ValueError = float(word[0])
                    ingredient_value = word
                except ValueError:
                    ingredient_key += word + " "
                except IndexError:
                    print word
            if ingredient_key == '': pass

        meal_ingredients[str(ingredient_key).strip()] = str(ingredient_value)
    meal_ingredients.pop('', None)

    return meal_ingredients



# print parse_ingredients(
# ("5\r\nappricots\r\n5 bannanas\r\nclementines 5\r\nbunch of dates\r\nelderflower bunch of\r\n5 forest fruits\r\nginormous grapes 5\r\nbunch of heavy horseradish\r\nignomineous itsu bunch of\r\njackfruit, 5\r\nkizu, 5 of\r\nlemons, 2kg\r\n").split("\r\n"))
