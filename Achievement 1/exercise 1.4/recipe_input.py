import pickle

def top_title():
    print("__________________________________")
    print("This is your recipe input program!")
    print("__________________________________")


# Recipe difficulty calculation
def calc_difficulty(cooking, total_ingredients):
    if cooking < 10 and total_ingredients < 4:
        return "Easy"
    elif cooking < 10 and total_ingredients >= 4:
        return "Medium"
    elif cooking >= 10 and total_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"
    
# User recipe input
def take_recipe(recipe_num):
    print(f"\n---- Recipe #{recipe_num} ----")

    # Validate recipe name
    while True:
        name = input("Enter your recipe name: ").strip()
        if name:
            break
        print("\nPlease enter a valid recipe name.")
  
 # Cooking time validation
    while True:
        try:
            cooking = int(input("Cooking time in minutes: "))
            if cooking > 0:
                break
            print("\nMust be a positive number.")
        except ValueError:
            print("\nPlease enter a number only.")

    # Ingredients validation
    while True:
        ingredients_input = input("Enter your ingredients, seperated by a comma: ").strip()
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
        if ingredients:
            break
        print("\nMust be at least one ingredient.")
    
    difficulty = calc_difficulty(cooking, len(ingredients))
    return {"name": name, "cooking": cooking, "ingredients": ingredients, "difficulty": difficulty}

# Main begining
top_title()
filename = input("Filename to save the recipes: ")

# Load file data or new file if not found
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = {"recipes_list": [], "all_ingredients": []}
except Exception as e:
    print(f"An error occured: {e}")
    data = {"recipes_list": [], "all_ingredients": []}

recipes_list, all_ingredients = data["recipes_list"], data["all_ingredients"]

# Collect user recipes
n = int(input("\nHow many recipes are you entering today?: "))
for i in range(1, n+1):
    recipe = take_recipe(i)
    recipes_list.append(recipe)
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

# Save updated data
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}
    
with open(filename, "wb") as file:
    pickle.dump(data, file)

print("\nYour recipes were saved!")    

