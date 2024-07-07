from app import app
from models import db, Ingredient, Recipe, Recipe_Ingredient
import pdb

with app.app_context():
    db.drop_all()
    db.create_all()

    # ingredient = Ingredient(name = 'steak')
    # recipe = Recipe(title='hello', source='hello', url='hello')

    # db.session.add_all([ingredient, recipe])
    # db.session.commit()

    # ingredient= Ingredient.query.filter(Ingredient.name == 'steak').first()
    # ingredient_id = ingredient.id

    # recipe = Recipe.query.filter(Recipe.title == 'hello').first()
    # recipe_id = recipe.id

    # recipe_ingredient = Recipe_Ingredient(recipe_id = recipe_id, ingredient_id = ingredient_id)
    # db.session.add(recipe_ingredient)
    # db.session.commit()





