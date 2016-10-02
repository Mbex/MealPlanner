import json
import flask
from flask_cors import CORS
from MealPlanner.MealPlan import MealPlan
from MealPlanner.Meal import Meal
import socket


import socket
ipaddr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


app = flask.Flask(__name__)
CORS(app)
instance = MealPlan('MealPlan')

@app.route('/', methods = ['GET'])
def hello():
	
   '''Welcome Message'''

   return flask.jsonify(["welcome! go to /meals!"])


#------------- databaseCRUDService Methods -------------#

@app.route('/meals', methods = ['GET', 'POST'])
def readAllEntries():

    '''All entries in database.'''

    if flask.request.method == "GET":
        "List entries."
        return flask.jsonify({'all entries': instance.readAll()})

    elif flask.request.method == 'POST':
        "Create new entry."
        name = 'pie'
        meal_type = ' dinner'
        kwargs = {'pastry': '200g'}

        meal_object = Meal(name, meal_type, kwargs)
        instance.create(meal_object)
        return flask.jsonify({'created':meal_object})

    else:
        return {'error':'oops'}


@app.route('/meals/<keyword>', methods = ['GET'])
def searchDatabase(keyword):

    '''Search database by keyword.'''

    return flask.jsonify({'keyword:'+keyword:instance.search((keyword))})


@app.route('/meals/<key>/<value>', methods = ['GET','PUT','DELETE'])
def readOneEntries(key, value):

    '''Entries that match kv pair in database.'''

    if flask.request.method == 'GET':
        "List entries."
        return flask.jsonify({key+':'+value:instance.readByField({key:value})})

    elif flask.request.method == 'PUT':
        "Update entries."
        update_object = instance.readByField({key:value})
        #NOT SURE IN HERE YET
        return flask.jsonify({key+':'+value:instance.readByField({key:value},{update_object})})

    elif flask.request.method == 'DELETE':
        "Delete entries."
        return flask.jsonify({key+':'+value:instance.deleteByField({key:value})})

    else:
        return {'error':'oops'}


#------------- MealPlan Methods -------------#

@app.route('/meals/_id/<_id>/add', methods = ['GET'])
def addMealToMealList(_id):

    '''Add a meal_object to instance.meals'''

    meal_object = instance.readByField({'_id':_id})
    instance.addMeal(meal_object)
    return flask.jsonify({'meal added:': meal_object})


@app.route('/meals/_id/<_id>/remove', methods = ['GET'])
def removeMealFromMealList(_id):

    '''Add a meal_object to instance.meals'''

    meal_object = instance.readByField({'_id':_id})
    instance.removeMeal(meal_object)
    return flask.jsonify({'meal removed:': meal_object})


@app.route('/meals/random/<n>', methods = ['GET'])
def nRandomMeals(n):

    '''n random meals from database.'''
    return flask.jsonify({str(n)+' random meal(s):': instance.randomMeals(int(n))})


@app.route('/meals/random', methods = ['GET'])
def fiveRandomMeals():

    '''default 5 random meals from database.'''
    return flask.jsonify({'5 random meals:': instance.randomMeals(5)})







# Run
if __name__ == '__main__':
    app.run(host = ipaddr)
