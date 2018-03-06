import copy
import json


def ask_user(recipe):
    
    for possible_transformation in ["to vegan", "to vegatarian", "to meaty", "to healthy", "to southern", "to mexican", "to italian","double the amount", "at all"]:
        response = input("Would you like to transform this recipe "+possible_transformation + "? [y or n] \t")
        
        if response == "y":
            break
        
        
        
    print(possible_transformation)
    transform_recipe(possible_transformation, recipe)
    

def transform_recipe(dimension, old_recipe):
    """
    
    """
    new_recipe = copy.deepcopy(old_recipe)

    changes_to_make = {} # a dictionary that with ("from tag", "to tag")


    # pick what transformations to make based on the dimension passed in    
    if dimension == "to vegan":
        # meat_protein -> veggie_protein
        # animal product -> not that
        
        pass
    
    elif dimension == "to vegatarian":
         # meat_protein -> veggie_protein
        changes_to_make["meat_protein"] = "veg_protein"
        pass
    
    
    elif dimension == "to meaty":
         # veggie_protein -> meat_protein 
        # add bacon
        # double amount of meat

        pass
    elif dimension == "to healthy":
        # less oil/butter/etc

        pass
    elif dimension == "to southern":
        # add gravy
        pass
    elif dimension == "to mexican":
        # replace sausage with chorizo
        # replace cheese with cojita
        # replace a spice with chili powder
        pass
    elif dimension == "to italian":
        # add olive oil
        # cheese to parm

        pass
    else:
        print("you dunce. You never specified a transformation.")
        return


    # changes = changes_to_make.keys()
    # making a lot of assumptions on the structure
    for ingredient in old_recipe["ingredients"]:
        
        if ingredient["tag"] is in changes:
            # make the change
            new_ingredient = 
            
            
            thing = new_recipe.pop(ingredient, None)

            # create a new ingredients object here

            # then add the new thing to the new_recipe