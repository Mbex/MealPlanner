import json
import re
import os
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from MealPlanner.unicodeConvertor import convert

class mongoCRUD(object):

    """Interact with mongo database """

    def __init__(self, database_name):

        self.client = MongoClient()
        self.db_name = None
        self.collection = None
        self.db_name = database_name
        self.database = self.client[database_name]
        self.collection = self.database[database_name]

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

    def search(self, keyword):

        """Search through database."""

        results = []
        allEntries = self.readAll()
        for entry in allEntries:
            if keyword in str(entry):
                results.append(entry)

        return results


    def create(self, meal_object):

        """Put meal_object in collection in database."""

        content = vars(meal_object)
        result = self.collection.insert_one(content)

        print "created id: %s meal_object: %s" % (result.inserted_id, meal_object.name)
        return result


    def readAll(self):

        """Gets all documents in a collection."""

        results = []
        cursor = self.collection.find()
        for document in cursor:
            results.append(self._objectIdtoStrId(convert(document)))

        return results

    def readByField(self, query_object):

        """Gets all documents in a collection
        that match query_object.
        """

        results = []
        query_object = self._strIdToObjectId(query_object)
        cursor = self.collection.find(query_object)
        [results.append(self._objectIdtoStrId(convert(document))) for document in cursor]

        return results


    def updateOneField(self, query_object, update_object):

        """Update field in single entry in database."""

        query_object = self._strIdToObjectId(query_object)

        return self.collection.update_one(
                 query_object, {'$set' : update_object}
               )


    def updateManyFields(self, query_object, update_object):

        """Update many fields in single entry in database."""

        query_object = self._strIdToObjectId(query_object)

        return self.collection.update_one(
                 query_object, {'$set' : update_object}
               )

    def deleteAll(self):

	"""Remove all entries in Database."""

	return self.collection.remove({})


    def deleteByField(self, query_object):

        """Delete meal_object in database."""

        query_object = self._strIdToObjectId(query_object)

        return self.collection.remove(query_object)
