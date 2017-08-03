from MealPlanner.databaseCRUDService import mongoCRUD
from MealPlanner.crossDomain import preflight_allow_CORS
from MealPlanner.parseIngredients import parse_ingredients
from MealPlanner.MealPlan import MealPlan
from MealPlanner.Meal import Meal
from MealPlanner.shoppingList import *
from flask_cors import CORS, cross_origin
import socket
import flask
import json
import re
import numpy as np

# --------for on the pi------------
# also app.run at the bottom
#ipaddr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
#----------------------------------

app = flask.Flask(__name__)
cors = CORS(app)

#------------- databaseCRUDService Meal Methods -------------#
Meals_db = mongoCRUD('MealPlanner','Meals') # collection

@app.route('/meals/', methods = ['GET','POST','OPTIONS','DELETE'])
def AllMealEntries():

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
        return flask.redirect("http://localhost:3000/meal_index.html")

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
        return flask.jsonify({key:Meals_db.readByField({key:value})})

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

@app.route('/meals/random', methods = ['GET'])
@cross_origin()
def nRandomMeals():

    '''N random meals from database.'''
    n = flask.request.args.get('n')
    print {"result" : Meals_db.randomMeals(int(n))}
    return flask.jsonify({"result" : Meals_db.randomMeals(int(n))})


#------------- MealPlan Methods -----------------------------#
mp = MealPlan('MealPlanner','MealPlans') # collection

@app.route('/mealplan/', methods = ['GET','POST','OPTIONS'])
def AllMealplanEntries():

    '''All entries in database.'''

    if flask.request.method == 'OPTIONS':
        '''Allow cross origin response.'''
        return preflight_allow_CORS()

    if flask.request.method == "GET":
        '''Show all entries in database.'''
        result = mp.readAll()
        return (str(mp.readAll()).replace("'",'"'), 202)

    if flask.request.method == "POST":
        '''Save meal ids to database.'''
        data = json.loads(flask.request.data)
        [str(x) for x in data['ids']]
        mp.Save(str(data['name']), data['ids'])
        return "Success", 200


@app.route('/mealplan/_id/<mealplan_id>/', methods = ['OPTIONS','DELETE','GET'])
def MealToMealPlan(mealplan_id):

    if flask.request.method == 'OPTIONS':
        '''Allow cross origin response.'''
        return preflight_allow_CORS()

    elif flask.request.method == 'GET':
        '''List entry.'''
        mealplan_object = mp.readByField({'_id':mealplan_id})[0]
        return flask.jsonify(mealplan_object)

    elif flask.request.method == "DELETE":
        '''Remove a mealplan_object from mealplan_db.meals.'''
        mealplan_object = mp.readByField({'_id':mealplan_id})[0]
        mp.deleteByField({"_id":mealplan_id})
        return flask.jsonify({"meal removed" : mealplan_object})


@app.route('/shoppinglist/<mealplan_id>', methods = ['GET'])
def ShoppingList(mealplan_id):

    """
    Returns object of ingredient keys and dict values containing
    ints, strings and dicts (unit : amount) of amounts.
    """

    mealplan_object = mp.readByField({'_id':mealplan_id})[0]
    ingredients = [Meals_db.readByField({"_id":meal_id})[0]['ingredients'] for meal_id in mealplan_object["meal_ids"]]

    # get dict of food keys and amount values
    shopping_list = {}
    for d in ingredients:
        for k, v in d.iteritems():
            shopping_list.setdefault(k, []).append(v)

    # for each ingredient in the shopping list.
    # discern type and consolidate list.
    for k, v in shopping_list.iteritems():
        items = [discern_type(item) for item in v]
        shopping_list[k] = consolidate_list(items)

    return flask.jsonify(shopping_list)





# Run
if __name__ == '__main__':
    app.run(threaded=True)
  #  app.run(host = ipaddr, port = 5000)
