from pprint import pformat
import os

import requests
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import db, User, Allergy, UserAllergy, Plan, UserDiet, Diet, RecipePlan, Recipe, connect_to_db

import random

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"

EDAMAM_RECIPE_SEARCH_APPLICATION_ID = os.environ.get('EDAMAM_RECIPE_SEARCH_APPLICATION_ID')
EDAMAM_RECIPE_SEARCH_APPLICATION_KEY = os.environ.get('EDAMAM_RECIPE_SEARCH_APPLICATION_KEY')

EDAMAM_URL = "https://api.edamam.com/search"

# @app.route("/show-recipe")
# def show_recipe():
# 	"""Show the recipe"""

# 	recipe_name = 'chicken' 

# 	payload = { 'q': recipe_name,
# 				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
# 				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }
	
# 	response = requests.get(EDAMAM_URL, params=payload)
# 	data = response.json()
	
# 	if response.ok:
# 		recipe = data["hits"][0]["recipe"]["dietLabels"]

# 	return render_template("recipe.html", results=recipe)

@app.route("/")
def homepage():
	"""Show homepage"""

	#if logged in - flash message: Succesfully logged in
	#show options in form(nav menu):
		# go to preferences 
		# go to make a meal from your fridge

	#if NOT logged in - flash message: You are not logged in
	# if "user_id" in session:
	# 	print(session)
		# show logout button


	return render_template("homepage.html")

@app.route("/register")
def register():
	"""Show register form"""

	return render_template("register_page.html")



@app.route("/register", methods=["POST"])
def register_form():
	"""Register user if not in the database"""

	fname=request.form.get("fname")
	lname=request.form.get("lname")
	email=request.form.get("email")
	password=request.form.get("password")

	new_user = User(fname=fname, lname=lname, email=email, password=password)
	user = User.query.filter_by(fname=fname, lname=lname, email=email, password=password).first()

	if user is not None:
		flash(f"User {user.fname} {user.lname} already exists in our database!")
		return redirect("/")
	else:
		db.session.add(new_user)

	db.session.commit()
	flash(f"User {new_user.fname} {new_user.lname} succesfully added to the database!")

	session["new_user_id"] = new_user.user_id

	return redirect("/allergy")

@app.route("/allergy")
def show_allergy_form():
	"""Redirect from homepage form. Display checkbox with set of allergies."""

	return render_template("allergies.html")


@app.route("/allergy", methods=["POST"])
def handle_allergy_form():
	"""Handle user's allergies."""

######################### maybe MORE ELEGANT??
	allergens = []

	gluten = request.form.get("allergen1")
	allergens.append(gluten)

	wheat = request.form.get("allergen2")
	allergens.append(wheat)

	tree_nut = request.form.get("allergen3")
	allergens.append(tree_nut)

	shellfish = request.form.get("allergen4")
	allergens.append(shellfish)

	soy = request.form.get("allergen5")
	allergens.append(soy)

	user_id = session["new_user_id"]

	for i, allergen in enumerate(allergens):
  		if allergen:
  			allergy_id = i + 1
  			user_allergy = UserAllergy(user_id=user_id, allergy_id=allergy_id)
  			db.session.add(user_allergy)

	db.session.commit()

	return redirect("/options")
	# make the user page more personal

@app.route("/options")
def show_options_form():
	"""Redirect from the preferences form. Display checkbox with diet options."""

	return render_template("options_diet.html")

@app.route("/options", methods=["POST"])
def handle_options_form():
	"""Handle user's diet options."""
	
	diet_options = []

	alcohol_free = request.form.get("option1")
	diet_options.append(alcohol_free)

	balanced = request.form.get("option2")
	diet_options.append(balanced)

	high_protein = request.form.get("option3")
	diet_options.append(high_protein)

	low_carb = request.form.get("option4")
	diet_options.append(low_carb)

	low_fat = request.form.get("option5")
	diet_options.append(low_fat)

	peanut_free = request.form.get("option6")
	diet_options.append(peanut_free)

	sugar_conscious = request.form.get("option7")
	diet_options.append(sugar_conscious)

	tree_nut_free = request.form.get("option8")
	diet_options.append(tree_nut_free)

	vegan = request.form.get("option9")
	diet_options.append(vegan)

	vegetarian = request.form.get("option10")
	diet_options.append(vegetarian)

	user_id = session["new_user_id"]

	for i, diet_option in enumerate(diet_options):
		if diet_option:
			diet_id = i + 1
			user_diet = UserDiet(user_id=user_id, diet_id=diet_id)
			db.session.add(user_diet)

	db.session.commit()

	return redirect("/login")


@app.route("/login")
def login():
	"""Show login form."""

	return render_template("login_page.html")

@app.route("/login", methods=["POST"])
def login_form():
	"""Login user."""

	email=request.form["email"]
	password=request.form["password"]

	user = User.query.filter_by(email=email).first()

	if not user:
		flash("Not such user.")
		return redirect("/login")

	elif user.password != password:
		flash("Incorrect password!")
		return redirect("/login")

	# elif "user_id" in session:
	# 	flash("Other user already logged in!")
	# 	return redirect("/")

	session["user_id"] = user.user_id
	# flash("User logged in!")
	# return redirect("/")

	# return redirect(f"/users/{new_user.user_id}")
	flash(f"User succesfully logged in.")
	return redirect("/plan")
	#in version 2.0 add option to go whenever


@app.route("/plan")
def user_options():
	"""Show users options"""

	return render_template("plan.html")

@app.route("/plan", methods=["POST"])
def user_breakfast_choices():
	"""Get the preferences from the form, search the options for breakfast."""

	user_id = session["user_id"]

	plan_name = request.form.get("plan_name")
	calories = request.form.get("calories")
	carbohydrates = request.form.get("carbohydrates")
	fat = request.form.get("fat")
	protein = request.form.get("protein")

	new_plan = Plan(plan_name=plan_name, user_id=user_id, calories=calories, carbohydrates=carbohydrates, fat=fat, protein=protein)
	db.session.add(new_plan)
	db.session.commit()

	#make a helper function

	#why calories is str??
	# calories = float(calories)

# 	return render_template("user_plan.html", calories=calories, carbohydrates=carbohydrates, fat=fat, protein=protein)
# 	# render to some recipes

# @app.route("/breakfast")
# def search_breakfast():
# 	"""Search breakfast which calories are 35% of user's daily preference."""

# 	# calories = request.form.get("calories")
# 	# carbohydrates = request.form.get("carbohydrates")
# 	# fat = request.form.get("fat")
# 	# protein = request.form.get("protein")

# 	user_id = session["user_id"]

	#change the allergy as the diet or change your mind :)
	user_allergies = UserAllergy.query.filter_by(user_id=user_id).all()
	allergies = []
	for user_allergy in user_allergies:
		allergy_name = Allergy.query.filter_by(allergy_id=user_allergy.allergy_id).first()
		allergies.append(allergy_name.allergy_name)


	diets = UserDiet.query.filter_by(user_id=user_id).all()
	user_diets = []
	for diet in diets:
		diet_name = Diet.query.filter_by(diet_id=diet.diet_id).first()
		user_diets.append(diet_name.diet_name)
		#diet_name is an object and diet name is an attribute


	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()
	#what if multiple plans?
	calories = plan.calories
	carbohydrates = plan.carbohydrates
	fat = plan.fat
	protein = plan.protein

	breakfast_limit_calories = calories * 0.35
	breakfast_limit_carbohydrates = carbohydrates * 0.35
	breakfast_limit_fat = fat * 0.35
	breakfast_limit_protein = protein * 0.35

	breakfast = "breakfast"

	payload = { 'q': breakfast,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }

	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()

	results = []

	if response.ok:
		for n in range(5):
			# not sure about the range - check later
			recipe = {}

			recipe_serving = data["hits"][n]["recipe"]["yield"]

			recipe_calories = data["hits"][n]["recipe"]["calories"]
			recipe_carbohydrates = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
			recipe_fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
			recipe_protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]	

			recipe_cautions = data["hits"][n]["recipe"]["cautions"]
			recipe_labels_1 = data["hits"][n]["recipe"]["dietLabels"]
			recipe_labels = data["hits"][n]["recipe"]["healthLabels"]

			for rec_lab_1 in recipe_labels_1:
				recipe_labels.append(rec_lab_1)

			calories_per_yield = recipe_calories/recipe_serving
			carbohydrates_per_yield = recipe_carbohydrates/recipe_serving
			fat_per_yield = recipe_fat/recipe_serving
			protein_per_yield = recipe_protein/recipe_serving

			# below is ok, dont worry!!!
			if (calories_per_yield > breakfast_limit_calories) or (carbohydrates_per_yield > breakfast_limit_carbohydrates) or (fat_per_yield > breakfast_limit_fat) or (protein_per_yield > breakfast_limit_protein):
				continue

			has_allergy = False

			for allergy in allergies:
				if allergy in recipe_cautions:
					has_allergy = True

			has_diet_label = False
			count = 0
			for user_diet in user_diets:
				if user_diet in recipe_labels:
					count += 1
			if count == len(user_diets):
				has_diet_label = True

			if has_allergy == False and has_diet_label == True:
				recipe_name = data["hits"][n]["recipe"]["label"]
				recipe["recipe_name"] = recipe_name

				recipe_url = data["hits"][n]["recipe"]["uri"]
				recipe["recipe_url"] = recipe_url
				
				recipe_image = data["hits"][n]["recipe"]["image"]
				recipe["recipe_image"] = recipe_image

				directions = data["hits"][n]["recipe"]["url"]
				recipe["directions"] = directions

				servings = data["hits"][n]["recipe"]["yield"]
				recipe["servings"] = servings

				calories = data["hits"][n]["recipe"]["calories"]
				recipe["calories"] = calories

				carbohydrates = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
				recipe["carbohydrates"] = carbohydrates

				fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
				recipe["fat"] = fat

				protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]
				recipe["protein"] = protein

				results.append(recipe)

	return render_template("display_breakfast.html", results=results)


@app.route("/add-breakfast", methods=["POST"])
def add_breakfast_to_db():
	"""Add breakfast to the database."""

	user_id = session["user_id"]

	recipe_name = request.form.get("recipe_name")
	recipe_url = request.form.get("recipe_url")
	recipe_image = request.form.get("recipe_image")
	directions = request.form.get("directions")
	servings = request.form.get("servings")
	calories = request.form.get("calories")
	carbohydrates = request.form.get("carbohydrates")
	fat = request.form.get("fat")
	protein = request.form.get("protein")

	recipe_obj = Recipe(recipe_name=recipe_name, recipe_url=recipe_url, recipe_image=recipe_image, directions=directions, servings=servings, calories=calories, carbohydrates=carbohydrates, fat=fat, protein=protein)
	db.session.add(recipe_obj)
	db.session.commit()

	recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()

	recipe_plan_obj = RecipePlan(plan_id=plan.plan_id, recipe_id=recipe.recipe_id)
	db.session.add(recipe_plan_obj)
	db.session.commit()

	return redirect ("/display-lunch")
# 
# copy for dinner and lunch
# display to the user all recipes with the links
# display shopping list to user

@app.route("/display-lunch")
def user_preferences():
	"""Get the preferences from the form, search the options for lunch."""
	pass

	user_id = session["user_id"]

	user_allergies = UserAllergy.query.filter_by(user_id=user_id).all()
	allergies = []
	for user_allergy in user_allergies:
		allergy_name = Allergy.query.filter_by(allergy_id=user_allergy.allergy_id).first()
		allergies.append(allergy_name.allergy_name)


	diets = UserDiet.query.filter_by(user_id=user_id).all()
	user_diets = []
	for diet in diets:
		diet_name = Diet.query.filter_by(diet_id=diet.diet_id).first()
		user_diets.append(diet_name.diet_name)
		#diet_name is an object and diet name is an attribute


	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()

	#add a form to select plan
	calories = plan.calories
	carbohydrates = plan.carbohydrates
	fat = plan.fat
	protein = plan.protein


	# 35+25+40
	lunch_limit_calories = calories * 0.25
	lunch_limit_carbohydrates = carbohydrates * 0.25
	lunch_limit_fat = fat * 0.25
	lunch_limit_protein = protein * 0.25

	lunch = "lunch"
	#add a form to get a word

	payload = { 'q': lunch,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }

	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()

	results = []

	if response.ok:
		for n in range(5):
			recipe = {}

			recipe_serving = data["hits"][n]["recipe"]["yield"]

			recipe_calories = data["hits"][n]["recipe"]["calories"]
			recipe_carbohydrates = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
			recipe_fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
			recipe_protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]	

			recipe_cautions = data["hits"][n]["recipe"]["cautions"]
			recipe_labels_1 = data["hits"][n]["recipe"]["dietLabels"]
			recipe_labels = data["hits"][n]["recipe"]["healthLabels"]

			for rec_lab_1 in recipe_labels_1:
				recipe_labels.append(rec_lab_1)

			calories_per_yield = recipe_calories/recipe_serving
			carbohydrates_per_yield = recipe_carbohydrates/recipe_serving
			fat_per_yield = recipe_fat/recipe_serving
			protein_per_yield = recipe_protein/recipe_serving

	# 		# below is ok, dont worry!!!
			if (calories_per_yield > lunch_limit_calories) or (carbohydrates_per_yield > lunch_limit_carbohydrates) or (fat_per_yield > lunch_limit_fat) or (protein_per_yield > lunch_limit_protein):
				continue

			has_allergy = False

			for allergy in allergies:
				if allergy in recipe_cautions:
					has_allergy = True

			has_diet_label = False
			count = 0
			for user_diet in user_diets:
				if user_diet in recipe_labels:
					count += 1
			if count == len(user_diets):
				has_diet_label = True

			if has_allergy == False and has_diet_label == True:
				recipe_name = data["hits"][n]["recipe"]["label"]
				recipe["recipe_name"] = recipe_name

				recipe_url = data["hits"][n]["recipe"]["uri"]
				recipe["recipe_url"] = recipe_url
				
				recipe_image = data["hits"][n]["recipe"]["image"]
				recipe["recipe_image"] = recipe_image

				directions = data["hits"][n]["recipe"]["url"]
				recipe["directions"] = directions

				servings = data["hits"][n]["recipe"]["yield"]
				recipe["servings"] = servings

				calories = data["hits"][n]["recipe"]["calories"]
				recipe["calories"] = calories

				carbohydrates = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
				recipe["carbohydrates"] = carbohydrates

				fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
				recipe["fat"] = fat

				protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]
				recipe["protein"] = protein

				results.append(recipe)

	return render_template("display_lunch.html", results=results)

@app.route("/add-lunch", methods=["POST"])
def add_lunch_to_db():
	"""Add lunch to the database."""

	user_id = session["user_id"]

	recipe_name = request.form.get("recipe_name")
	recipe_url = request.form.get("recipe_url")
	recipe_image = request.form.get("recipe_image")
	directions = request.form.get("directions")
	servings = request.form.get("servings")
	calories = request.form.get("calories")
	carbohydrates = request.form.get("carbohydrates")
	fat = request.form.get("fat")
	protein = request.form.get("protein")

	recipe_obj = Recipe(recipe_name=recipe_name, recipe_url=recipe_url, recipe_image=recipe_image, directions=directions, servings=servings, calories=calories, carbohydrates=carbohydrates, fat=fat, protein=protein)
	db.session.add(recipe_obj)
	db.session.commit()

	recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()

	recipe_plan_obj = RecipePlan(plan_id=plan.plan_id, recipe_id=recipe.recipe_id)
	db.session.add(recipe_plan_obj)
	db.session.commit()

	return redirect ("/display-dinner")


@app.route("/display-dinner")
def user_dinner_preferences():
	"""Get the preferences from the form, search the options for dinner."""
	pass

	user_id = session["user_id"]

	user_allergies = UserAllergy.query.filter_by(user_id=user_id).all()
	allergies = []
	for user_allergy in user_allergies:
		allergy_name = Allergy.query.filter_by(allergy_id=user_allergy.allergy_id).first()
		allergies.append(allergy_name.allergy_name)


	diets = UserDiet.query.filter_by(user_id=user_id).all()
	user_diets = []
	for diet in diets:
		diet_name = Diet.query.filter_by(diet_id=diet.diet_id).first()
		user_diets.append(diet_name.diet_name)
		#diet_name is an object and diet name is an attribute


	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()

	#add a form to select plan
	calories = plan.calories
	carbohydrates = plan.carbohydrates
	fat = plan.fat
	protein = plan.protein


	# 35+25+40
	dinner_limit_calories = calories * 0.4
	dinner_limit_carbohydrates = carbohydrates * 0.4
	dinner_limit_fat = fat * 0.4
	dinner_limit_protein = protein * 0.4

	dinner = "dinner"
	#add a form to get a word

	payload = { 'q': dinner,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }

	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()

	results = []

	if response.ok:
		for n in range(5):
			recipe = {}

			recipe_serving = data["hits"][n]["recipe"]["yield"]

			recipe_calories = data["hits"][n]["recipe"]["calories"]
			recipe_carbohydrates = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
			recipe_fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
			recipe_protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]	

			recipe_cautions = data["hits"][n]["recipe"]["cautions"]
			recipe_labels_1 = data["hits"][n]["recipe"]["dietLabels"]
			recipe_labels = data["hits"][n]["recipe"]["healthLabels"]

			for rec_lab_1 in recipe_labels_1:
				recipe_labels.append(rec_lab_1)

			calories_per_yield = recipe_calories/recipe_serving
			carbohydrates_per_yield = recipe_carbohydrates/recipe_serving
			fat_per_yield = recipe_fat/recipe_serving
			protein_per_yield = recipe_protein/recipe_serving

	# 		# below is ok, dont worry!!!
			if (calories_per_yield > dinner_limit_calories) or (carbohydrates_per_yield > dinner_limit_carbohydrates) or (fat_per_yield > dinner_limit_fat) or (protein_per_yield > dinner_limit_protein):
				continue

			has_allergy = False

			for allergy in allergies:
				if allergy in recipe_cautions:
					has_allergy = True

			has_diet_label = False
			count = 0
			for user_diet in user_diets:
				if user_diet in recipe_labels:
					count += 1
			if count == len(user_diets):
				has_diet_label = True

			if has_allergy == False and has_diet_label == True:
				recipe_name = data["hits"][n]["recipe"]["label"]
				recipe["recipe_name"] = recipe_name

				recipe_url = data["hits"][n]["recipe"]["uri"]
				recipe["recipe_url"] = recipe_url
				
				recipe_image = data["hits"][n]["recipe"]["image"]
				recipe["recipe_image"] = recipe_image

				directions = data["hits"][n]["recipe"]["url"]
				recipe["directions"] = directions

				servings = data["hits"][n]["recipe"]["yield"]
				recipe["servings"] = servings

				calories = data["hits"][n]["recipe"]["calories"]
				recipe["calories"] = calories

				carbohydrates = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
				recipe["carbohydrates"] = carbohydrates

				fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
				recipe["fat"] = fat

				protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]
				recipe["protein"] = protein

				results.append(recipe)

	return render_template("display_dinner.html", results=results)

@app.route("/add-dinner", methods=["POST"])
def add_dinner_to_db():
	"""Add dinner to the database."""

	user_id = session["user_id"]

	recipe_name = request.form.get("recipe_name")
	recipe_url = request.form.get("recipe_url")
	recipe_image = request.form.get("recipe_image")
	directions = request.form.get("directions")
	servings = request.form.get("servings")
	calories = request.form.get("calories")
	carbohydrates = request.form.get("carbohydrates")
	fat = request.form.get("fat")
	protein = request.form.get("protein")

	recipe_obj = Recipe(recipe_name=recipe_name, recipe_url=recipe_url, recipe_image=recipe_image, directions=directions, servings=servings, calories=calories, carbohydrates=carbohydrates, fat=fat, protein=protein)
	db.session.add(recipe_obj)
	db.session.commit()

	recipe = Recipe.query.filter_by(recipe_name=recipe_name).first()
	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()

	recipe_plan_obj = RecipePlan(plan_id=plan.plan_id, recipe_id=recipe.recipe_id)
	db.session.add(recipe_plan_obj)
	db.session.commit()

	return redirect("/display-plan")
	# redirect to the whole selected plan

@app.route("/display-plan")
def show_web_with_whole_plan():
	"""Display the whole plan for a day."""
	#display with the 

	user_id = session["user_id"]
	plan = Plan.query.filter_by(user_id=user_id).order_by(Plan.plan_id.desc()).first()
	recipe_plan_lst = RecipePlan.query.filter_by(plan_id=plan.plan_id).all()

	results = []
	for recipe_plan_obj in recipe_plan_lst:
		recipe = {}
		recipe_obj = Recipe.query.filter_by(recipe_id=recipe_plan_obj.recipe_id).first()
		print(recipe_obj)
		recipe["recipe_name"] = recipe_obj.recipe_name
		recipe["recipe_image"] = recipe_obj.recipe_image
		print(recipe)
		print(type(recipe))
		print("gosia")
		results.append(recipe)
		print("!!!!!!!!!!!!!!!!!!!!!!!!!")
		print(results)
	print("oleole")
	print(results)


	# for recipe_lst in recipes_lst:
	# 	# recipe["recipe_name"] = recipes_lst[recipe_lst].recipe_id
	# 	# recipe["recipe_image"] = recipes_lst[recipe_lst].recipe_image
	# 	print(recipes_lst)
	# 	print(type(recipes_lst))
	# 	print("gosia")

	# 	results.append(recipe)
	# print("oleole")
	# print(results)

	return render_template("display_plan.html", results=results)
	# return render_template("homepage.html")



































#########query just 1 thing - how can I query multiple? FUNCTION MAKE A MEAL FROM YOUR FRIDGE################

@app.route("/make-a-meal-from-fridge")
def show_ing_form():
	"""Display checkbox with ingredients options."""

	return render_template("make_a_meal.html")

@app.route("/make-a-meal-from-fridge", methods = ["POST"])
def make_a_meal_from_fridge():
	"""Get user ingredients and query to API for available recipes."""

	chicken = request.form.get("option1")
	tomato = request.form.get("option2")
	avocado = request.form.get("option3")
	onion = request.form.get("option4")
	milk = request.form.get("option5")
	ginger = request.form.get("option6")
	oregano = request.form.get("option7")
	pepper = request.form.get("option8")
	parsley = request.form.get("option9")
	potato = request.form.get("option10")

	ingredients = []
	ingredients.append(chicken)
	ingredients.append(tomato)
	ingredients.append(avocado)
	ingredients.append(milk)
	ingredients.append(ginger)
	ingredients.append(oregano)
	ingredients.append(pepper)
	ingredients.append(parsley)
	ingredients.append(potato)
	# can I do this more elegant?

	results = []

	meal = ""
	for ing in ingredients:
		if ing != None:
			meal += ing + ","

	payload = { 'q': meal,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }

	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()


	if response.ok:
		for n in range(5):
			recipe = {}
			recipe_url = data["hits"][n]["recipe"]["url"]
			recipe["recipe_url"] = recipe_url

			recipe_image = data["hits"][n]["recipe"]["image"]
			recipe["recipe_image"] = recipe_image

			recipe_name = data["hits"][n]["recipe"]["label"]
			recipe["recipe_name"] = recipe_name

			results.append(recipe)

#later: add photo to the recipe
#later: do the interactive link

	return render_template("make_a_meal_display_recipes.html", results=results)


@app.route("/logout")
def logout():
    """Log out user."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")

	# add a button Log Out
	# jquery




@app.route("/")
def create_meal_plan():
	"""Based on users preferences search recipes."""

	#the essence of the app
	#how to get the recipes from db and sum (calories, macros,allergies)
	#1. get all the recipes from db where allergies AND health label is the same as user`s preference
	#2. Think about dinner/breakfast/lunch - do they have labels??
	#3. Proportion of calories - br-lunch-dinner????
	#....what will be next?
	# sum a bunch of br+lunch+dinner
	#check if sum is equal to users preferences

	pass


@app.route("/make-a-meal-from-fridge")
def make_a_meal():
	"""Make a meal from your fridge"""

	# make an html form
	# put a checkbox with the ingredients
	# put a submit button
	# redirect to the route cooking route

	pass

@app.route("/cook-a-meal-from-fridge")
def cook_a_meal():

	#get ingredients from the form
	#search recepies from the database which have those ingredients
	#list the recipes
	#redirect to a form which listing recepies

	pass

@app.route("/show-a-meal-from-fridge")
def show_meal():

	#I am not sure if I need this route
	# make a form listing the recipes
	#after clicking favorite recipe recirect to recipe url
	#recipe url is in database as directions

	pass

if __name__ == "__main__":
	app.debug = True
	app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
	DebugToolbarExtension(app)
	connect_to_db(app)
    # db.create_all()
	app.run(host='0.0.0.0', port=5000)