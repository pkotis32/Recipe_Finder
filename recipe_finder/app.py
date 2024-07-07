from flask import Flask, render_template, request, session, redirect, flash, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Recipe, Ingredient_Line, Ingredient, Ingredient_Info, Recipe_Ingredient, User_Favorite
from forms import Register, Login
from api_models import RecipeClass
from config import application_id, application_key
import requests
import json
import pdb

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone1"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

BASE_URL = 'https://api.edamam.com/api/recipes/v2'



def read_ingredients():
    """ read ingredients from file """

    file_path = 'top_1000_ingredients.txt'

    ingredients = []
    with open(file_path, 'r') as file:
        for line in file:
            ingredient = line.strip()
            ingredients.append(ingredient)

    return ingredients



def save_ingredients_to_database(ingredients):
    """ save the ingredients to the database """
    
    unique_ingredients = set(ingredients)
    
    # delete any existing ingredients if there are any
    db.session.query(Ingredient).delete()
    db.session.commit()

    for ingredient in unique_ingredients:
        ingredient = Ingredient(name = ingredient)
        db.session.add(ingredient)

    db.session.commit()

    return jsonify({'message': 'ingredients saved successfully'})


def save_recipe_info_to_database(recipes):
    """ save all recipe information to the database """
    
    for recipe in recipes:
        title = recipe.title
        source = recipe.source
        image = recipe.image
        url = recipe.url
        ingredient_lines = recipe.ingredient_lines
        calories = recipe.calories
        total_time = recipe.total_time
        cuisine_type = recipe.cuisine_type
        meal_type = recipe.meal_type

        database_recipe = Recipe(title=title, source=source, image=image, url=url, calories=calories, total_time=total_time, cuisine_type=cuisine_type, meal_type=meal_type)

        db.session.add(database_recipe)
        db.session.commit()
    
        recipe_id = database_recipe.id

        for ingredient_line in ingredient_lines:
            line = Ingredient_Line(line=ingredient_line, recipe_id = recipe_id)
            db.session.add(line)
            db.session.commit()

        for ingredient in recipe.ingredients:
            name = ingredient['food']
            database_ingredient = Ingredient(name = name)
            db.session.add(database_ingredient)
            db.session.commit()

            ingredient_id = database_ingredient.id
            quantity = ingredient['quantity']
            measure = ingredient['measure']
            weight = ingredient['weight']
            food_category = ingredient['foodCategory']
            image = ingredient['image']

            ingredient_info = Ingredient_Info(quantity=quantity, measure=measure, weight=weight, food_category=food_category, image=image, ingredient_id=ingredient_id)
            db.session.add(ingredient_info)
            db.session.commit()

            recipe_ingredient = Recipe_Ingredient(recipe_id=recipe_id, ingredient_id=ingredient_id)
            db.session.add(recipe_ingredient)
            db.session.commit()




@app.before_request
def add_user_to_global():

    if 'curr_user' in session:
        g.user = User.query.get(session['curr_user'])
    else:
        g.user = None

        

@app.route('/')
def show_home():

    return render_template('home.html')

@app.route('/register', methods=['get', 'post'])
def register():
    """ register user """
    
    form = Register()

    if form.validate_on_submit(): 
        
        new_user = User.signup(username = form.username.data,
                                password = form.password.data,
                                email = form.email.data,
                                first_name = form.first_name.data,
                                last_name = form.last_name.data)

        db.session.add(new_user)
        db.session.commit()

        session['curr_user'] = new_user.id
        flash('Registerred Successfully', 'success')

        return redirect('/')
    


    return render_template('register_form.html', form = form)


@app.route('/login', methods=['get', 'post'])
def login():  
    """ login user """

    form = Login()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username = username, password = password)


        if user:
            session['curr_user'] = user.id
            flash('Successfully logged in', 'success')
        else:
            flash('Please login/signup first', 'danger')

        return redirect('/')
        

    return render_template('login_form.html', form = form)


@app.route('/logout')
def logout():
    """ logout user """

    if g.user:
        del session['curr_user']
        flash('Logged out successfully', 'success')
    else:
        flash('Please login/signup first', 'danger')


    return redirect('/')


@app.route('/get_ingredients')
def get_ingredients():
    """ return list of ingredients """

    ingredients = read_ingredients()
    ingredients = [ingredient.lower() for ingredient in ingredients]
    ingredients = set(ingredients)


    return jsonify({'ingredients': list(ingredients)})


@app.route('/save_ingredients', methods=['post'])
def save_ingredients():
    """ save ingredients to database """

    ingredients = read_ingredients()
    ingredients = [ingredient.lower() for ingredient in ingredients]

    return save_ingredients_to_database(ingredients)


@app.route('/api/recipes')
def get_recipes():
    """ get all relevant recipes """

    params = {
        'type': 'public',
        'q': 'chicken',
        'app_id': application_id,
        'app_key': application_key
    }

    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers)
        response = response.json()
    
        recipes = RecipeClass.extract_from_json(response)

        save_recipe_info_to_database(recipes)


    except Exception as e:
        print(f'An error occurred, {e}')

    return render_template('recipe_list.html', recipes = recipes)






