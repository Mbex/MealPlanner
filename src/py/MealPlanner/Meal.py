class Meal(object):

    """Meal objects contain all information on different meals"""

    def __init__(self, name, typ, **kwargs):
        self.name = name
        if typ not in ["breakfast", "lunch", "dinner", "snack"]:
            raise ValueError("Not a valid meal type")
        else:
            self.typ = typ
            self.ingredients = kwargs

    def __str__(self):
        return "meal object"

    def __repr__(self):
        pass


    def Method(method):
        self.method = method
