from app import app
from models import db, User, Favorite, Ingredient, Recipe_Ingredient
import pdb

with app.app_context():
    db.drop_all()
    db.create_all()



   
    pdb.set_trace()


