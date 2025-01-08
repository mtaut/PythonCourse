# ------------ connecting script to MySQL server and database ------------
import mysql.connector # type: ignore

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'cf-python',
    passwd = 'password'
)

# initializing cursor object from conn
cursor = conn.cursor()

# creating database for task
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

# accessing database
cursor.execute("USE task_database")

# creating table 'recipes'
cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(50),
               ingredients VARCHAR(255),
               cooking_time INT,
               difficulty VARCHAR(20) 
               )''')

# ------------ user menu and functions here ------------

# function for main_menu and CRUD functions - create_recipe / search_recipe / update_recipe / delete_recipe
def main_menu():
    # while loop to run while user makes selection
    selection = ""
    while(selection != 'quit'):
        print("\nWelcome to Recipes")
        print("=============================================")
        print("What would you like to do? Select an option.")
        print("---------------------------------------------")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exit the program")
        selection = input("Your selection: ").strip().lower()
         
        if selection == '1':
            create_recipe(conn, cursor)
        elif selection == '2':
            search_recipe(conn, cursor)
        elif selection == '3':
            update_recipe(conn, cursor)
        elif selection == '4':
            delete_recipe(conn, cursor)
        elif selection == 'quit':
            print("\nExiting the program. Goodbye!")              
            conn.commit()
            conn.close()
        else:
            print("Invalid option. Please select 1, 2, 3, 4, or type 'quit'.")

# function to create a recipe
def create_recipe(conn, cursor):
    name = str(input("\nEnter the name of the recipe: "))
    cooking_time = int(input("\nEnter the cooking time in minutes: "))
    ingredients = [str(ingredients) for ingredients in input("\nEnter the ingredients, separated by a comma: ").split(", ")]
    ingredients_str = ', '.join(ingredients)
    print("\nRecipe successfully saved!")

    difficulty = calc_difficulty(cooking_time, ingredients)

    # SQL query here
    sql = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ingredients_str, cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    

# function to search for a recipe
def search_recipe(conn, cursor):
    all_ingredients = set()

    # fetches ingredients from database
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall()

    # this adds ingredient string to the set
    for (ingredients_string,) in results:             
            split_ingredients = ingredients_string.split(", ")
            all_ingredients.update(split_ingredients)

    searched_ingredients = sorted(all_ingredients)

    # displays ingredients to user
    print("\nIngredients available for search: ")
    for index, ingredient in enumerate(searched_ingredients, start=1):
        print(f"{index}. {ingredient}")

    search_ingredient = None

    try:
        ingredient_choice = int(input("\nEnter the number corresponding to the ingredient you want to search for: "))
        if 1 <= ingredient_choice <= len(searched_ingredients):
            search_ingredient = searched_ingredients[ingredient_choice - 1]
            print(f"\nYou selected: {search_ingredient}")

        else:
            print("\nInvalid choice. Please try again.")
            return
    except ValueError:
            print("\nInvalid input. Please enter a number.")
            return
    # query to SQL
    sql = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    val = (f"%{search_ingredient}%",)

    cursor.execute(sql, val)
    search_result = cursor.fetchall()

    if search_result:
        print("\nRecipes found: ")
        for row in search_result:
            print(f"ID: {row[0]}, Name: {row[1]}, Ingredients: {row[2]}, "
            f"Cooking Time: {row[3]} mins, Difficulty: {row[4]}")
    else:
        print("Sorry, no recipes found with that ingredient.")
    

# function to update recipe
def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    # displays recipe info to user
    print("\nRecipes: ")
    for recipe in results:
        print(f"ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]},"
            f"Cooking Time: {recipe[3]} mins, Difficulty: {recipe[4]}")
         
    try:
        recipe_id = int(input("\nEnter the ID of the recipe you want to update: "))

        # asking user which column to update
        print("\nRecipe info available to update: name, cooking_time, ingredients")
        column_to_update = input("Enter the column you wish to update: ").strip().lower()

        if column_to_update not in {"name", "cooking_time", "ingredients"}:
            print("Invalid column name. Please choose from 'name', 'cooking_time', or 'ingredients'.")
            return

        # prompt for new value
        new_value = input(f"Enter the new value for {column_to_update}: ").strip()

        if column_to_update == "cooking_time":
            try:
                new_value = int(new_value)
            except ValueError:
                print("Cooking time must be a number.")
                return
        
        # query to SQL
        sql = f"UPDATE Recipes SET {column_to_update} = %s WHERE id = %s"
        cursor.execute(sql, (new_value, recipe_id))
        conn.commit()
        print(f"\n{column_to_update.capitalize()} updated successfully!")

        if column_to_update in ["cooking_time", "ingredients"]:
            cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
            updated_recipe = cursor.fetchone()

            if updated_recipe:
                updated_cooking_time = updated_recipe[0]
                updated_ingredients = updated_recipe[1].split(", ")

                # recalculate recipe difficulty with modified cooking_time and ingredients
                new_difficulty = calc_difficulty(updated_cooking_time, updated_ingredients)

                cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id =%s", (new_difficulty, recipe_id))
                conn.commit()                                            
            
    except ValueError:
        print("Oops, this entry is invalid. Please try again.")       
         

# function to delete recipe
def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    # shows all recipes first
    print("\nRecipes: ")
    for recipe in results:
        print(f"ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]},"
            f"Cooking Time: {recipe[3]} mins, Difficulty: {recipe[4]}")
              
    id_to_delete = int(input("\nEnter the ID of the recipe you wish to delete: "))

    # call to delete recipe
    cursor.execute(f"DELETE FROM Recipes WHERE id = %s", (id_to_delete, ))
    conn.commit()
    print("Recipe successfully deleted.")

    # this re-displays updated list of recipes after deletion
    cursor.execute("SELECT * FROM Recipes")
    updated_results = cursor.fetchall()

    if updated_results:
        print("\nUpdated Recipes: ")
        for recipe in updated_results:
            print(f"ID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]},"
            f"Cooking Time: {recipe[3]} mins, Difficulty: {recipe[4]}")
        else:
            print("\nNo recipes found in database.")
    
# recipe difficulty function
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) >= 4:
        difficulty = "Hard"
    return difficulty
    
main_menu()
