from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect to db"""

    db.app = app
    db.init_app(app)



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.String, nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False, unique = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    
    favorites = db.relationship('Favorite', backref = 'user')

    def __repr__(self):
        return f'<id={self.id} usernmae={self.username} password={self.password} email={self.email} first_name={self.first_name} last_name={self.last_name}>'


    @classmethod
    def signup(cls, username, password, email, first_name, last_name):

        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username = username, password = hashed_password, email = email, first_name = first_name, last_name = last_name)

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def authenticate(cls, username, password):

        user = User.query.filter(User.username == username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False


class Favorite(db.Model):

    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String, nullable = False, unique = True)
    description = db.Column(db.Text)
    instruction = db.Column(db.Text)
    image_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete = 'cascade'), nullable = False)

    ingredients = db.relationship('Ingredient', secondary='recipe_ingredients', backref='favorites')



    def __repr__(self):
        return f'<id={self.id} title={self.title} description={self.description} instruction={self.instruction} user_id={self.user_id}>'
    

class Ingredient(db.Model):

    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String, nullable = False, unique = True)

    def __repr__(self):
        return f'<id={self.id} name={self.name}>'



class Recipe_Ingredient(db.Model):
    
    __tablename__ = 'recipe_ingredients'

    recipe_id = db.Column(db.Integer, db.ForeignKey('favorites.id', ondelete='cascade'), primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id', ondelete ='cascade'), primary_key=True)
    quantity = db.Column(db.Float, nullable = False)
    unit = db.Column(db.String)

    recipe = db.relationship('Favorite', backref='recipe_ingredients')
    ingredient = db.relationship('Ingredient', backref='recipe_ingredients')

    def __repr__(self):
        return f'<recipe_id={self.recipe_id} ingredient_id={self.ingredient_id} quantity={self.quantity} unit={self.unit}>'