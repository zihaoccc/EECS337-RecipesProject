# -*- coding: utf-8 -*-
from modules import parse_recipe

import pprint
pp = pprint.PrettyPrinter(indent=2)

## TEST
preprocessed_recipe = parse_recipe('https://www.allrecipes.com/recipe/212451/enchanted-sour-cream-chicken-enchiladas/')
pp.pprint(preprocessed_recipe['ingredients'])
print(preprocessed_recipe['serving_size'])
print(preprocessed_recipe['tools'])
print(preprocessed_recipe['primary_methods'])
print(preprocessed_recipe['secondary_methods'])