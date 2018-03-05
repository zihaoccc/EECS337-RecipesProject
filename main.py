# -*- coding: utf-8 -*-
from modules import parse_recipe

import pprint
pp = pprint.PrettyPrinter(indent=2)

## TEST
ingr, dirs = parse_recipe('https://www.allrecipes.com/recipe/212451/enchanted-sour-cream-chicken-enchiladas/')
pp.pprint(ingr)
pp.pprint(dirs)