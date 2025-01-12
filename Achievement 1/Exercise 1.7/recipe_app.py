# import packages and methods
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker

# create engine object to connect SQLAlchemy to database
engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

# create session object for changes to database
Session = sessionmaker(bind=engine)
session = Session()

# store declarative base class
Base = declarative_base()

# define Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # representation method to quickly show recipe info 
    def __repr__(self):
        return f"<Recipe ID: {self.id} - Name: {self.name} - Difficulty: {self.difficulty}>"
    
    # string method to print formatted version of recipe
    def __str__(self):
        return (
            f"\t{'*'*1} {'-'*7} {self.name} {'-'*7} {'*'*1}\n"
            f"Recipe ID: {self.id}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time (min): {self.cooking_time}\n"
            f"Difficulty: {self.difficulty}\n"
        )
    
    # method to calculate recipe difficulty
    def calculate_difficulty(self):
        ingredients_list = self.return_ingredients_as_list()
        if self.cooking_time < 10 and len(ingredients_list) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(ingredients_list) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(ingredients_list) < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients_list) >= 4:
            self.difficulty = "Hard"
        return self.difficulty

    # method that retrieves ingredients
    def return_ingredients_as_list(self):
        if self.ingredients == "":
            return []
        else:
            return self.ingredients.split(", ")
        
# creates table on database
Base.metadata.create_all(engine)

# # # ------------------ main operation functions here ------------------ # # #

# function to create a recipe
def create_recipe():
    # validate user input for recipe name
    while True:
        name = input("Enter the name of the recipe: ").strip()
        if len(name) > 50:
            print("Error. Name must be 50 characters or less. Please try again.")
        elif not name.isalnum() and name != ' ':
            print("Error. Name can only contain alphanumeric characters.")
        else:
            break     

    # validate user input for ingredients
    ingredients = []
    while True:
        try:
            n = int(input("How many ingredients would you like to enter? ").strip())
            if n <= 0:
                print("Error. You must enter at least one ingredient. Please try again.")
            else:          
                break
        except ValueError:
            print("You must enter a positive number.")

    # collect ingredients from user here
    for i in range(n):
        while True:
            ingredient = input(f"Enter ingredient {i + 1}: ").strip()
            if ingredient:
                ingredients.append(ingredient)
                break
            else:
                print("Error. Ingredient list cannnot be empty. Please try again.")   

    # validate user input for cooking time is a number
    while True:
        cooking_time = input("Enter the cooking time in minutes: ").strip()
        if not cooking_time.isnumeric():
            print("Error. Cooking time must be a number. Please try again.")
        else:
            cooking_time = int(cooking_time)
            break

    ingredients_str = ", ".join(ingredients)
    print(f"Ingredients: {ingredients_str}") 

    # new object from Recipe model
    recipe_entry = Recipe(
        name = name,
        cooking_time = cooking_time,
        ingredients = ingredients_str
    )

    # generate difficulty with above recipe object
    recipe_entry.difficulty = recipe_entry.calculate_difficulty()

    # add recipe entry to session and commit
    session.add(recipe_entry)
    session.commit()

    print("Your recipe was successfully created!")

# function to view all recipes
def view_all_recipes():
    # call to database to retrieve recipes as a list
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no recipes in the database to view. You must create one!")
        return None
    
    for recipe in recipes:
        print(recipe)
    
# function to search recipe by ingredients
def search_by_ingredients():
    # query check to table for entries
    search_entries = session.query(Recipe).count()
    if search_entries == 0:
        print("No ingredients found! Return to the main menu and create a recipe.")
        return None    
    results = session.query(Recipe.ingredients).all()

    all_ingredients = []

    # add ingredients to a list, if not already there
    for result in results:
        ingredients_list = result[0].split(', ')
        for ingredient in ingredients_list:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # display numbered ingredients to user
    print("Available ingredients: ")
    for i, ingredient in enumerate(all_ingredients, start=1):
        print(f"{i}. {ingredient}")

    # user input
    selected_ingredients = input(
        "Select ingredient by typing the corresponding number, separated by spaces: "
        ).strip()

    try:
        selected_indices = [int(num) for num in selected_ingredients.split()]

        # check if selected numbers are valid
        if any(i < 1 or i > len(all_ingredients) for i in selected_indices):
            print("Error. One or more selected numbers are invalid. Please try again.")
            return None
        
    except ValueError:
        # handle error if user enters non-numeric value
        print("Error. Enter only numbers separated by spaces.")
        return None
    
    # list of ingredients to be searched for
    search_ingredients = [all_ingredients[i - 1] for i in selected_indices]

    # initialize empty list
    conditions = []

    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))
    
    # retrieve all recipes from database using filter() query
    recipes = session.query(Recipe).filter(*conditions).all()

    if recipes:
        for recipe in recipes:
            print(recipe)
        
    else:
        print("No recipes found from selected ingredients.")

# function to edit recipe
def edit_recipe():
    # checks if recipes are in database
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database to edit. Please create a recipe to continue!")
        return None
    
    # calls recipes by name and id from database
    results = session.query(Recipe.id, Recipe.name).all()       

    print("Available recipes:")                                
    for recipe in results:
        print(f"ID: {recipe.id} Name: {recipe.name}")

    # prompt user to select recipe by ID to edit
    try:
        selected_id = input("Enter the ID of the recipe you wish to edit: ").strip()            
        # call to database to get selected recipe by ID
        recipe_to_edit = session.query(Recipe).filter_by(id=selected_id).one()
        if not recipe_to_edit:
            print("Error. No recipe found with the provided ID.")
            return None
    except ValueError:
        print("Error. Invalid input. Please enter the ID of recipe.")
        return None                        

    # display selected recipe details
    print("Selected recipe:")                                                               
    print(f"1. Name: {recipe_to_edit.name}")
    print(f"2. Ingredients: {recipe_to_edit.ingredients}")
    print(f"3. Cooking Time (minutes): {recipe_to_edit.cooking_time}")

    # user prompt to select attribute to edit
    try:
        choice = int(input("Enter the number corresponding to the attribute you wish to edit (1-Name, 2-Ingredients, 3-Cooking Time): ").strip())        

        if choice == 1:
            # edit recipe name
            new_name = input("Enter the new name for the recipe: ").strip()
            if len(new_name) > 50 or not all(char.isalnum() or char.isspace() for char in new_name):
                print("Error. Name must be 50 characters or less and must only contain alphanumeric characters and spaces.")
                return None
            recipe_to_edit.name = new_name

        elif choice == 2:
            # edit ingredients
            new_ingredients = input("Enter the new ingredients for the recipe (separated by commas): ").strip()
            if not new_ingredients:
                print("Error. You must enter at least one ingredient. Please try again.")
                return None            
            recipe_to_edit.ingredients = ', '.join(new_ingredients)

        elif choice == 3:
            # edit cooking time
            new_cooking_time = input("Enter the new cooking time in minutes: ").strip()
            if not new_cooking_time.isnumeric():                
                print("Error. Cooking time must be a number. Please try again.")
                return None                       
            recipe_to_edit.cooking_time = int(new_cooking_time)

        else:
            print("Error. Invalid choice. Please select 1, 2, or 3.")
            return None

        # recalculate recipe difficulty and commit to database
        recipe_to_edit.difficulty = recipe_to_edit.calculate_difficulty()
        session.commit()
        print("Recipe has been successfully updated!")

    except ValueError:
        print("Error. Invalid input. Please try again.")

# function to delete a recipe
def delete_recipe():
    # checks if recipes are in database before proceeding
    if session.query(Recipe).count() == 0:
        print("There are no recipes in the database to delete. Please create a recipe to continue.")
        return None
    
    # retrieve and then displays list of recipes
    results = session.query(Recipe.id, Recipe.name).all()

    print("Available recipes:")
    for recipe in results:
        print(f"ID: {recipe.id} Name: {recipe.name}")

    # prompt user to select recipe by ID to delete
    try:
        selected_id = int(input("Enter the ID of the recipe you wish to delete: ").strip())
    except ValueError:
        print("Error. Invalid entry. Please enter a valid numeric ID.")
        return None

    # recipe retrieved from user selection
    recipe_to_delete = session.query(Recipe).filter_by(id=selected_id).one()
    if not recipe_to_delete:
        print("Error. No recipe found with provided ID.")
        return None

    while True:    
        selection = input(f"Are you sure you want to delete the recipe {recipe_to_delete.name}? Enter 'yes' or 'no': ").strip().lower()
        if selection == 'yes':
            session.delete(recipe_to_delete)
            session.commit()
            print("Recipe was successfully deleted.")
            break
        elif selection == 'no':
            print("Operation cancelled.")
            break
        else:
            print("Error. Invalid input. Please enter 'yes' or 'no'.")
       

# # # ------------------ main menu here ------------------ # # #

# while loop to run while user makes selection
def main_menu():
    selection = ""
    while selection != 'quit':
        print("\nWelcome to Recipes")
        print("=============================================")
        print("What would you like to do? Select an option.")
        print("---------------------------------------------")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit the application")

        selection = input("Your selection: ").strip().lower()

        # function to execute based on user input
        if selection == '1':
            create_recipe()
        elif selection == '2':
            view_all_recipes()
        elif selection == '3':
            search_by_ingredients()
        elif selection == '4':
            edit_recipe()
        elif selection == '5':
            delete_recipe()
        elif selection == 'quit':
            print("Exiting the application. Goodbye!")
            session.close()
            engine.dispose()
        else:
            print("Error. Invalid option. Please select 1, 2, 3, 4, or 5 or type 'quit'.")

main_menu()           
    