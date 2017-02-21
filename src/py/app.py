from MealPlanner.MealPlan import MealPlan
from MealPlanner.Meal import Meal
from MealPlanner.databaseCRUDService import mongoCRUD
import socket
import flask
from flask_cors import CORS
import re


# --------for on the pi------------
# also app.run at the bottom
#ipaddr = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
#----------------------------------

app = flask.Flask(__name__)
CORS(app)
meal_db = mongoCRUD('meals')


#mealplan_db = MealPlan('MealPlans')
#------------- Views ------------------------------------#
# @app.route('/', methods = ['GET'])
# def home():
#
#     '''Choose if you want to meal plan or edit database.'''
#
#     return flask.send_from_directory(HTML_DIR,'index.html')
#
# @app.route('/database.html', methods = ['GET', 'POST', 'PUT', 'DELETE'])
# def database_page():
#
#     '''interact with database.'''
#
#     return flask.send_from_directory(HTML_DIR,'database.html')

#------------- databaseCRUDService Meal Methods -------------#
@app.route('/meals/', methods = ['GET', 'POST', 'DELETE'])
def AllEntries():

    '''All entries in database.'''

    if flask.request.method == "GET":

        #List entries based on keyword passed.
        return flask.jsonify(meal_db.readAll())

    if flask.request.method == 'POST':

        '''Create new entry.'''
        name = flask.request.form['name']
        meal_type = flask.request.form['meal type']
        ingredients = flask.request.form['ingredient'].split("\r\n")

		# parse ingredients correctly
        meal_ingredients = {}
        for i, line in enumerate(ingredients):
            line = line.split(' ')
            ingredient_key = ''
            ingredient_value = ''
            for word in line:
                try:
                    ingredient_value = float(word)
                except ValueError:
                    ingredient_key = ingredient_key+' '+word
            if ingredient_key == '': pass
            meal_ingredients[str(ingredient_key).strip()] = str(ingredient_value)
        meal_ingredients.pop('', None)
        meal_object = Meal(name, meal_type, **meal_ingredients)

        if flask.request.form['method']: meal_object.Method(flask.request.form['method'])

        meal_db.create(meal_object)
        return flask.redirect("http://localhost:3001/database.html")

    # elif flask.request.method == 'DELETE':
    #     '''Delete all entries.'''
    #     return flask.jsonify({'deleted':meal_db.deleteAll()})

    else:
        return {'error':'oops'}


@app.route('/meals/keyword=<key>/value=<value>', methods = ['GET','PUT','DELETE'])
def OneEntry(key, value):

    '''Entries that match kv pair in database.'''

    if flask.request.method == 'GET':
        "List entries."
        return flask.jsonify({key+':'+value:meal_db.readByField({key:value})})

    elif flask.request.method == 'PUT':
        "Update entries."
        update_object = meal_db.readByField({key:value})

        flask.request.form['name'] = update_object.name

        return flask.jsonify({key+':'+value:meal_db.readByField({key:value},{update_object})})

    elif flask.request.method == 'DELETE':
        "Delete entries."
        return flask.jsonify({key+':'+value:meal_db.deleteByField({key:value})})

    else:
        return {'error':'oops'}






































#------------- MealPlan Methods -------------#

@app.route('/meals/_id/<_id>/', methods = ['POST','DELETE'])
def addMealToMealList(_id):

    '''Add a meal_object to mealplan_db.meals.'''

    if flask.request.method == "POST":

        meal_object = mealplan_db.readByField({'_id':_id})
        mealplan_db.addMeal(meal_object)
        return flask.jsonify({'meal added:': meal_object})

    elif flask.request.method == "DELETE":

        '''Remove a meal_object from mealplan_db.meals.'''

        meal_object = mealplan_db.readByField({'_id':_id})
        mealplan_db.removeMeal(meal_object)
        return flask.jsonify({'meal removed:': meal_object})

    else:
        return {'error':'oops'}



@app.route('/meals/random/<n>', methods = ['GET'])
def nRandomMeals(n):

    '''N random meals from database.'''
    return flask.jsonify({str(n)+' random meal(s):': mealplan_db.randomMeals(int(n))})


@app.route('/meals/random', methods = ['GET'])
def fiveRandomMeals():

    '''Default 5 random meals from database.'''
    return flask.jsonify({'5 random meals:': mealplan_db.randomMeals(5)})







# Run
if __name__ == '__main__':
    app.run()
  #  app.run(host = ipaddr, port = 5000)
