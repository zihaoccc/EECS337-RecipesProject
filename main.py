# -*- coding: utf-8 -*-
from modules import parse_recipe

import pprint
pp = pprint.PrettyPrinter(indent=2)

## TEST
preprocessed_recipe = parse_recipe('https://www.allrecipes.com/recipe/8894/chicken-divan')
pp.pprint(preprocessed_recipe['ingredients'])
pp.pprint(preprocessed_recipe['instructions'])
pp.pprint(preprocessed_recipe['serving_size'])
pp.pprint(list(preprocessed_recipe['tools']))
pp.pprint(list(preprocessed_recipe['primary_methods']))
pp.pprint(list(preprocessed_recipe['secondary_methods']))
