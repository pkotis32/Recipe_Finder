
import pdb
# class to save relevant recipe information from json respone
class Recipe:

    def __init__(self, source=None, image=None, recipe_url=None, ingredient_lines=None, ingredients=None, calories=None, total_time=None, cuisine_type=None, meal_type=None):
        self.source = source
        self.image = image
        self.recipe_url = recipe_url
        self.ingredient_lines = ingredient_lines
        self.ingredients = ingredients
        self.calories = calories
        self.total_time = total_time
        self.cuisine_type = cuisine_type
        self.meal_type = meal_type

    def __repr__(self):
        return f"<source={self.source} image={self.image} recipe_url={self.recipe_url} ingredient_lines={self.ingredient_lines} ingredients={self.ingredients} calories={self.calories} total_time={self.total_time} cuisine_type={self.cuisine_type} meal_type={self.meal_type}>"

    @staticmethod
    def extract_from_json(response):
        recipes = []
        for hit in response['hits'][:3]:
            recipe = hit['recipe']

            source = recipe['source']
            image = recipe['image']
            recipe_url = recipe['url']
            ingredient_lines = recipe['ingredientLines']
            ingredients = recipe['ingredients']
            calories = recipe['calories']
            total_time = recipe['totalTime']
            cuisine_type = recipe['cuisineType'][0]
            meal_type = recipe['mealType'][0]
            recipe = Recipe(source=source, image=image, recipe_url=recipe_url, ingredient_lines=ingredient_lines, ingredients=ingredients, calories=calories, total_time=total_time, cuisine_type=cuisine_type, meal_type=meal_type)
            recipes.append(recipe)

        return recipes
        




