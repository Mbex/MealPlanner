from MealPlanner.databaseCRUDService import mongoCRUD
import random

class MealPlan(mongoCRUD):

    """Get n random meals from a database and
    display them in a shopping list format
    """


    def __init__ (self, database_name, collection_name):

        mongoCRUD.__init__(self, database_name, collection_name)
        self.meals = []
        self.shopping_list = {}


    # def Add(self, obj):
    # 
    #     """Add meal from database to mealPlan object."""
    #     self.meals.append(obj['_id'])
    #
    #
    # def Remove(self, obj):
    #
    #     """Remove meal from mealPlan object."""
    #     self.meals.remove(obj['_id'])


    def Save(self):

        """Save ids of meals as entry in database."""
        self.create_MealPlan(self.meals)

    # def shoppingList(self):
    #
    #     """Return dictionary of meals with ingredients as keys"""
    #
    #     shopping_list = {}
    #     for meal in self.meals:
    #        print meal['name'], meal['ingredients']
    #       # print type(meal['ingredients'])
    #       # for ingredient in meal['ingredients']:
    #         #   print ingredient, meal['ingredients'][ingredient]
    #          #  print type(ingredient), type(meal['ingredients'][ingredient])
    #
    #             #priznt json.loads(ingredient)
    #
    #
    #     #         if type(meal['ingredients'][ingredient]) is int:
    #     #             amount = meal['ingredients'][ingredient]
    #     #             unit = "each"
    #     #         else:
    #     #             value = self._parseStringAmount(meal['ingredients'][ingredient])
    #     #             amount = value[0]
    #     #             unit   = value[1]
    #     #
    #     #         if ingredient not in shopping_list:
    #     #             shopping_list.setdefault(ingredient,[amount, unit])
    #     #         else:
    #     #             shopping_list[ingredient][0] += amount
    #     #
    #     #
    #     # self.shopping_list = shopping_list
    #     #
    #     #
