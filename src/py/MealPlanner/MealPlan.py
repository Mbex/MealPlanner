from flask import Flask

class Meal_Plan(Database_Mixin):
    
    """Get n random meals from a database and 
    display them in a shopping list format
    """
    
    
    def __init__ (self, database_name):
        Database_Mixin.__init__(self, database_name)
      
        self.meals = []  
        self.meal_names = []
        self.shopping_list = {}
     
    
    def add_meal(self, meal):
        
        """Adds meal to meal database.
        Pass dictionary for json dump to work.
        """
        
        self.write_entry(meal.name, meal.data)
       
    
    def _parse_stringd_amount(self, string):
    
        """returns list of int of amount and unit of amount"""
    
        split = string.split()
        return [int(split[0]), split[1]]
    
    @app.route("/")
    def plan_meals(self, n):
        
        """Get n random n selections of meals 
        from database containing .json files
        """
        
        meals = self.choose_entries(n)
        self.meals = meals
        for meal in meals: self.meal_names.append(meal['name'])
        return meals

    
    def make_shopping_list(self):
                
        """Return dictionary of meals with ingredients as keys"""
        
        shopping_list = {}  

        meal_names = []
        for meal in self.meals:
            
            meal_names.append(meal['name'])
            
            for ingredient in meal['ingredients']:
         
                if type(meal['ingredients'][ingredient]) is int:
                    amount = meal['ingredients'][ingredient]
                    unit = "each"
                else:
                    value = self._parse_stringd_amount(meal['ingredients'][ingredient])
                    amount = value[0]
                    unit   = value[1]
                
                if ingredient not in shopping_list:
                    shopping_list.setdefault(ingredient,[amount, unit])
                else:
                    shopping_list[ingredient][0] += amount
                    
        
        self.shopping_list = shopping_list 
        print "\n"
        print "***************"
        print " Shopping List"
        print "***************"
        print  meal_names
        print "\n"
        return shopping_list  
    
    
if __name__ == "__main__":
    app.run()