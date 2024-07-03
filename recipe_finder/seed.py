from app import app
from models import db, User, Favorite, Ingredient, Recipe_Ingredient
import pdb

with app.app_context():
    db.drop_all()
    db.create_all()


    user = User.signup(username = 'philko', password = 'password', email = 'phil@gmail.com', first_name = 'phil', last_name = 'kotis' )

    recipe1 = Favorite(title = 'butter chicken', description = 'amazing', instruction = 'simple', user_id = 1)
    recipe2 = Favorite(title = 'cookies', description = 'tasty', instruction = 'easy', user_id = 1)

    db.session.add_all([user,recipe1,recipe2])
    db.session.commit()

    egg = Ingredient(name = 'egg')
    steak = Ingredient(name = 'steak')
    chicken = Ingredient(name = 'chicken')

    db.session.add_all([egg, steak, chicken])
    db.session.commit()

    recipe_ingredient1 = Recipe_Ingredient(recipe_id = recipe1.id, ingredient_id = egg.id, quantity = 1)
    recipe_ingredient2 = Recipe_Ingredient(recipe_id = recipe1.id, ingredient_id = steak.id, quantity = 1)
    recipe_ingredient3 = Recipe_Ingredient(recipe_id = recipe1.id, ingredient_id = chicken.id, quantity = 1)
    recipe_ingredient4 = Recipe_Ingredient(recipe_id = recipe2.id, ingredient_id = egg.id, quantity = 1)

    db.session.add_all([recipe_ingredient1, recipe_ingredient2, recipe_ingredient3, recipe_ingredient4])
    db.session.commit()

    pdb.set_trace()


