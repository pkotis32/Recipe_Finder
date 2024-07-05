

class Ingredients:
    """ structure to save ingredient info from json object """
    
    def __init__(self, ingredients):
        """ create class with a list of ingredients as an attribute """
        self.ingredients = ingredients



def extract_json(response):
    """ extract information from json response """

    ingredients = response['data']['ingredients']

    return ingredients
