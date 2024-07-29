from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.expression import or_

# Connecting SQLAlchemy with the database
engine = create_engine("mysql://cf-python:password@localhost/task_database")

# Base Class: All model classes will inherit from this class.
Base = declarative_base()

# Create Session: Session will be used to query and commit transactions.
Session = sessionmaker(bind=engine)
session = Session()


class Recipe(Base):
    # Table Name: The name of the table.
    __tablename__ = "final_recipes"

    # Schema:
    # |-----------------------------------------------------------------------------------|
    # | Field        | Type         | Null     | Key         | Default   | Extra          |
    # |--------------|--------------|----------|-------------|-----------|----------------|
    # | id           | int          | NOT NULL | PRIMARY KEY | NULL      | AUTO_INCREMENT |
    # | name         | varchar(50)  | NULLABLE |             | NULL      |                |
    # | ingredients  | varchar(255) | NULLABLE |             | NULL      |                |
    # | cooking_time | int          | NULLABLE |             | NULL      |                |
    # | difficulty   | varchar(20)  | NULLABLE |             | NULL      |                |
    # |-----------------------------------------------------------------------------------|

    # Columns: The structure.
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        # Representation: Quick string representation of the object.
        return f"<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>"

    def __str__(self):
        # String Representation: A user-friendly way for printing.
        ingredients_list = self.ingredients.split(", ")
        formatted_ingredients = "\n ".join(
            f"  - {ingredient.title()}" for ingredient in ingredients_list)

        return (f"Recipe ID: {self.id}\n"
                f"  Name: {self.name.title()}\n"
                f"  Ingredients:\n {formatted_ingredients}\n"
                f"  Cooking Time: {self.cooking_time} minutes\n"
                f"  Difficulty: {self.difficulty}\n")

    def calculate_difficulty(self):
        # Calculate Difficulty: Difficulty based on cooking time and number of ingredients.
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        elif self.cooking_time >= 10 and num_ingredients >= 4:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        # Convert Ingredients to List: Splits the ingredients string into a list.
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")


# Create Tables: Execute the creation of tables in the database.
Base.metadata.create_all(engine)


def create_recipe():
    # Display the header for the building a recipe function.
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("             Build New Recipes for the Database             ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("To add new recipes, follow along below!\n")

    # Loop to get the number of recipes the user wants to enter.
    # Validates that the input is a positive number.
    while True:
        try:
            number_of_recipes = int(
                input("How many recipes would you like to enter? "))
            if number_of_recipes < 1:
                print("Please enter a positive number.\n")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a number.\n")

    # Loop over the number of recipes to be created.
    for i in range(number_of_recipes):
        print(f"\nEnter recipe #{i + 1}")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        # Input validation for recipe name, ensuring it's within the character limit.
        while True:
            name = input("  Enter the recipe name: ").strip().lower()
            if 0 < len(name) <= 50:
                break
            else:
                print("Please enter a valid recipe name (1-50 characters).\n")

        # Input validation for cooking time, ensuring it's a positive number.
        while True:
            try:
                cooking_time = int(
                    input("  Enter the cooking time in minutes: "))
                if cooking_time > 0:
                    break
                else:
                    print("Please enter a positive number for cooking time.\n")
            except ValueError:
                print(
                    "Invalid input. Please enter a positive number for cooking time.\n")

        # Validation for ingredients, validating input is not empty.
        while True:
            ingredients_input = input(
                "  Enter the recipe's ingredients, separated by a comma: ").strip().lower()
            if ingredients_input:
                break
            else:
                print("Please enter at least one ingredient.\n")

        # Create a new recipe instance and add it to the session.
        new_recipe = Recipe(
            name=name, ingredients=ingredients_input, cooking_time=cooking_time)
        new_recipe.calculate_difficulty()

        # Add the new recipe to the session and attempt to commit it to the database.
        session.add(new_recipe)
        try:
            session.commit()
            print("   Recipe added! ")

        except Exception as err:
            # Rollback in case of error during commit.
            session.rollback()
            print("Error occurred: ", err)

    # Display a final message after adding recipes.
    final_message = "Recipe added!" if number_of_recipes == 1 else "All recipes added!"
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print(f"            {final_message}            ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

    # Pause the execution and wait for the user to press enter.
    pause()


def view_all_recipes():
    # Retrieve all recipes from the database.
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database, and display a message if there are none.
    if not recipes:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("         There are no recipes in the database to search.        ")
        print("                      Build a new recipe!                   ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        pause()
        return None

    # Header display for viewing all recipes.
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("                   View All Recipes                   ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    # Display the number of recipes found.
    recipe_count = len(recipes)
    recipe_word = "recipe" if recipe_count == 1 else "recipes"
    print(f"Displaying {recipe_count} {recipe_word}\n")

    # Loop through each recipe and display its details using a formatted string.
    for i, recipe in enumerate(recipes, start=1):
        print(f"Recipe #{i}\n----------")
        print(format_recipe_for_search(recipe))
        print()

    # Display after listing all recipes.
    print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("             Search successful, found your recipe!              ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

    # Pause the execution and wait for the user to press enter.
    pause()


def search_recipe():
    # Retrieve all ingredients from all recipes in the database.
    results = session.query(Recipe.ingredients).all()

    # If no recipes are found, display a message and return to the main menu.
    if not results:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("       There are no recipes in the database to search.         ")
        print("                     Build a new recipe!                   ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        pause()
        return

    # Initialize a set to store all unique ingredients from the database results.
    all_ingredients = set()
    for result in results:
        ingredients_list = result[0].split(", ")
        for ingredient in ingredients_list:
            all_ingredients.add(ingredient.strip())

    # Print header for search function and instructions for user.
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("                Recipe seach by Ingredient             ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("To see all recipes that use a certain ingredient, enter a number:\n")

    # Sort and display each ingredient with its corresponding ID.
    sorted_ingredients = sorted(all_ingredients)
    for i, ingredient in enumerate(sorted_ingredients):
        print(f"{i+1}.) {ingredient.title()}")

    # Request user to enter one or more ingredient numbers, separated by spaces.
    print()
    while True:
        try:
            choices = input(
                "Enter ingredient numbers (separate multiple numbers with spaces): ").split()
            selected_indices = [int(choice) for choice in choices]
            if all(1 <= choice <= len(all_ingredients) for choice in selected_indices):
                break
            else:
                print("Please enter numbers within the list range.\n")
        except ValueError:
            print("Invalid input. Please enter valid numbers.\n")

    # Convert user input into a list of selected ingredients.
    search_ingredients = [sorted_ingredients[index - 1]
                          for index in selected_indices]

    # Build a search query using the selected ingredients.
    search_conditions = [Recipe.ingredients.ilike(
        f"%{ingredient}%") for ingredient in search_ingredients]
    search_results = session.query(Recipe).filter(
        or_(*search_conditions)).all()

    # Format the string of selected ingredients.
    if len(search_ingredients) > 1:
        selected_ingredients_str = ", ".join(
            ingredient.title() for ingredient in search_ingredients[:-1])
        selected_ingredients_str += ", or " + search_ingredients[-1].title()
    else:
        selected_ingredients_str = search_ingredients[0].title()

    # See if there are any recipes with the selected ingredients.
    if search_results:
        recipe_count = len(search_results)
        recipe_word = "recipe" if recipe_count == 1 else "recipes"
        print(f"\n{recipe_count} {recipe_word} found with '{
              selected_ingredients_str}'\n")

        # Display each found recipe with its details.
        for i, recipe in enumerate(search_results, start=1):
            print(f"Recipe #{i}\n^^^^^^^^^^")
            print(format_recipe_for_search(recipe))
            print()

        # End of search result display with a success message.
        print()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("            Search successful, found your recipe!             ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    else:
        # Message for the user if no matching recipes are found.
        print(f"No recipes found with '{selected_ingredients_str}'\n")

    # Pause and wait for the user to press enter.
    pause()


def update_recipe():
    # Retrieve all recipes from the database.
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database; if not, display a message.
    if not recipes:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("       There are no recipes in the database to update.         ")
        print("                     Build a new recipe!                    ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        pause()
        return

    # Header for the update function.
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("              Recipe update by ID number                 ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Enter an ID number to update that recipe\n")

    # Display the available recipes for update.
    print("^^^^ Avaiable Recipes ^^^^\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))
    print()

    # Loop to get the ID of the recipe to update.
    while True:
        try:
            recipe_id = int(
                input("Enter the ID number of the recipe to update: "))
            recipe_to_update = session.get(Recipe, recipe_id)
            if recipe_to_update:
                break
            else:
                print("That entered ID is not linked to a recipe. Try again.\n")
        except ValueError:
            print("Invalid input. Entry must be a numeric value.\n")

    # Ask the user to choose which field of the recipe to update.
    print(f"\nWhich part of the recipe would you like to update for '{
          recipe_to_update.name}'?")
    print(" - Name")
    print(" - Cooking Time")
    print(" - Ingredients\n")

    # Flag to track if the field has been successfully updated.
    field_updated = False
    while not field_updated:
        update_field = input("Enter your choice: ").lower()

        # Update logic for each field.
        if update_field == "name":
            while True:
                new_value = input(
                    "\nEnter the new name (1-50 characters): ").strip()
                if 0 < len(new_value) <= 50:
                    recipe_to_update.name = new_value
                    field_updated = True
                    break
                else:
                    print("Invalid name. Please enter 1-50 characters.\n")
            break

        elif update_field == "cooking time":
            while True:
                try:
                    new_value = int(
                        input("\nEnter the new cooking time (in minutes): "))
                    if new_value > 0:
                        recipe_to_update.cooking_time = new_value
                        # Recalculate the difficulty after updating cooking time.
                        recipe_to_update.calculate_difficulty()
                        field_updated = True
                        break
                    else:
                        print(
                            "Invalid input. Entry must be a numeric value for cooking time.")
                except ValueError:
                    print(
                        "Invalid input. Enter a numeric value for cooking time.")
            break

        elif update_field == "ingredients":
            while True:
                new_value = input(
                    "\nEnter the new ingredients, separated by a comma: ").strip().lower()
                if new_value:
                    # Update the ingredients and recalculate the difficulty.
                    recipe_to_update.ingredients = new_value
                    recipe_to_update.calculate_difficulty()
                    field_updated = True
                    break
                else:
                    print("Please enter at least one ingredient.")
            break
        else:
            print(
                "Invalid choice. Please choose 'name', 'cooking time', or 'ingredients'.")

    # Attempt to commit the updated recipe to the database.
    try:
        session.commit()
        print("\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("           Recipe has been successfully modified!          ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    except Exception as err:
        # Rollback in case of error during the commit.
        session.rollback()
        print(f"An error occurred: {err}")

    # Pause the execution and wait for the user to press enter.
    pause()


def delete_recipe():
    # Retrieve all recipes from the database.
    recipes = session.query(Recipe).all()

    # Check if there are any recipes in the database; if not, display a message.
    if not recipes:
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("        There are no recipes in the database to delete.        ")
        print("                  Please create a new recipe!                  ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        pause()
        return

    # Header for the delete recipe function.
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("              Recipe delete by ID Number                 ")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print("Enter the ID number of the recipe to delete")
    print("**ALERT!: This is permenant!**\n")

    # Display the available recipes for deletion.
    print("^^^^ Avaiable Recipes ^^^^\n")
    for recipe in recipes:
        print(format_recipe_for_update(recipe))

    # Loop to get the ID of the recipe to be deleted.
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
            # Retrieve the recipe to be deleted from the database.
            recipe_to_delete = session.get(Recipe, recipe_id)

            # Confirm deletion from the user.
            if recipe_to_delete:
                confirm = input(f"\nAre you positive you want to delete '{
                                recipe_to_delete.name}'? (Yes/No): ").lower()
                if confirm == "yes":
                    break
                elif confirm == "no":
                    print("Cancelled. Back to main menu.\n")
                    pause()
                    return
                else:
                    print("Please answer with 'Yes' or 'No'.")
            else:
                print("Invalid input. Entry must be a numeric value.")

        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    # Attempt to delete the selected recipe from the database.
    try:
        session.delete(recipe_to_delete)
        session.commit()
        print()
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("           Deletion of recipe successful!           ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    except Exception as err:
        # Rollback in case of error during the deletion.
        session.rollback()
        print(f"An error occured: {err}")

    # Pause the execution and wait for the user to press enter.
    pause()


def main_menu():
    # Initialize the choice variable.
    choice = ""

    # Main menu loop - continues until the user decides to quit the app.
    while choice != "quit":

        # Main menu header and options.
        print(" ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("\nThe Recipe App - Main Menu:")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("Make a Selection!    ")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Update an existing recipe")
        print("5. Delete a recipe\n")
        print("Type 'quit' to exit the program\n")

        # while True:
        # Get the user's choice and convert it to lower case.
        choice = input("Your choice: ").strip().lower()

        # Execute the appropriate function.
        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_recipe()
        elif choice == "4":
            update_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            # Goodbye message when user decides to quit.
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("      Thank you for using the Recipe App!       ")
            print("        Happy cooking! Please come back.   ")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            break  # Exit the loop to end program.
        else:
            # Handle invalid input and prompt the user to try again.
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print("Not a valid choice! Please enter 1, 2, 3, 4, 5, or 'quit'.")
            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")

            # Pause for user acknowledgement.
            pause()

    session.close()
    engine.dispose()


def format_recipe_for_search(recipe):
    # Format the recipe's ingredients for display.
    formatted_ingredients = "\n  ".join(
        f"- {ingredient.title()}" for ingredient in recipe.ingredients.split(", "))

    # Return a string representing the recipe's details.
    return (f"Recipe Name: {recipe.name.title()}\n"
            f"  Cooking Time: {recipe.cooking_time} mins\n"
            f"  Ingredients:\n  {formatted_ingredients}\n"
            f"  Difficulty: {recipe.difficulty}")


def format_recipe_for_update(recipe):
    # Capitalize the first letter of each ingredient.
    capitalized_ingredients = [ingredient.title()
                               for ingredient in recipe.ingredients.split(", ")]

    # Capitalize the first letter of each ingredient.
    capitalized_ingredients_str = ", ".join(capitalized_ingredients)

    # Return a string representing the recipe's details.
    return (f"ID: {recipe.id} | Name: {recipe.name}\n"
            f"Ingredients: {capitalized_ingredients_str} | Cooking Time: {recipe.cooking_time} | Difficulty: {recipe.difficulty}\n")


def pause():
    # Message prompting the user to press ENTER, then wait for input.
    print("Press ENTER to return to the main menu...", end="")
    input()

    print("\n\n\n\n")


if __name__ == "__main__":
    # This is the entry point of the program. Runs Main Menu function.
    main_menu()
