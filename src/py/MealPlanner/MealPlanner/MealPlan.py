from MealPlanner.databaseCRUDService import mongoCRUD
import random
import flask

class MealPlan(mongoCRUD):

    """Get n random meals from a database and
    display them in a shopping list format
    """


    def __init__ (self, database_name, collection_name):

        mongoCRUD.__init__(self, database_name, collection_name)

        self.meal_ids = []
        self.shopping_list = {}


    def Save(self, name, array_of_ids):

        """Save ids of meals as entry in database."""
        self.meal_ids = array_of_ids
        self.create_MealPlan(name, array_of_ids)
