import os
import json
import random

from src.controllers.controller import Controller
from src.util.dao import DAO

from src.static.diets import Diet
from src.util.calculator import calculate_readiness

class RecipeController(Controller):
    def __init__(self, items_dao: DAO):
        super().__init__(dao=items_dao)

        # load existing recipes
        self.recipes = self.load_recipes()

    def load_recipes(self) -> list[dict]:
        """Read all available recipes from the src/static/recipes/ directory and puts them in an array. The items of this array follow the same format as the JSON files in the directory.

        returns:
          recipes -- list of recipes in dictionary format"""
        recipes: list[dict] = []
        for filename in os.listdir('./src/static/recipes'):
            with open(f'./src/static/recipes/{filename}') as f:
                recipe = json.load(f)
                recipes.append(recipe)
        return recipes

    def get_available_items(self, minimum_quantity: int = -1) -> dict:
        """Obtain a dictionary of available items in the pantry.

        parameters:
          minimum_quantity -- the minimum quantity that an item needs to have in order to be included in the returned dictionary

        returns:
          available_items: dict -- a dictionary mapping pantry item names to their quantity (only including pantry items which have a quantity of minimum_quantity or higher)
          None -- in case the self.get_all() method throws an exception"""

        items = self.get_all() # array of objects

        available_items = {}
        for item in items:
            if item["quantity"] > minimum_quantity:
                available_items[item["name"]] = item["quantity"]

        return available_items

    def get_recipe_readiness(self, recipe: dict, available_items: dict, diet: Diet) -> float:
        """Calculate the readiness value of a recipe. The readiness determines to what degree the required ingredients are already available in the current pantry.

        parameters:
          recipe -- a recipe in the structure as found in src/static/recipes
          available_items -- dictionary mapping all available pantry items to their currently available amount
          diet -- dietary preference which a recipe needs to comply to

        returns:
          readiness -- a value between 0 and 1 obtained via calculate_readiness and representing, how many of the required ingredients are already available
          None -- if the recipe has a current readiness of below 0.1
          None -- if the recipe is not available to the selected diet
        """
        if diet.name.lower() not in recipe['diets']:
            return None

        readiness = calculate_readiness(recipe, available_items)

        if readiness > 0.1:
            return readiness
        return None

    def get_readiness_of_recipes(self, recipes: list[dict], diet: Diet) -> dict:
        """Calculate the readiness of each recipe by the available items.

        parameters:
          recipes -- list of recipes in the structure as found in src/static/recipes
          available_items -- list of available pantry items
          diet -- dietary preference which a recipe needs to comply to

        returns:
          readiness -- A dictionary that maps a recipe name (of recipes complying to the dietary restrictions) to a readiness value between 0 and 1 as calculated via calculate_readiness"""
        # obtain all available items
        available_items = self.get_available_items()

        recipe_readiness = {}
        for recipe in recipes:
            readiness = self.get_recipe_readiness(
                recipe, available_items, diet)
            if readiness != None:
                recipe_readiness[recipe["name"]] = readiness

        return recipe_readiness

    def get_recipe(self, diet: Diet, take_best: bool) -> str:
        """Propose a suitable recipe depending on the diet and the item usage strategy.

        parameters:
          diet -- A specification of a diet (available from the Diet enumerator) which the returned recipes must comply to.
          take_best -- Item usage strategy (True = Optimal, False = Random)

        returns:
          recipe -- A recipe name. If the usage strategy 'Optimal' has been selected (take_best == True) then the recipe with the highest readiness value as calculated in calculate_readiness will be returned - otherwise a random recipe will be returned.
          None -- if none of the the recipes has a readiness value of 0.1 or above or no recipe complying to the diet specification is available
          """

        # obtain a list of recipes associated to a readiness value
        recipe_readiness = self.get_readiness_of_recipes(
            recipes=self.recipes, diet=diet)
        if len(recipe_readiness.keys()) == 0: 
            return None

        # order the recipes in descending order according to the readiness values, i.e., the first recipe in the list is the one with the highest readiness value
        sorted_recipes = [k for k, v in sorted(
            recipe_readiness.items(), key=lambda item: item[0])]

        # determine which recipe to return according to the item usage mode
        selected_recipe_index = 0
        if take_best:
            selected_recipe_index = random.randint(0, len(sorted_recipes)-1)

        # determine the recipe name and retrieve the recipe from the list of recipes to return it
        selected_recipe_name: str = sorted_recipes[selected_recipe_index]
        return selected_recipe_name
        

    def get_recipe_by_name(self, recipe_name: str) -> dict:
      selected_recipe = [recipe for recipe in self.recipes if recipe['name'] == recipe_name][0]
      return selected_recipe