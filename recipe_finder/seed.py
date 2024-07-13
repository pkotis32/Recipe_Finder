from app import app
from models import db, Ingredient, Recipe, Recipe_Ingredient
import pdb

with app.app_context():
    db.drop_all()
    db.create_all()





