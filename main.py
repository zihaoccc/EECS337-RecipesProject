# -*- coding: utf-8 -*-
from modules import parse_recipe
from modules import get_whole_recipe_steps
from modules import ask_user 

import pprint
pp = pprint.PrettyPrinter(indent=2)

## TEST
ask_user(get_whole_recipe_steps())