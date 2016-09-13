import json
import re
import os
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId


class mongoCRUD():

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

    def idToObjectId(self, query_object):

        """Modifies query object if key is '_id'
        so value is an objectId.
        """

        key = query_object.keys()[0]
        if key == "_id":
            query_object[key] =  ObjectId(query_object[key])

        return query_object


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
            for key in document:
                document[key] = str(document[key])
                document[str(key)] = document.pop(key)

            results.append(document)

        print results
        return results


    def readByField(self, query_object):

        """Gets all documents in a collection
        that match query_object.
        """

        results = []
        query_object = self.idToObjectId(query_object)
        cursor = self.collection.find(query_object)
        for document in cursor:
            for key in document:
                document[key] = str(document[key])
                document[str(key)] = document.pop(key)
            results.append(document)

        print results
        return json.dumps(results)


    def updateOneField(self, query_object, update_object):

        """Update single object in database."""

        query_object = self.idToObjectId(query_object)

        return self.collection.update_one(
                 query_object, {'$set' : update_object}
                 )


    def updateManyFields(self, query_object, update_object):

        """Update many entries in database."""

        query_object = self.idToObjectId(query_object)

        return self.collection.update_one(
                 query_object, {'$set' : update_object}
                 )


    def deleteByField(self, query_object):

        """Delete meal_object in database."""

        query_object = self.idToObjectId(query_object)

        return self.collection.remove(query_object)
