import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="cf-python",
    passwd="password"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(50),
ingredients VARCHAR(255),
cooking_time INT,
difficulty VARCHAR(20)
)''')


def main_menu(conn, cursor):
    choice = ""
    while (choice != "quit"):
        print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("\nMain Menu:")
        print("^^^^^^^^^^^^^^")
        print("Pick a choice:")
        print("   1. Create a new recipe")
        print("   2. Search for a recipe by ingredient")
        print("   3. Update an existing recipe")
        print("   4. Delete a recipe")
        print("   5. View all recipes")
        print("\nType 'quit' to exit the program.")
        choice = input("\nYour choice: ").strip().lower()
        print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

        if choice in ["1", "2", "3", "4", "5"]:

            if choice == "1":
                create_recipe(conn, cursor)
            elif choice == "2":
                search_recipe(conn, cursor)
            elif choice == "3":
                update_recipe(conn, cursor)
            elif choice == "4":
                delete_recipe(conn, cursor)
            elif choice == "5":
                view_all_recipes(conn, cursor)
        elif choice == "quit":
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("      Thank you for using the Recipe App!       ")
            print("      Happy cooking! Please come back.          ")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            break
        else:
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("Not a valid choice! Please enter 1, 2, 3, 4, or 'quit'.")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
            print("...back to the main menu\n\n")

    conn.close()


def create_recipe(conn, cursor):
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("            Build New Recipes              ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("To add new recipes, follow along below!\n")

    while True:
        try:
            number_of_recipes = int(
                input("How many recipes would you like to build? "))
            if number_of_recipes < 1:
                print("Please enter a positive number.\n")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.\n")

    for i in range(number_of_recipes):
        print(f"\nEnter recipe #{i + 1}")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        name = input("  Enter recipe name: ").strip()
        cooking_time = int(input("  Enter cooking time in minutes: "))
        ingredients_input = input(
            "  Enter recipe's ingredients, each separated by a comma: ")
        ingredients = ingredients_input.split(", ")

        difficulty = calculate_difficulty(cooking_time, ingredients)

        ingredients_str = ", ".join(ingredients)

        try:
            insert_query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, ingredients_str,
                           cooking_time, difficulty))
            conn.commit()

            print("  ** You have added a recipe! **")
        except mysql.connector.Error as err:
            print("Error occurred: ", err)

    final_message = "Recipe added!" if number_of_recipes == 1 else "All recipes have been added!"

    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(f"            {final_message}            ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    print("...back to main menu\n\n")


def calculate_difficulty(cooking_time, ingredients):
    num_ingredients = len(ingredients)
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    elif cooking_time >= 10 and num_ingredients >= 4:
        return "Hard"


def format_recipe_display(recipe):
    print(f"\nRecipe: {recipe[1].title()}")
    print(f"  Time: {recipe[3]} mins")
    print("  Ingredients:")
    for ingredient in recipe[2].split(", "):
        print(f"  - {ingredient.title()}")
    print(f"  Difficulty: {recipe[4]}")


def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("    The recipe database seems to be empty, nothing to search.   ")
        print("                  Please build a new recipe!                  ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        print("...returning to main menu\n\n")
        return

    all_ingredients = set()

    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("                Recipe seach by Ingredient             ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("To see all recipes that use a certain ingredient, enter a number: \n")

    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    for i, ingredient in enumerate(sorted(all_ingredients)):
        print(f"{i+1}.) {ingredient.title()}")

    print()
    while True:
        try:
            choice = int(input("For your ingredient enter a number: "))
            if 1 <= choice <= len(all_ingredients):
                break
            else:
                print()
                print("Number must be within the list range.\n")
        except ValueError:
            print()
            print("Invalid input. Please enter a number.\n")

    selected_ingredient = sorted(all_ingredients)[choice - 1]

    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(search_query, ("%" + selected_ingredient + "%",))
    search_results = cursor.fetchall()

    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found containing '{
              selected_ingredient.title()}'\n")
        for recipe in search_results:
            format_recipe_display(recipe)

        print()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("            Search successful, found your recipe!             ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        print("...back to main menu\n")
    else:
        print(f"No recipes with '{selected_ingredient.title()}'\n")

    print("\n")


def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("   The recipe database seems to be empty, nothing to update.    ")
        print("                  Please build a new recipe!                  ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        print("...back to main menu\n\n")
        return

    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("             Recipe update by ID number                 ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Enter an ID number to update that recipe\n")

    print("^^^^ Avaiable Recipes ^^^^\n")
    for result in results:
        ingredients_list = result[2].split(", ")
        capitalized_ingredients = [ingredient.title()
                                   for ingredient in ingredients_list]
        capitalized_ingredients_str = ", ".join(capitalized_ingredients)

        print(f"ID: {result[0]} | Name: {result[1]}")
        print(f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {
              result[3]} | Difficulty: {result[4]}\n")

    while True:
        try:
            print()
            recipe_id = int(
                input("Enter the ID number of the recipe to update: "))
            print()

            cursor.execute(
                "SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("That entered ID is not linked to a recipe. Try again.\n")
            else:
                break
        except ValueError:
            print()
            print("Invalid input. Entry must be a numeric value.\n")

    selected_recipe = next(
        (recipe for recipe in results if recipe[0] == recipe_id), None)
    if selected_recipe:
        print(f"Which part of the recipe would you like to update for '{
              selected_recipe[1]}'?")
    else:
        print("Recipe not found.")
        return
    print(" - Name")
    print(" - Cooking Time")
    print(" - Ingredients\n")

    update_field = input("Enter your choice: ").lower()
    print()

    if update_field == "cooking time":
        update_field = "cooking_time"

    if update_field not in ["name", "cooking_time", "ingredients"]:
        print("Invalid entry. Please enter 'name', 'cooking_time', or 'ingredients'.")
        return

    if update_field == "cooking_time" or update_field == "cooking time":
        while True:
            try:
                new_value = int(
                    input("Enter the new cooking time (in minutes): "))
                break
            except ValueError:
                print("Invalid input. Entry must be a numeric value for cooking time.")
    else:
        new_value = input(f"Enter the new value for {update_field}: ")

    update_query = f"UPDATE Recipes SET {update_field} = %s WHERE id = %s"
    cursor.execute(update_query, (new_value, recipe_id))

    if update_field in ["cooking_time", "ingredients"]:
        cursor.execute(
            "SELECT cooking_time, ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        updated_recipe = cursor.fetchone()
        new_difficulty = calculate_difficulty(
            int(updated_recipe[0]), updated_recipe[1].split(", "))

        cursor.execute(
            "UPDATE Recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))

    conn.commit()

    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("           Recipe has been successfully modified!           ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    print("...back to main menu\n\n")


def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    if not results:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("   The recipe database seems to be empty, nothing to delete.   ")
        print("                  Build a new recipe!                  ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        print("...back to main menu\n\n")
        return

    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("              Recipe delete by ID Number                ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Enter the ID number of the recipe to delete")
    print("*ALERT!: This is permenant!\n")

    print("---- Avaiable Recipes ----\n")
    for result in results:
        ingredients_list = result[2].split(", ")
        capitalized_ingredients = [ingredient.title()
                                   for ingredient in ingredients_list]
        capitalized_ingredients_str = ", ".join(capitalized_ingredients)

        print(f"ID: {result[0]} | Name: {result[1]}")
        print(f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {
              result[3]} | Difficulty: {result[4]}\n")

    while True:
        try:
            recipe_id = int(input("Enter the ID of the recipe to delete: "))
            print()

            cursor.execute(
                "SELECT COUNT(*) FROM Recipes WHERE id = %s", (recipe_id,))
            if cursor.fetchone()[0] == 0:
                print("That entered ID is not linked to a recipe. Try again.\n")
            else:

                cursor.execute(
                    "SELECT name FROM Recipes WHERE id = %s", (recipe_id,))
                recipe_name = cursor.fetchone()[0]
                confirm = input(f"Are you positive you want to delete '{
                                recipe_name}'? (Yes/No): ").lower()

                if confirm == "yes":
                    break
                elif confirm == "no":
                    print()
                    print("Cancelled. Back to main menu\n\n")
                    return
                else:
                    print()
                    print("Answer with 'Yes' or 'No'.\n")

        except ValueError:
            print()
            print("Invalid input. Entry must be a numeric value.\n")

    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))

    conn.commit()

    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("           Deletion of recipe successful!           ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    print("...back to main menu\n\n")


def view_all_recipes(conn, cursor):
    print("\nThis is all the recipes: ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    for row in results:
        print("\nID: ", row[0])
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking Time: ", row[3])
        print("Difficulty: ", row[4])


main_menu(conn, cursor)
