import pdb
# class to save relevant recipe information from json respone
class RecipeClass:

    def __init__(self, title=None, source=None, image=None, url=None, ingredient_lines=None, ingredients=None, calories=None, total_time=None, cuisine_type=None, meal_type=None):
        self.title = title
        self.source = source
        self.image = image
        self.url = url
        self.ingredient_lines = ingredient_lines
        self.ingredients = ingredients
        self.calories = calories
        self.total_time = total_time
        self.cuisine_type = cuisine_type
        self.meal_type = meal_type

    def __repr__(self):
        return f"<title={self.title} source={self.source} image={self.image} url={self.url} ingredient_lines={self.ingredient_lines} ingredients={self.ingredients} calories={self.calories} total_time={self.total_time} cuisine_type={self.cuisine_type} meal_type={self.meal_type}>"

    @staticmethod
    def extract_from_json(response):
        """ extract recipe information from response and return the recipes, also save recipes to database """
        recipes = []
        for hit in response['hits']:
            recipe = hit['recipe']

            title = recipe['label']
            source = recipe['source']
            image = recipe['image']
            url = recipe['url']
            ingredient_lines = recipe['ingredientLines']
            ingredients = recipe['ingredients']
            calories = recipe['calories']
            total_time = recipe['totalTime']
            cuisine_type = recipe['cuisineType'][0]
            meal_type = recipe['mealType'][0]
            
            recipe = RecipeClass(title=title, source=source, image=image, url=url, ingredient_lines=ingredient_lines, ingredients=ingredients, calories=calories, total_time=total_time, cuisine_type=cuisine_type, meal_type=meal_type)

            recipes.append(recipe)

        return recipes
        




