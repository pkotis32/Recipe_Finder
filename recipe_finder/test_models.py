import os
from unittest import TestCase
from models import db, User, Recipe, Nutrition_Fact, Ingredient, Ingredient_Info, Recipe_Ingredient, User_Favorite


os.environ['supabase_database_uri'] = "postgresql:///capstone1_test"

from app import app


with app.app_context():
    db.drop_all()
    db.create_all()


class UserModelTestCase(TestCase):
    
    
    
    
    def setUp(self):
        with app.app_context():
            db.drop_all()
            db.create_all()
            # Create a test user
            user = User.signup(username = 'phil', email = 'phil@gmail.com', password = 'hello', first_name = 'Phil', last_name = 'Kotis')
            db.session.add(user)
            db.session.commit()

    def test_user_signup(self):
        """test valid user signup"""
        with app.app_context():

            user = User.query.filter_by(username = 'phil').first()
            self.assertEqual(user.username, 'phil')
            self.assertEqual(user.email, 'phil@gmail.com')
            self.assertTrue(user.password.startswith('$2b$'))
            self.assertEqual(user.first_name, 'Phil')
            self.assertEqual(user.last_name, 'Kotis')

    def test_user_login(self):
        """test valid user login"""

        with app.app_context():
            user = User.query.filter_by(username = 'phil').first()

            print(user)
            print('hello')
            print(User.authenticate('phil', 'hello'))
            self.assertEqual(User.authenticate('phil', 'hello'), user)
            self.assertFalse(User.authenticate('phil', 'password'))

    def test_recipe_model(self):
        """test recipe model"""

        with app.app_context():
            recipe = Recipe(title = 'recipe', source = 'google', url = 'google.com')

            self.assertEqual(recipe.title, 'recipe')
            self.assertEqual(recipe.source, 'google')
            self.assertEqual(recipe.url, 'google.com')

    def test_nutrition_fact_model(self):
        """test nutrition_fact model"""

        nutrition_facts = Nutrition_Fact(label = 'fat', quantity = 5, unit = 'g', recipe_id = 1)

        self.assertEqual(nutrition_facts.label, 'fat')
        self.assertEqual(nutrition_facts.quantity, 5)
        self.assertEqual(nutrition_facts.unit, 'g')
        self.assertEqual(nutrition_facts.recipe_id, 1)

    def test_ingredient_model(self):
        """test ingredient model"""

        ingredient = Ingredient(name = 'chicken')

        self.assertEqual(ingredient.name, 'chicken')

    def test_ingredient_info(self):
        """test ingredient info"""

        ingredient_info = Ingredient_Info(text = '1 cup of water')

        self.assertEqual(ingredient_info.text, '1 cup of water')

    
    def test_recipe_ingredient(self):
        """test recipe_ingredient model"""

        recipe_ingredient = Recipe_Ingredient(recipe_id = 1, ingredient_id = 1)

        self.assertEqual(recipe_ingredient.recipe_id, 1)
        self.assertEqual(recipe_ingredient.ingredient_id, 1)


    def test_user_favorite(self):
        """test user_favorite model"""

        user_favorite = User_Favorite(user_id = 1, recipe_id = 1)

        self.assertEqual(user_favorite.user_id, 1)
        self.assertEqual(user_favorite.recipe_id, 1)