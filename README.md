# Project Title/Description

The goal of this project was to create an application that allows a user to search for recipes based on ingredients they want the recipe to contain. This application allows a user to enter ingredients, which will then create a query that will fetch all relevant recipes based on the ingredients enterred. 


# Deployement Link

[Project Link](https://recipe-finder-5ji5.onrender.com)


# Technologies Used 

Python/Flask, PostgreSQL, SQLAlchemy, Jinja, RESTful APIs, WTForms, Bcrypt, HTML, CSS, Bootstrap, [API Link](https://developer.edamam.com/edamam-recipe-api)


# Database Schema

[Database Schema Link](https://github.com/pkotis32/Capstone1/blob/main/Database%20Schema.drawio.png)


# Installation instructions

The first step to install the project is to clone the repository from github on a local machine by typing 'git clone (git_repo_url)'. The next step would be to install python3 if it isn't already installed. This can be done a couple of ways: one method is to download it directly from python's own webpage, or it can be installed using homebrew on a mac device using the command 'brew install python'. Next, a virtual environment should be created using the command 'python -m venv venv'. Then all the dependencies should be installed from the requirements.txt file with the command 'pip install -r requirements.txt'. Once all the dependencies are installed, the next step is to get started with the free plan for the recipe search product within the api linked above. Once this is done, you will be given an application_id and an application_key, which should be inserted in a .env file exactly as they are spelled here. This should set everything up so that the application is ready, the only thing left is to start a server which can be done using the command 'flask run'. 


# Usage/Features

This application will first ask the user to login/signup. Once the user has done so, they will have access to the recipe finder search bar where they should enter desired ingredients for their recipe to have. The user can either click on many ingredients that will be populated in the dropdown area to add to their query, or they can type an ingredient from scratch and click enter, which will add it to the list of ingredients. Once the user clicks on the search button, a list of relevant recipes should be returned. The user will be able to click on each recipe that is returned to further explore the recipe details. The user will be able to access the original recipe link, as well as information about the ingredients used and the nutrition facts associated with the recipe. Additionally, the user is allowed to favorite a recipe to add it to a favorite list, that will be saved every time the user is logged in. 


# Contributing

Other users can contribute to this project a couple different ways. I think one of the biggest issues I see is that it takes a long time for the recipes to be returned after a user searches for them. The reason for this is that when search button is clicked, all of the recipes are saved to a database as well as all of their infromation such as ingredients and nutrition facts. I have tried to make the commits more efficient by not commiting after each addition of a recipe ingredient or nutrition information and istead to commit once they have all been added to the session. Still, I believe improvements can be made, which I would love to have people contribute to. Possibly, instead of saving all the recipe information to the database for every recipe that is returned, maybe instead it would be better to save just the general recipe information initially, but then once a user clicks on a recipe to see further detail about it, to then make an another api request to retrieve the further details instead of query the information that was already save to the database. Additionally, I am not the best with visual appearance, so others can definetely contribute to enhace the visuals of the application. 


# Contact Info

Name: Phillip Kotis
Email: kotisphillip@gmail.com
