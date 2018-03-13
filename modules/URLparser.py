# -*- coding: utf-8 -*-
# adapted from https://realpython.com/blog/python/python-web-scraping-practical-introduction/

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from .ingredientParser import Ingredient
from .directionParser import process_direction


def get_url(url):
    '''
    Makes an HTTP GET request to and returns text/xml content if
    response is good, else returns None and tries to log error
    '''
    try:
        with closing(get(url, stream=True)) as res:
            if is_good_response(res):
                return res.content
            else:
                return None
    except RequestException as e:
        print('Error during requests to {0} : {1}', format(url, str(e)))
        return None

def is_good_response(res):
    '''
    Performs check to response element ensuring we got a
    good response from the HTML GET request
    '''
    content_type = res.headers['Content-Type'].lower()
    return (res.status_code == 200 and 
            content_type is not None and
            content_type.find('html') > -1)


def parse_recipe(url):
    '''
    Gets the html content of the recipe website

    '''
    # init return vars
    preprocessed_recipe = {}
    ingredients = []
    instructions = []
    tools = []
    primary_methods = []
    secondary_methods = []

    # get html
    recipe_html = get_url(url)
    if recipe_html is not None:
        html = BeautifulSoup(recipe_html, 'html.parser')
        servingSize = html.find("meta", {"itemprop":"recipeYield"})['content']
        preprocessed_recipe['serving_size'] = servingSize

        # get instructions
        for elem in html.select('.recipe-directions__list--item'):
            if len(elem.text) == 0:
                # last li element not a direction
                break
            instructions.append(elem.text)
            tools, primary_methods, secondary_methods = process_direction(elem.text)
         
        preprocessed_recipe['instructions'] = instructions
        tools = set(tools)
        preprocessed_recipe['tools'] = tools
        primary_methods = set(primary_methods)
        preprocessed_recipe['primary_methods'] = primary_methods
        secondary_methods = set(secondary_methods)
        preprocessed_recipe['secondary_methods'] = secondary_methods
        
        
        # get ingredients
        for elem in html.select('.recipe-ingred_txt'):
            ## TODO: need to process ingredient here
            if elem['class'].pop() == 'white':
                # last li element not an ingredient
                break
            processed_ingredient = Ingredient(elem.text, instructions).get_object()
            ingredients.append(processed_ingredient)
       
        # insert ingredient data into recipe json
        preprocessed_recipe['ingredients'] = ingredients
        
    return preprocessed_recipe


def get_whole_recipe_steps():
    preprocessed_recipe = parse_recipe('https://www.allrecipes.com/recipe/25200/slow-cooker-beef-stew-iv')
    ingredients = preprocessed_recipe['ingredients']
    tools = preprocessed_recipe['tools']
    primary_methods = preprocessed_recipe['primary_methods']
    secondary_methods = preprocessed_recipe['secondary_methods']
    instructions = preprocessed_recipe['instructions']
    
    print(ingredients)
    print(tools)
    print(primary_methods)
    print(secondary_methods)
    for i in instructions:
        print(i)
    return preprocessed_recipe