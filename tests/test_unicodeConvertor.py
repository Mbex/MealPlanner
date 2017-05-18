from MealPlanner.unicodeConvertor import convert
import unittest
import collections



class test_convert(unittest.TestCase):

    def test_is_basestring(self):
        self.assertTrue(isinstance(convert("string"), str))
        self.assertTrue(isinstance(convert(u"unicode"), str))
        self.assertFalse(isinstance(convert(1), str))


    def test_is_collections_Mapping(self):
        test_mapping = {u"A":u"1"}
        self.assertTrue(isinstance(convert(test_mapping).keys()[0], str))
        self.assertTrue(isinstance(convert(test_mapping).values()[0], str))


    def test_is_collections_iterable(self):
        # test_iterable = [1,2,3]
        # self.assertTrue(isinstance(convert(test_iterable), str))
        pass
