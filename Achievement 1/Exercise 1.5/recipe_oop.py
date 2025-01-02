# defining Recipe and its attributes
class Recipe:

    # class variable that keeps track of all ingredients
    all_ingredients = set()

    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None
        self.update_all_ingredients()

    # initialization method for name and cooking_time
    def get_name(self):
        return self.name  
    
    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time   

    # method to take in variable-length ingredients
    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
    
    # getter method that returns ingredient list
    def get_ingredients(self):
        return self.ingredients   
    
    # method to determine level of recipe difficulty
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(self.ingredients) >= 4:
            self.difficulty = "Hard"

    # getter method that returns difficulty and also calls method from above ^ 
    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty
    
    # getter method that searches an ingredient and returns True/False 
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # method that goes through recipe's ingredients and add them to all ingredients from all recipes
    def update_all_ingredients(self):        
            Recipe.all_ingredients.update(self.ingredients)

    # string that prints entire recipe
    def __str__(self):
        return (
            f"Recipe: {self.name}\n"
            f"Ingredients: {', '.join(self.ingredients)}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.get_difficulty()}\n"
        )     
    
# find a recipe that contains a specific ingredient
def recipe_search(data, search_term):
        print(f"\nSearch for recipes with ingredient: {search_term}")        
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)
            else:
                print("No recipes found with that ingredient.")

# recipe objects
tea = Recipe("Tea", ["tea leaves", "sugar", "water"], 5)
coffee = Recipe("Coffee", ["coffee powder", "sugar", "water"], 5)
cake = Recipe("Cake", ["sugar", "butter", "eggs", "vanilla essence", "flour", "baking powder", "milk"], 50)
banana_smoothie = Recipe("Banana Smoothie", ["bananas", "milk", "peanut butter", "sugar", "ice cubes"], 5)

# list of recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

# print all recipes
print("--- All Recipes ---")
for recipe in recipes_list:
    print(recipe)

# search for ingredients in recipes
for ingredient in ["water", "sugar", "bananas"]:
    recipe_search(recipes_list, ingredient)


