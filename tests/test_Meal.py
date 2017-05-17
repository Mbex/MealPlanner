from MealPlanner.Meal import Meal
import unittest


class MealTestCase(unittest.TestCase):

    def setUp(self):
	self.meal = Meal(name='TestName', meal_type='breakfast', ingredients={'A':'2','B':2})

    def test_meal_name(self):
        self.assertEqual(self.meal.name, 'TestName', 'name is wrong')       

    def test_meal_type(self):
        self.assertEqual(self.meal.meal_type, 'breakfast', 'meal type is wrong')

    def test_ingredients(self):
        ingredients = self.meal.ingredients['ingredients']
        self.assertTrue('A' in ingredients.keys(), 'ingredients key is wrong')
        self.assertTrue('B' in ingredients.keys(), 'ingredients key is wrong')
        self.assertTrue(ingredients['A'] == '2', 'ingredient value is wrong')
        self.assertTrue(ingredients['B'] == 2, 'ingredient value is wrong')

    def test_method(self):
        self.meal.Method("Test Method")
        self.assertEqual(self.meal.method, "Test Method", 'method is wrong')



if __name__ == '__main_':
    unittest.main()
