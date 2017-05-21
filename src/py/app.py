from MealPlanner.MealPlan import MealPlan
from MealPlanner.Meal import Meal
from MealPlanner.databaseCRUDService import mongoCRUD
from MealPlanner.crossDomain import preflight_allow_CORS
from MealPlanner.parseIngredients import parse_ingredients
import socket
import flask
from flask_cors import CORS, cross_origin
import re
import json

# --------for on the pi------------
# also app.run at the bottom
#ipaddr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
#----------------------------------
app = flask.Flask(__name__)
cors = CORS(app)
Meals_db = mongoCRUD('MealPlanner','Meals') # collection
#------------- databaseCRUDService Meal Methods -------------#
@app.route('/meals/', methods = ['GET','POST','OPTIONS','DELETE'])
def AllEntries():

    '''All entries in database.'''

    if flask.request.method == 'OPTIONS':
        '''Allow cross origin response.'''
        return preflight_allow_CORS()


    if flask.request.method == "GET":
        '''Show all entries in database.'''
        return (str(Meals_db.readAll()).replace("'",'"'), 202)


    if flask.request.method == 'POST':
        '''Create new entry.'''

        name = flask.request.form['name']
        meal_type = flask.request.form['meal type']
        ingredients = flask.request.form['ingredients'].split("\r\n")
        meal_ingredients = parse_ingredients(ingredients)
        meal_object = Meal(name, meal_type, **meal_ingredients)
        if flask.request.form['method']:
             meal_object.Method(flask.request.form['method'])
        Meals_db.create(meal_object)
        return flask.redirect("http://localhost:3000/meal_search.html")

    if flask.request.method == 'DELETE':
        '''Delete all entries.'''
        return flask.jsonify({'deleted':Meals_db.deleteAll()})

    else:
        return {'flask.request.method':'NOT FOUND'}



@app.route('/meals/<key>/<value>/', methods = ['GET','PUT','DELETE','OPTIONS'])
@cross_origin()
def OneEntry(key, value):

    '''Entries that match kv pair in database.'''

    if flask.request.method == 'OPTIONS':
        '''Allow cross origin response.'''
        return preflight_allow_CORS()


    elif flask.request.method == 'GET':
        '''List entry.'''
        return flask.jsonify({key+':'+value:Meals_db.readByField({key:value})})


    elif flask.request.method == 'PUT':
        '''Update entry.'''

        update_dict = json.loads(flask.request.data)
        update_dict['ingredients'] = parse_ingredients(update_dict['ingredients'].split("\n"))

        Meals_db.updateManyFields({'_id':update_dict['_id']}, update_dict)
        return 'Success', 200, {'Content-Type': 'text/plain'}


    elif flask.request.method == 'DELETE':
        '''Delete entry.'''

        {key+':'+value : Meals_db.deleteByField({key : value})}
        return 'Success', 200, {'Content-Type': 'text/plain'}


    else:
        return 500




























#
#
#
# MealPlans_db = mongoCRUD('MealPlanner','MealPlans')
#
#
# #------------- MealPlan Methods -------------#
#
# @app.route('/mealplan/_id/<_id>/', methods = ['POST','DELETE'])
# def addMealToMealList(_id):
#
#     '''Add a meal_object to mealplan_db.meals.'''
#
#     if flask.request.method == "POST":
#
#         meal_object = mealplan_db.readByField({'_id':_id})
#         MealPlans_db.addMeal(meal_object)
#         return flask.jsonify({'meal added:': meal_object})
#
#     elif flask.request.method == "DELETE":
#
#         '''Remove a meal_object from mealplan_db.meals.'''
#
#         meal_object = mealplan_db.readByField({'_id':_id})
#         MealPlans_db.removeMeal(meal_object)
#         return flask.jsonify({'meal removed:': meal_object})
#
#     else:
#         return {'error':'oops'}
#
#
#
# @app.route('/mealplan/random/<n>', methods = ['GET'])
# def nRandomMeals(n):
#
#     '''N random meals from database.'''
#     return flask.jsonify({str(n)+' random meal(s):': MealPlans_db.randomMeals(int(n))})
#
#
# @app.route('/mealplan/random', methods = ['GET'])
# def fiveRandomMeals():
#
#     '''Default 5 random meals from database.'''
#     return flask.jsonify({'5 random meals:': MealPlans_db.randomMeals(5)})











# Run
if __name__ == '__main__':
    app.run(threaded=True)
  #  app.run(host = ipaddr, port = 5000)
