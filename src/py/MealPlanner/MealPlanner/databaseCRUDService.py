from MealPlanner.unicodeConvertor import convert
from bson.objectid import ObjectId
from pymongo import MongoClient
import random
import datetime as dt
import json
import re
import os

class mongoCRUD(object):

    """Interact with mongo database """

    def __init__(self, database_name, collection_name):

        self.client = MongoClient()
        self.collection_name = collection_name
        self.db_name = database_name
        self.database = self.client[database_name]
        self.collection = self.database[collection_name]

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def _strIdToObjectId(self, obj):

        """Modifies object if key is '_id'
        so value is an objectId.
        """

        key = obj.keys()[0]
        if key == "_id":
            obj[key] =  ObjectId(obj[key])

        return obj

    def _objectIdtoStrId(self, obj):

        """Modifies query object if key is '_id'
        so value is a string.
        """

        for key in obj.keys():
            if key == "_id":
                obj[key] =  str(obj[key])

        return obj

    # def search(self, keyword):
    #
    #     """Search through database."""
    #
    #     results = []
    #     allEntries = self.readAll()
    #     for entry in allEntries:
    #         if keyword in str(entry):
    #             results.append(entry)
    #
    #     return results


    def create(self, meal_object):

        """Put meal_object in collection."""

        content = vars(meal_object)
        content['_id'] = ObjectId()
        content['created'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print content

        result = self.collection.insert_one(content)
        print ("created id: %s meal_object: %s" %
                            (content['_id'], meal_object.name))
        return result


    def create_MealPlan(self, list_of_meal_ids):

        """Put meal plan id list in collection."""

        content = {'meal_ids' : list_of_meal_ids}
        content['_id'] = ObjectId()
        content['created'] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print content

        result = self.collection.insert_one(content)
        print "created id: %s MealPlan" % content['_id']

        return result


    def readAll(self):

        """Gets all documents in a collection."""

        results = []
        cursor = self.collection.find()
        for document in cursor:
            results.append(self._objectIdtoStrId(convert(document)))

        return results


    def readByField(self, query_object):

        """Gets all documents in a collection that match query_object."""

        results = []
        query_object = self._strIdToObjectId(query_object)
        cursor = self.collection.find(query_object)
        [results.append(self._objectIdtoStrId(convert(document))) for document in cursor]

        return results


    # def updateOneField(self, query_object, update_object):
    #
    #     """Update field in single entry in database."""
    #
    #     query_object = self._strIdToObjectId(query_object)
    #
    #     return self.collection.update(
    #              query_object, {'$set' : update_object}
    #            )


    def updateManyFields(self, query_object, update_object):

        """Update many fields in single entry in collection."""
        query_object = self._strIdToObjectId(query_object)
        del update_object["_id"]

        return self.collection.update(
                query_object , {'$set' : update_object}
               )


    def deleteAll(self):

        """Remove all entries in collection."""
        return self.collection.remove({})


    def deleteByField(self, query_object):

        """Delete entry in collection."""
        query_object = self._strIdToObjectId(query_object)

        return self.collection.remove(query_object)


    def randomMeals(self, n):

        """Get n random selections of meals from collection."""
        allEntries = self.readAll()
        len_allEntries = len(allEntries)
        if n > len_allEntries:
            n = len_allEntries
        randList = random.sample(range(0, len(allEntries)), n)
        meals = [allEntries[i] for i in randList]

        return meals
