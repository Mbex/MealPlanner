class Meal(object):
    
    """Meal objects contain all information on different meals"""
    
    def __init__(self, name, typ, **kwargs):
        self.name = name
        if typ not in ["Breakfast", "Lunch", "Dinner"]:
            raise ValueError("Not a valid meal type")
        else:
            self.typ = typ
            self.ingredients = kwargs
            
        self.data = {"name" : self.name, "type" : self.typ, "ingredients" : self.ingredients}

    def __str__(self):
        return "meal object"
        
    def __repr__(self):
        pass
