from MealPlanner.unicodeConvertor import convert
import unittest

class test_convert(unittest.TestCase):

    def test_is_basestring(self):
        self.assertTrue(isinstance(convert("string"), str))
        self.assertTrue(isinstance(convert(u"unicode"), str))
#
 #   def test_is_collections_Mapping(self):
  #      pass
#
 #   def test_is_collections_iterable(self):
  #      pass
   #                                                                                                                           25,0-1        17%
#
