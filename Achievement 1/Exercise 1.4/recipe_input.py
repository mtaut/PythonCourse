import pickle

# defining function to take a recipe from user
def take_recipe():
    name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (min): "))
    ingredients = input("Enter the recipe ingredients separated by a comma: ").split(', ')
    difficulty = calc_difficulty(cooking_time, ingredients)

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }

    return recipe

# defining difficulty of recipe
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermidiate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"

    return difficulty
    
# load file entered from user    
file_name = input("Enter a file name to open: ")

try:
    file = open(file_name, "rb")
    data = pickle.load(file)
    print("File opened successfully.")

# if file entered from user not found a new dictionary will be created    
except FileNotFoundError:
    print("File doesn't exist. Creating a new file.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

#if other errors occur completes same operation as above    
except:
    print("An unknown error has occured. One moment, please.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }
else:
    file.close()

# creates two separate dictionaries from extracted values of "recipes_list" and "all_ingredients"  
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# user prompt
n = int(input("How many recipes would you like to enter? "))

for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in all_ingredients:
            all_ingredients.append(ingredient)

        recipes_list.append(recipe)
        print("Recipe added successfully.")

# this is gathering the updated "recipes_list" and "all_ingredients" into dictionary
data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

# opens binary file and saves data to it
updated_file = open(file_name, "wb")
pickle.dump(data, updated_file)
updated_file.close()
print("Recipe has been updated.")