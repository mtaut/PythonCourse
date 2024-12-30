import pickle

# function to print attributes of recipe
def display_recipe(recipe):
    print("Recipe: " + recipe["name"])
    print("Cooking Time (min): " + str(recipe["cooking_time"]))
    print("Ingredients: ")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty: " + recipe["difficulty"])

#function to search for ingredients in data
def search_ingredient(data):
    available_ingredients = enumerate(data["all_ingredients"])
    all_ingredients = list(available_ingredients)
    print("Ingredients list: ")
    
    for index, ingredient in all_ingredients:
        print(index, ingredient)

    # user inputs number to retrieve ingredient
    try:
        num = int(input("Enter the number of an ingredient to search: "))
        ingredient_searched = all_ingredients[num][1]
        print("Searching for recipes with that ingredient...")

    # error warning if input is incorrect
    except ValueError:
        print("Oops! Please enter a number.")

    # will go through each and display each recipe that contains given ingredient
    else:
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                print(recipe)

# asking user for name of file that contains recipe data
filename = input("Enter the name of the file that contains your recipe: ")

# this will open the file
try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File opened successfully.")

# error for when file is not found
except FileNotFoundError:
    print("File cannot be found. Please try again.")

else:
    file.close()
    search_ingredient(data) 