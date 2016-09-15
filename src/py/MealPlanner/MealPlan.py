from MealPlanner.databaseCRUDService import mongoCRUD
import random

class MealPlan(mongoCRUD):

    """Get n random meals from a database and
    display them in a shopping list format
    """


    def __init__ (self, database_name):
        mongoCRUD.__init__(self, database_name)

        self.meals = []
        self.shopping_list = {}


    def search(self, keyword):

        """search through database"""

        results = []
        allEntries = self.readAll()
        for entry in allEntries:
            if keyword in str(entry):
                results.append(entry)

        return results


    def addMeal(self, query_object):

        """Add meal from database to mealPlan object."""

        meal_object = self.readByField(query_object)
        self.meals.append(meal_object[0])


    def removeMeal(self, query_object):

        """Remove meal from mealPlan object."""

        for i, entry in enumerate(self.meals):
            if query_object[query_object.keys()[0]] in str(entry):
                self.meals.pop(i)


    def randomMeals(self, n):

        """Get n random n selections of meals
        from database containing .json files.
        """

        allEntries = self.readAll()
        randList = random.sample(range(0, len(allEntries)), n)

        meals = [allEntries[i] for i in randList]

        return meals


    def _parseStringAmount(self, string):

        """Returns list of int of amount and unit of amount."""

        split = string.split()
        return [int(split[0]), split[1]]



    def shoppingList(self):

        """Return dictionary of meals with ingredients as keys"""

        shopping_list = {}
        for meal in self.meals:

            print meal
            for ingredient in meal['ingredients']:

                print ingredient
                if type(meal['ingredients'][ingredient]) is int:
                    amount = meal['ingredients'][ingredient]
                    unit = "each"
                else:
                    value = self._parseStringAmount(meal['ingredients'][ingredient])
                    amount = value[0]
                    unit   = value[1]

                if ingredient not in shopping_list:
                    shopping_list.setdefault(ingredient,[amount, unit])
                else:
                    shopping_list[ingredient][0] += amount


        self.shopping_list = shopping_list
