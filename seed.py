from sqlalchemy import func
import json 
# do I need json?
import requests
import os

from server import app

EDAMAM_RECIPE_SEARCH_APPLICATION_ID = os.environ.get('EDAMAM_RECIPE_SEARCH_APPLICATION_ID')
EDAMAM_RECIPE_SEARCH_APPLICATION_KEY = os.environ.get('EDAMAM_RECIPE_SEARCH_APPLICATION_KEY')

EDAMAM_URL = "https://api.edamam.com/search"

######################to do:::
def get_recipe_attributes_db(name):
	"""Get the recipes' attributes."""


	payload = { 'q': name,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }
	
	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()
	# import pdb; pdb.set_trace()

	set_of_recipes = []

	

	if response.ok:
		for n in range(2):
			recipe = {}
			recipe_obj = Recipe(recipe_url=data["hits"][n]["recipe"]["url"],
								recipe_image=data["hits"][n]["recipe"]["image"],






								)

			# recipe["recipe"] = data["hits"][n]["recipe"]["label"]
			# recipe_obj.recipe = data["hits"][n]["recipe"]["label"]
			# set_of_recipes.append(recipe)

			recipe_url = data["hits"][n]["recipe"]["url"]
			set_of_recipes.append(recipe_url)

			recipe_image = data["hits"][n]["recipe"]["image"]
			set_of_recipes.append(recipe_image)

			directions = data["hits"][n]["recipe"]["url"]
			set_of_recipes.append(directions)

			servings = data["hits"][n]["recipe"]["yield"]
			set_of_recipes.append(servings)

			calories = calories = float(data["hits"][1]["recipe"]["calories"])
			set_of_recipes.append(calories)
			
			carbs = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
			set_of_recipes.append(carbs)
			
			fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
			set_of_recipes.append(fat)
			
			protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]			
			set_of_recipes.append(protein)

			db.session.add(recipe_obj)

		db.session.commit()

	print(set_of_recipes)

	return set_of_recipes

def get_recipe_attributes(name):
	"""Get the recipes' attributes."""


	payload = { 'q': name,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }
	
	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()
	# import pdb; pdb.set_trace()

	set_of_recipes = []

	

	if response.ok:
		for n in range(2):	
			recipe["recipe"] = data["hits"][n]["recipe"]["label"]
			set_of_recipes.append(recipe)

			recipe_url = data["hits"][n]["recipe"]["url"]
			set_of_recipes.append(recipe_url)

			recipe_image = data["hits"][n]["recipe"]["image"]
			set_of_recipes.append(recipe_image)

			directions = data["hits"][n]["recipe"]["url"]
			set_of_recipes.append(directions)

			servings = data["hits"][n]["recipe"]["yield"]
			set_of_recipes.append(servings)

			calories = calories = float(data["hits"][1]["recipe"]["calories"])
			set_of_recipes.append(calories)
			
			carbs = data["hits"][n]["recipe"]["totalNutrients"]["CHOCDF"]["quantity"]
			set_of_recipes.append(carbs)
			
			fat = data["hits"][n]["recipe"]["totalNutrients"]["FAT"]["quantity"]
			set_of_recipes.append(fat)
			
			protein = data["hits"][n]["recipe"]["totalNutrients"]["PROCNT"]["quantity"]			
			set_of_recipes.append(protein)

	print(set_of_recipes)

	return set_of_recipes


def print_recipe_to_textfile(set_of_recipes):
	"""Print the recipe's attributes to the text file"""
	
	set_of_recipes = str(set_of_recipes)

	f = open("./seed_data/database.txt", "a")
	f.write(set_of_recipes)
	f.write("\n")
	f.write("\n")
	f.close() #not sure about closing




set_of_recipes = get_recipe_attributes('breakfast')
print_recipe_to_textfile(set_of_recipes)

set_of_recipes = get_recipe_attributes('lunch')
print_recipe_to_textfile(set_of_recipes)

set_of_recipes = get_recipe_attributes('dinner')
print_recipe_to_textfile(set_of_recipes)


############################################### up is working! ###################################



def get_recipe_labels(name):
	"""Get the recipes' labels."""

	payload = { 'q': name,
				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }
	
	response = requests.get(EDAMAM_URL, params=payload)
	data = response.json()

	set_of_labels = []

	if response.ok:
		for n in range(2):
			recipe = data["hits"][n]["recipe"]["label"]
			set_of_labels.append(recipe)

			recipe_url = data["hits"][n]["recipe"]["dietLabels"]
			set_of_labels.append(recipe_url)

			recipe_image = data["hits"][n]["recipe"]["healthLabels"]
			set_of_labels.append(recipe_image)

	print(set_of_labels)

	return set_of_labels


def print_labels_to_textfile(set_of_labels):
	"""Print the labels to the text file"""
	
	set_of_labels = str(set_of_labels)

	f = open("./seed_data/labels.txt", "a")
	f.write(set_of_labels)
	f.write("\n")
	f.write("\n")
	f.close()


# set_of_labels = get_recipe_labels('breakfast')
# print_labels_to_textfile(set_of_labels)

# set_of_labels = get_recipe_labels('lunch')
# print_labels_to_textfile(set_of_labels)

# set_of_labels = get_recipe_labels('dinner')
# print_labels_to_textfile(set_of_labels)



################# up is tested ######################################


# def get_recipe_cautions(name):
# 	"""Get the recipes' cautions."""

# 	payload = { 'q': name,
# 				'app_id': EDAMAM_RECIPE_SEARCH_APPLICATION_ID,
# 				'app_key': EDAMAM_RECIPE_SEARCH_APPLICATION_KEY }
	
# 	response = requests.get(EDAMAM_URL, params=payload)
# 	data = response.json()

# 	set_of_cautions = []

# 	if response.ok:
# 		for n in range(2):
# 			recipe = data["hits"][n]["recipe"]["label"]
# 			set_of_cautions.append(recipe)

# 			recipe = data["hits"][n]["recipe"]["cautions"]
# 			set_of_cautions.append(recipe)

# 	print(set_of_cautions)

# 	return set_of_cautions

# def print_cautions_to_textfile(set_of_lcautions):
# 	"""Print the cautions to the text file"""
	
# 	set_of_cautions = str(set_of_cautions)

# 	f = open("./seed_data/cautions.txt", "a")
# 	f.write(set_of_cautions)
# 	f.write("\n")
# 	f.write("\n")
# 	f.close() #not sure about closing



# set_of_recipes = get_recipe_attributes('breakfast')
# print_recipe_to_textfile(set_of_recipes)

# set_of_recipes = get_recipe_attributes('lunch')
# print_recipe_to_textfile(set_of_recipes)

# set_of_recipes = get_recipe_attributes('dinner')
# print_recipe_to_textfile(set_of_recipes)