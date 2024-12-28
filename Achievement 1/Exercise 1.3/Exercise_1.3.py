recipes_list = []
ingredients_list=[]

# recipe function
def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the amount of cooking time, in minutes: "))
    ingredients = input("Enter ingredients separated by commas: ").split(',')
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

n = int(input("How many recipes would you like to enter? "))

# for loop that returns recipe in a dictionary
for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)

    recipes_list.append(recipe)

# for loop that iterates through recipe_list to determine difficulty based on number of ingredients and cooking time
for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Hard"

# displaying recipe format
for recipe in recipes_list:
    print("Recipe: ", recipe["name"])
    print("Cooking Time (minutes): ", recipe["cooking_time"])
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: ", recipe["difficulty"])

# sorting all ingredients from recipes alphabetically
print("n\Ingredients Available Across All Recipes: ")
for ingredient in sorted(ingredients_list):
    print(ingredient)