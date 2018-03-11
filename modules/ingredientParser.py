# -*- coding: utf-8 -*-
import spacy
nlp = spacy.load('en')

# hardcoded sets
measurement_types = {'cup', 'tablespoon', 'teaspoon', 'pint', 'ounce', 'quart', 'gallon', 'pound', 'dash', 'pinch', 'clove', 'piece', 'stalk', 'can'}
measurement_abbr_mapping = {'t':'teaspoon','tsp':'teaspoon','T':'tablespoon','Tbsp':'tablespoon','c':'cup','oz':'ounce','pt':'pint','qt':'quart',
                            'gal':'gallon','lb':'pound','#':'pound'}


class Ingredient:
    def __init__(self, ingredient_line, instructions):
        self.ingredient_line = ingredient_line
        self.instructions = instructions
        self.ingredient_obj = {
            'name': None, 
            'quantity': None, 
            'measurement': None, 
            'descriptor': None, 
            'preparation': None
        }
        self.process_ingredient()
    
    def get_object(self):
        return self.ingredient_obj

    def process_ingredient(self):
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

        self.ingredient_obj['preparation'] = self.extract_preparation()
        self.ingredient_obj['quantity'], self.ingredient_obj['measurement'] = self.extract_quantity_measurement()
        self.ingredient_obj['name'], self.ingredient_obj['descriptor'] = self.extract_name_and_descriptor()

        return ingredient_obj


    def extract_preparation(self):
        ''' Extract preparation phrase from ingredient line if it exists '''
        # last phrase in ingredient line after a dash or a comma is usually a preparation directive
        if self.ingredient_line.find(' - ') > -1:
            split_by_dash = self.ingredient_line.split(' - ')
            self.ingredient_line = split_by_dash[0]
            return split_by_dash.pop()
        elif self.ingredient_line.find(', ') > -1:
            split_by_comma = self.ingredient_line.split(', ')
            if len(split_by_comma) > 1:
                new_line = ", ".join(split_by_comma[:-1])
                prep = split_by_comma.pop().strip()
                
                # try to catch edge cases whereby a comma was just a part of the descriptors
                # e.g. skinless, boneless chicken breast halves
                if len(prep.split(" ")) <= len(new_line.split(" ")):
                    self.ingredient_line = new_line
                    return prep
        
        return None
        

    def extract_quantity_measurement(self):
        ''' Extract quantity and measurement type from ingredient line if it exists '''
        # e.g. 1 tablespoon, 12 ounces, 1 (1 pound) steak
        # init vars
        quantity = None
        measurement_type = None

        split_by_space = self.ingredient_line.split(' ')

        if split_by_space[0][0].isdigit():
            # get quantity
            if split_by_space[0].find('/') > -1:
                split_by_slash = split_by_space[0].split('/')
                quantity = float(split_by_slash[0]) / float(split_by_slash[1])
            else:
                quantity = float(split_by_space[0])
            
            del split_by_space[0]

            # get measurement type
            potential_measurement = split_by_space[0] if split_by_space[0][0] != '(' else split_by_space[2]
            potential_measurement_lemmatized = nlp(potential_measurement)[0].lemma_

            if potential_measurement_lemmatized in measurement_types:
                measurement_type = potential_measurement_lemmatized
                ind = 0 if split_by_space[0][0] != '(' else 2
                del split_by_space[ind]
            
            self.ingredient_line = " ".join(split_by_space)
            return quantity, measurement_type
        else:
            return None, None

    def extract_name_and_descriptor(self):
        ''' Extract ingredient name and descriptors from the ingredient line '''
        descriptor = None
        name = self.ingredient_line

        split_by_space = self.ingredient_line.split(" ")

        # people are so inconsistent when it comes to CHICKEN (Ughh)
        # e.g. chicken breast halved, chicken pieces, chicken meat
        # let's be real unless it's soup or broth, chicken
        if len(split_by_space) > 2:
            chicken_index_from_last = -1
            if (split_by_space[len(split_by_space) - 2] == 'chicken' and
                split_by_space[len(split_by_space) - 1] != 'soup' and
                split_by_space[len(split_by_space) - 1] != 'broth'):
               chicken_index_from_last = 2
            elif split_by_space[len(split_by_space) - 3] == 'chicken':
                chicken_index_from_last = 3
            
            # if found
            if chicken_index_from_last != -1:
                name = split_by_space.pop(len(split_by_space) - chicken_index_from_last)
                descriptor = " ".join(split_by_space)
                return name, descriptor

        # eliminate last two words id they're not part of the ingredient
        # e.g. vegetable oil for frying
        # e.g. salt to taste
        if len(split_by_space) > 2:
            if ( split_by_space[len(split_by_space) - 2] == 'for' or
            split_by_space[len(split_by_space) - 2] == 'taste'):
                split_by_space = split_by_space[:-2]

        # put bracket information in descriptor 
        bracket_stuff = None
        if split_by_space[0][0] == '(':
            bracket_stuff = " ".join(split_by_space[:2])
            split_by_space = split_by_space[2:]
            name = " ".join(split_by_space)

        # find ingredient root name in instructions
        last_found = -1
        for i in range(1, len(split_by_space) + 1):
            test = " ".join(split_by_space[-i:])
            if last_found == -1:
                for idx, instruction in enumerate(self.instructions):
                    if instruction.find(test) > -1:
                        name = test
                        descriptor = " ".join(split_by_space[:len(split_by_space) - i]) 
                        last_found = idx
                        break
                # no hope, forget about it
                if last_found == -1:
                    break
            else:
                # found instruction line
                if self.instructions[last_found].find(test) > -1:
                    name = test
                    descriptor = " ".join(split_by_space[:len(split_by_space) - i]) 
                else:
                    break

        # combine all descriptors found
        if bracket_stuff is not None:
            descriptor = bracket_stuff if (descriptor is None or len(descriptor) == 0) else " ".join([bracket_stuff, descriptor])
        # standardize into None to match preparation
        descriptor = descriptor if (descriptor == None or len(descriptor) > 0) else None

        # all set
        return name, descriptor