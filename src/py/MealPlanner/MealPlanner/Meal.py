#!/home/mikbok/anaconda/bin/python
from MealPlanner.unicodeConvertor import convert

class Meal(object):

    """Meal objects contain all information on different meals"""

    def __init__(self, name, meal_type, **kwargs):
        self.name = name
        if meal_type not in ["breakfast", "lunch", "dinner", "snack"]:
            raise ValueError("Not a valid meal type")
        else:
            self.meal_type = meal_type
            self.ingredients = kwargs

    def __str__(self):
	return str(convert(vars(self)))

    def __repr__(self):
        return str(convert(vars(self)))


    def Method(self, method):
        self.method = method
