# -*- coding: utf-8 -*-
# adapted from https://realpython.com/blog/python/python-web-scraping-practical-introduction/

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

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
    ingredients = []
    instructions = []

    # get html
    recipe_html = get_url(url)
    if recipe_html is not None:
        html = BeautifulSoup(recipe_html, 'html.parser')

        # get ingredients
        for elem in html.select('.recipe-ingred_txt'):
            ## TODO: need to process ingredient here
            ingredients.append(elem.text)
        
        # get instructions
        for elem in html.select('.recipe-directions__list--item'):
            instructions.append(elem.text)
    
    return ingredients, instructions

def process_ingredient(ingredient_line):
    '''
    Given an ingredient line, splits the content
    into relevant ingredient categories
    '''

    ingredient_obj = {
        'name': None, 
        'quantity': None, 
        'measurement': None, 
        'descriptor': None, 
        'preparation': None
    }

    

    return ingredient_obj


## TEST
parse_recipe('https://www.allrecipes.com/recipe/80827/easy-garlic-broiled-chicken')