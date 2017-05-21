from MealPlanner.parseIngredients import parse_ingredients
import unittest


# 5
# appricots
# 5 bannanas
# clementines 5
# bunch of dates
# elderflower bunch of
# 5 forest fruits
# ginormous grapes 5
# bunch of heavy horseradish
# ignomineous itsu bunch of
# jackfruit, 5
# kizu, 5 of
# lemons, 2kg


class test_parse_ingredients(unittest.TestCase):

    def setUp(self):
        self.ingredients_test = "5\r\nappricots\r\n5 bannanas\r\nclementines 5\r\nbunch of dates\r\nelderflower bunch of\r\n5 forest fruits\r\nginormous grapes 5\r\nbunch of heavy horseradish\r\nignomineous itsu bunch of\r\njackfruit, 5\r\nkizu, 5 of\r\nlemons, 2kg\r\n"

    def test_parse_the_ingredients(self):
        answer = parse_ingredients(self.ingredients_test.split("\r\n"))
        self.assertEqual(answer['jackfruit'],"5")
        self.assertEqual(answer['dates'],"bunch")
        self.assertEqual(answer['clementines'],"5")
        self.assertEqual(answer['appricots'],"")
        self.assertEqual(answer['lemons'],"2kg")
        self.assertEqual(answer['kizu'],"5")
        self.assertEqual(answer['ignomineous itsu'],"bunch")
        self.assertEqual(answer['ginormous grapes'],"5")
        self.assertEqual(answer['bannanas'],"5")
        self.assertEqual(answer['forest fruits'],"5")
        self.assertEqual(answer['heavy horseradish'],"bunch")
        self.assertEqual(answer['elderflower'],"bunch")
