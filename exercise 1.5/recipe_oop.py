class Recipe:
    # Class variable storing all unique ingredients from recipes
    all_ingredients = set()

    # Initialization method with name and cooking time
    def __init__(self, name, cooking_time):
        self.name = name
        self.ingredients = []
        self.cooking_time = cooking_time
        self.difficulty = None

    # Add ingredients to the recipe
    def add_ingredients(self, *dish):
        for ingredient in dish:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()  # Update with new ingredients

    # Update the class variable all_ingredients with unique ingredients
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)

    # Difficulty level calculated based on cooking time and ingredients quantity
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    # Recipe name getter
    def get_name(self):
        return self.name
    
    # Resipe name setter
    def set_name(self, name):
        self.name = name

    # Cooking time getter
    def get_cooking_time(self):
        return self.cooking_time

    # Cooking time setter
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # Ingredients list getter
    def get_ingredients(self):
        return self.ingredients

    # Difficulty getter, will calculate if not done
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    # Ingredient search
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # String of the recipe
    def __str__(self):
        self.calculate_difficulty()
        return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}"


# Specific ingredient search
def recipe_search(data, search_term):
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


# Main code

# Instances of the Recipes
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients(
    "Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"
)
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients(
    "Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"
)
print(banana_smoothie)

# List of recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

# Find recipes containing specific ingredients using Recipe_search
print("\nRecipes containing Water:")
recipe_search(recipes_list, "Water")

print("\nRecipes containing Sugar:")
recipe_search(recipes_list, "Sugar")

print("\nRecipes containing Bananas:")
recipe_search(recipes_list, "Bananas")