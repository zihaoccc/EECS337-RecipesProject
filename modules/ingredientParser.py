# -*- coding: utf-8 -*-
import spacy
nlp = spacy.load('en')

# hardcoded sets
measurement_types = {'cup', 'tablespoon', 'teaspoon', 'pint', 'ounce', 'quart', 'gallon', 'pound', 'dash', 'pinch', 'clove', 'piece', 'stalk', 'can'}
measurement_abbr_mapping = {'t':'teaspoon','tsp':'teaspoon','T':'tablespoon','Tbsp':'tablespoon','c':'cup','oz':'ounce','pt':'pint','qt':'quart',
							'gal':'gallon','lb':'pound','#':'pound'}

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

    ingredient_obj['preparation'] = extract_preparation(ingredient_line)
    ingredient_obj['quantity'], ingredient_obj['measurement'] = extract_quantity_measurement(ingredient_line)

    return ingredient_obj


def extract_preparation(ingredient_line):
    ''' Extract preparation phrase from ingredient line if it exists '''
    # last phrase in ingredient line after a dash or a comma is usually a preparation directive
    if ingredient_line.find(' - ') > -1:
        split_by_dash = ingredient_line.split(' - ')
        return split_by_dash.pop()
    elif ingredient_line.find(', ') > -1:
        split_by_comma = ingredient_line.split(',')
        if len(split_by_comma) > 1:
            return split_by_comma.pop().strip()
    
    return None
    

def extract_quantity_measurement(ingredient_line):
    ''' Extract quantity and measurement type from ingredient line if it exists '''
    # e.g. 1 tablespoon, 12 ounces, 1 (1 pound) steak
    # init vars
    quantity = None
    measurement_type = None

    split_by_space = ingredient_line.split(' ')

    if split_by_space[0][0].isdigit():
        # get quantity
        if split_by_space[0].find('/') > -1:
            split_by_slash = split_by_space[0].split('/')
            quantity = float(split_by_slash[0]) / float(split_by_slash[1])
        else:
            quantity = float(split_by_space[0])

        # get measurement type
        potential_measurement = '' if len(split_by_space) < 2 else split_by_space[1]
        potential_measurement_lemmatized = nlp(potential_measurement)[0].lemma_
        if potential_measurement_lemmatized in measurement_types:
            measurement_type = potential_measurement_lemmatized
        
        return quantity, measurement_type
    else:
        return None, None

def extract_name(ingredient_line):
    pass

def extract_descriptor(ingredient_line):
    pass