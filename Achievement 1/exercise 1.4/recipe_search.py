import pickle

def top_title():
    print("__________________________________")
    print("This is your recipe search program!")
    print("__________________________________")

# Show single recipe
def display_recipe(recipe):
    print(f"\nRecipe: {recipe['name'].title()}")
    print(f"  Time: {recipe['cooking']} mins")
    print("  Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(f"  - {ingredient.title()}")
    print(f"  Difficulty: {recipe['difficulty']}")

# Search by a specified ingredient
def search_ingredient(data):
    all_ingredients = data["all_ingredients"]
    print("\n-----------------------")
    print(" All Ingredients Listed ")
    print("-----------------------")
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}.) {ingredient.title()}")
    
# Validate input for an ingredient
    try:
        while True:
            choice = int(input("\nHow many ingredients would you like to search: "))
            if 1 <= choice <= len(all_ingredients):
                ingredient_searched = all_ingredients[choice-1]
                break
            print(f"Please enter a number between 1 and {len(all_ingredients)}.")
        
# Locate recipe for the selected ingredient
        recipes_with_ingredient = [recipe for recipe in data["recipes_list"] if ingredient_searched in recipe["ingredients"]]
        num_recipes = len(recipes_with_ingredient)

# Display number of found recipes
        recipe_word = "Recipe" if num_recipes == 1 else "Recipes"

        decoration = "-" * (len(f"{num_recipes} {recipe_word} found containing {ingredient_searched.title()}") + 2)
        print(f"\n{decoration}")
        print(f" {num_recipes} {recipe_word} found containing {ingredient_searched.title()} ")
        print(f"{decoration}")

# Display each found recipe
        for recipe in recipes_with_ingredient:
            display_recipe(recipe)

# Invalid inputs responses
    except ValueError:
        print("Invalid input! Please enter a number.")
    except IndexError:
        print("No such ingredient number.")

# Main begining
top_title()  
filename = input("Filename of your recipe data: ")

# File load
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not located. Please check your spelling and try again.")
else:
    search_ingredient(data)    