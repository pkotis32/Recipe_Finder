import pdb
# class to save relevant recipe information from json respone
class RecipeClass:

    def __init__(self, title=None, source=None, image=None, url=None, ingredients=None, nutrition_facts=None, calories=None, serves=None, total_time=None, cuisine_type=None, meal_type=None):
        self.title = title
        self.source = source
        self.image = image
        self.url = url
        self.ingredients = ingredients
        self.nutrition_facts = nutrition_facts
        self.calories = calories
        self.serves = serves
        self.total_time = total_time
        self.cuisine_type = cuisine_type
        self.meal_type = meal_type

    def __repr__(self):
        return f"<title={self.title} source={self.source} image={self.image} url={self.url} ingredients={self.ingredients} nutrition_facts={self.nutrition_facts} calories={self.calories} serves={self.serves} total_time={self.total_time} cuisine_type={self.cuisine_type} meal_type={self.meal_type}>"

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
            ingredients = recipe['ingredients']
            nutrition_facts = recipe['totalNutrients']
            calories = recipe['calories']
            serves = recipe['yield']
            total_time = recipe['totalTime']
            cuisine_type = recipe['cuisineType'][0]
            meal_type = recipe['mealType'][0]


            
            recipe = RecipeClass(title=title, source=source, image=image, url=url, ingredients=ingredients, nutrition_facts=nutrition_facts, calories=calories, serves=serves, total_time=total_time, cuisine_type=cuisine_type, meal_type=meal_type)

            
            recipes.append(recipe)

        return recipes
        




