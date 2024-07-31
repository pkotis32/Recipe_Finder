import os
from unittest import TestCase
from models import db, User, Recipe, Nutrition_Fact, Ingredient, Ingredient_Info, Recipe_Ingredient, User_Favorite
import time

os.environ['supabase_database_uri'] = "postgresql:///capstone1_test"
os.environ['application_id'] = '32d3247a'
os.environ['application_key'] = '3c429ec629b898d6f4b5f0749f19e576'


from app import app



with app.app_context():
    db.drop_all()
    db.create_all()



class UserViewsTestCase(TestCase):


    @classmethod
    def setUpClass(cls):

        cls.client = app.test_client()

        with app.app_context():

            "add user to database"
            user = User.signup(username = 'phil', email = 'phil@gmail.com', password = 'hello', first_name = 'Phil', last_name = 'Kotis')
            db.session.add(user)
            db.session.commit()

            with cls.client as client:
                "populate some recipes in database"

                with cls.client.session_transaction() as sess:
                    user = User.query.filter_by(username = 'phil').first()
                    sess['curr_user'] = user.id

                query_params = {
                    'ingredients': ['steak']
                }

                resp = client.get('/api/recipes', query_string=query_params, follow_redirects=True)
                assert resp.status_code == 200




    def setUp(self):
        """clear and remake any tables"""
        
        with app.app_context():
            self.client = app.test_client()

            with self.client.session_transaction() as sess:
                    user = User.query.filter_by(username = 'phil').first()
                    sess['curr_user'] = user.id

    
            


    def test_home(self):
        """make sure home page shows up appropriately"""

        with app.app_context():

            with self.client as client:
                
                "check home page when not logged in"

                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.get('/', follow_redirects = True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Get Started', html)


                "check home page when logged in"
                with self.client.session_transaction() as sess:
                    sess['curr_user'] = 1

                resp = client.get('/', follow_redirects = True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Logout', html)
                    

    def test_recipe_results(self):
        """test recipe search results"""

        with app.app_context():

            with self.client as client:

                query_params = {
                    'ingredients': ['steak']
                }

                resp = client.get('/api/recipes', query_string=query_params, follow_redirects=True)
                html = resp.get_data(as_text=True)
                print(html)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('ul class="list-group recipe_list', html)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.get('/api/recipes', query_string=query_params, follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)


    def test_specific_recipe(self):
        """test specific recipe result"""

        with app.app_context():
            
            with self.client as client:

                recipe = Recipe.query.get(1)

                resp = client.get('/api/recipes/1', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(recipe.title, 'Salt-and-Pepper Steak')
                self.assertIn('Salt-and-Pepper Steak', html)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.get('/api/recipes/1', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)


    def test_recipe_ingredients(self):
        """test showing recipe ingredients"""
        with app.app_context():
            with self.client as client:

                resp = client.get('/api/recipes/1/ingredients', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Salt-and-Pepper Steak Ingredients', html)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.get('/api/recipes/1/ingredients', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)


    def test_recipe_nutrition_facts(self):
        """test showing recipe nutrition facts"""

        with app.app_context():
            with self.client as client:

                with self.client.session_transaction() as sess:
                    user = User.query.filter_by(username = 'phil').first()
                    sess['curr_user'] = user.id

                resp = client.get('/api/recipes/1/nutrition_facts', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn('Nutrition Facts', html)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.get('/api/recipes/1/nutrition_facts', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)


    def test_adding_to_favorites(self):
        """test adding recipe to favorites"""

        with app.app_context():
            with self.client as client:

                recipe = Recipe.query.get(1)

                resp = client.post('/api/favorites/1/add', follow_redirects=True)
                favorite = User_Favorite.query.filter_by(recipe_id = recipe.id).first()
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(recipe.id, favorite.recipe_id)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.post('/api/favorites/1/add', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)
            

    def test_deleting_favorite(self):
        """test deleting recipe from favorites""" 

        with app.app_context():
            with self.client as client:

                resp = client.post('/api/favorites/1/delete', follow_redirects=True)
                favorite = User_Favorite.query.filter_by(recipe_id = 1).first()
                self.assertEqual(resp.status_code, 200)
                self.assertIsNone(favorite)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.post('/api/favorites/1/delete', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)

    
    def test_show_favorites(self):
        """test show favorite recipes list"""

        with app.app_context():
            with self.client as client:
                
                resp = client.post('/api/favorites/2/add', follow_redirects=True)
                favorite = User_Favorite.query.get(2)
                favorite = favorite.recipe
                resp = client.get('/api/favorites', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertEqual(resp.status_code, 200)
                self.assertIn(favorite.title, html)

                """make sure not logged in person can access route"""
                with self.client.session_transaction() as sess:
                    del sess['curr_user']

                resp = client.get('/api/favorites', follow_redirects=True)
                html = resp.get_data(as_text=True)
                self.assertIn('Access unauthorized, please login/signup', html)










                



                

