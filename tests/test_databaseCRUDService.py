from MealPlanner.databaseCRUDService import mongoCRUD
from bson.objectid import ObjectId
from pymongo import MongoClient
import unittest



class Meal():

    def __init__(self, name):
        self.name = name

# Create fake meal objects
meal_object1 = Meal("test meal 1")
meal_object2 = Meal("test meal 2")


class test_mongoCRUD(unittest.TestCase):

    # create test database
    def setUp(self):
        self.db_collection = mongoCRUD("test_database", "test_collection1")

    # delete test database
    def tearDown(self):
        client = MongoClient('localhost', 27017)
        client.drop_database('test_database')

    # create and test by number of entries in db
    def test_collection_create(self):
        self.db_collection.create(meal_object1)
        client = MongoClient('localhost', 27017)

        self.assertEqual(client["test_database"]["test_collection1"].count(), 1)

    #  create and test by number of entries in db
    def test_collection_readAll(self):
        self.db_collection.create(meal_object1)
        self.db_collection.create(meal_object2)
        client = MongoClient('localhost', 27017)

        readAll = self.db_collection.readAll()
        self.assertEqual(client["test_database"]["test_collection1"].count(), len(readAll))

    # create and test ids match
    def test_collection_readByField(self):
        self.db_collection.create(meal_object1)

        readByField = self.db_collection.readByField({"name" : "test meal 1"})
        self.assertEqual(readByField[0]['_id'], str(vars(meal_object1)['_id']))

    # create two, delete one, check id of other matches
    def test_collection_deleteByField(self):
        self.db_collection.create(meal_object1)
        self.db_collection.create(meal_object2)

        client = MongoClient('localhost', 27017)
        self.db_collection.deleteByField({"name" : "test meal 1"})
        remaining_entry = client["test_database"]["test_collection1"].find({})[0]
        self.assertEqual(str(remaining_entry['_id']), str(vars(meal_object2)['_id']))
