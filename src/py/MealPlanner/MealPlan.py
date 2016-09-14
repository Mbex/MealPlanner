from MealPlanner.databaseCRUDService import mongoCRUD
import random.random as rnd

class Meal_Plan(mongoCRUD):

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
        allEntires = self.readAll()
        for entry in allEntries:
            if keyword in entry:
                results.append(entry)

        return results


    def addMeal(self, query_object):

        """Add meal from database to mealPlan object."""

        meal_object = readByField(query_object)
        self.meals.append(meal_object)


    def removeMeal(self, meal_object):

        """Remove meal from mealPlan object."""

        self.meals.pop(meal_object)



    def random_meals(self, n):

        """Get n random n selections of meals
        from database containing .json files.
        """

        allEntries = self.readAll()
        randList = random.sample(range(1, len(allEntries)), n)

        meals = [allEntries[i] for i in randList]

        return meals




    def _parse_stringd_amount(self, string):

        """Returns list of int of amount and unit of amount."""

        split = string.split()
        return [int(split[0]), split[1]]



    def shopping_list(self):

        """Return dictionary of meals with ingredients as keys"""

        shopping_list = {}

        meal_names = []
        for meal in self.meals:

            meal_names.append(meal['name'])

            for ingredient in meal['ingredients']:

                if type(meal['ingredients'][ingredient]) is int:
                    amount = meal['ingredients'][ingredient]
                    unit = "each"
                else:
                    value = self._parse_stringd_amount(meal['ingredients'][ingredient])
                    amount = value[0]
                    unit   = value[1]

                if ingredient not in shopping_list:
                    shopping_list.setdefault(ingredient,[amount, unit])
                else:
                    shopping_list[ingredient][0] += amount


        self.shopping_list = shopping_list
        print "\n"
        print "***************"
        print " Shopping List"
        print "***************"
        print  meal_names
        print "\n"
        return shopping_list
