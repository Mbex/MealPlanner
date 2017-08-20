from MealPlanner.MealPlan import MealPlan
from MealPlanner.databaseCRUDService import mongoCRUD
from MealPlanner.shoppingList import *
import re

mp = MealPlan('MealPlanner','MealPlans') # collection
Meals_db = mongoCRUD('MealPlanner','Meals') # collection


mealplan_object = mp.readByField({'_id':"59836a3d6225eb1208667049"})[0]
ingredients = [Meals_db.readByField({"_id":meal_id})[0]['ingredients'] for meal_id in mealplan_object["meal_ids"]]

# get dict of food keys and amount values
shopping_list = {}
for d in ingredients:
    for k, v in d.iteritems():
        shopping_list.setdefault(k, []).append(v)
print shopping_list

# for each ingredient in the shopping list.
for k, v in shopping_list.iteritems():
    items = [discern_type(item) for item in v]
    print k, consolidate_list(items)

# print consolidate_list(items_)

#
#
#
# ints = 0
# strings = {}
# mixed = {}
# for item in items:
#     if isinstance(item, int):
#         ints += item
#     if isinstance(item, str):
#         try:
#             strings[item] += 1
#         except:
#             strings[item] = 1
#     if isinstance(item, tuple):
#         amount = int(item[0])
#         unit = item[1]
#         try:
#             mixed[unit] += amount
#         except:
#             mixed[unit] = amount
#
#     return ints, strings, mixed
#
#
#
# # units.append(items[i][1])
# # nums.append(int(items[i][0]))
# #
# # nums = np.array(nums)
# # for uniq_unit in list(set(units)):
# # indeces = [i for i, x in enumerate(units) if x == uniq_unit]
# # total_val = nums[indeces].sum()
# # print total_val
# # # print uniq_unit, total_val
# #
# # print k, items, nums, units
