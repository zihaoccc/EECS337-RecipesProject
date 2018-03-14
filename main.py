# -*- coding: utf-8 -*-
from modules import parse_recipe, print_recipe, ask_user

# Prompt for url and get recipe 
url = input('Input url for recipe: ') 
recipe = parse_recipe(url) 
print_recipe(recipe)

# Ask user for possible transformations
ask_user(recipe)