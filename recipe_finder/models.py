from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect to db"""

    db.app = app
    db.init_app(app)



class User(db.Model):
    """user model which holds user informatino"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    
    favorites = db.relationship('Recipe', secondary='user_favorite', backref='user')

    def __repr__(self):
        return f'<id={self.id} usernmae={self.username} password={self.password} email={self.email} first_name={self.first_name} last_name={self.last_name}>'


    @classmethod
    def signup(cls, username, password, email, first_name, last_name):
        # signup user

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username = username, password = hashed_password, email = email, first_name = first_name, last_name = last_name)

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def authenticate(cls, username, password):
        # login user

        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        

class Recipe(db.Model):
    """recipe model which holds recipe information"""

    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    image = db.Column(db.String)
    url = db.Column(db.String, nullable=False)
    calories = db.Column(db.Float)
    serves = db.Column(db.Float)
    total_time = db.Column(db.Float)
    cuisine_type = db.Column(db.String)
    meal_type = db.Column(db.String)

    ingredients = db.relationship('Ingredient', secondary='recipe_ingredient', backref='recipe')
    nutrition_facts = db.relationship('Nutrition_Fact', backref='recipe')

    def __repr__(self):
        return f"<id={self.id} title={self.title} source={self.source} image={self.image} url={self.url} calories={self.calories} serves={self.serves} total_time={self.total_time} cuisine_type={self.cuisine_type} meal_type={self.meal_type}>"
    

class Nutrition_Fact(db.Model):
    """nutrition_facts model which holds nutrition fact data"""

    __tablename__ = 'nutrition_facts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String, nullable = False)
    quantity = db.Column(db.Float, nullable = False)
    unit = db.Column(db.String, nullable = False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), nullable=False)

    def __repr__(self):
        return f'<id={self.id} label={self.label} quanitity={self.quantity} unit={self.unit} recipe_id={self.recipe_id}>'



class Ingredient(db.Model):
    """ingredient model which holds ingredient name information"""

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False)

    info = db.relationship('Ingredient_Info', backref='ingredient')

    def __repr__(self):
        return f'<id={self.id} name={self.name}>'
    



class Ingredient_Info(db.Model):
    """ingredient_info model which holds more ingredient information"""

    __tablename__ = 'ingredient_info'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    text = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float)
    measure = db.Column(db.String)
    weight = db.Column(db.Float)
    food_category = db.Column(db.String)
    image = db.Column(db.String)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete='cascade'), nullable = False)

    def __repr__(self):
        return f"<id={self.id} quantity={self.quantity} measure={self.measure} weight={self.weight} food_category={self.category} image={self.image} ingredient_id={self.ingredient_id}>"
    




class Recipe_Ingredient(db.Model):
    """links together the recipe and ingredient models"""
    
    __tablename__ = 'recipe_ingredient'

    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete='cascade'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete='cascade'), primary_key=True)

    recipe = db.relationship('Recipe', backref='recipe_ingredients')
    ingredient = db.relationship('Ingredient', backref='recipe_ingredients')

    def __repr__(self):
        return f'<recipe_id={self.recipe_id} ingredient_id={self.ingredient_id}>'
    




    

class User_Favorite(db.Model):
    """links together the user with the recipe model to create a user favorite"""

    __tablename__ = 'user_favorite'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), nullable = False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id', ondelete = 'cascade'), nullable = False)

    user = db.relationship('User', backref='user_favorite')
    recipe = db.relationship('Recipe', backref='user_recipe')


    def __repr__(self):
        return f'<id={self.id} user_id={self.user_id} recipe_id={self.recipe_id}>'