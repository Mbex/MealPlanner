from MealPlanner.MealPlan import MealPlan
from MealPlanner.databaseCRUDService import mongoCRUD
#import unittest

#class MealPlanTestCase(unittest.TestCase):

#    def setUp(self):
#        self.mealPlan = MealPlan('testMeals')



#if __name__ == '_main':
#    unittest.main()

test_meal_plan = MealPlan('MealPlanner','testMealPlans')
Meals_db = mongoCRUD('MealPlanner','Meals')
meal_plan1 = Meals_db.readAll()

for meal in meal_plan1:
    test_meal_plan.addMeal(meal)

test_meal_plan.saveMeals()
print "\n go on \n"
print test_meal_plan.randomMeals(1)
