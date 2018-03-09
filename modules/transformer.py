import copy
import json


with open("../parsedRecipe.json") as json_data:
    recipe_data = json.load(json_data)
    # print(recipe_data)

with open("../categories.json") as json_data:
    ingredient_kb = json.load(json_data)

def ask_user(recipe):
    
    for possible_transformation in ["to vegan", "to vegetarian", "to meaty", "to healthy", "to southern", "to mexican", "to italian","double the amount", "at all"]:
        response = input("Would you like to transform this recipe "+ possible_transformation + "? [y or n] \t")
        
        if response == "y":
            break
         
    print(possible_transformation)
    transform_recipe(possible_transformation, recipe)
    

def transform_recipe(dimension, old_recipe):
    """
    
    """
    new_recipe = copy.deepcopy(old_recipe)


    # pick what transformations to make based on the dimension passed in    
    if dimension == "to vegan":
         # meat_protein -> veggie_protein
        new_recipe = toVegetarian(new_recipe, ingredient_kb)
        #animal products -> alternatives
        new_recipe = toVegan(new_recipe, ingredient_kb)
         
    
    elif dimension == "to vegetarian":
        # meat_protein -> veggie_protein
        new_recipe = toVegan(new_recipe, ingredient_kb)
    
    
    elif dimension == "to meaty":
        # veggie -> bacon, double amount of meat
        new_recipe = toMeaty(new_recipe, ingredient_kb)

    elif dimension == "to healthy":
        # less oil/butter/etc
        #TO-DO
        pass

    elif dimension == "to southern":
        # add gravy
        #TO-DO
        pass
    elif dimension == "to mexican":
        # replace cheese with cojita
        # replace a spice with chili powder
        #TO-DO
        pass
    elif dimension == "to italian":
        # add olive oil
        # cheese to parm
        #TO-DO
        pass
    else:
        print("you dunce. You never specified a transformation.")
        

    print(new_recipe)


## TRANSFORMATION HELPERS
def toVegan(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient = str(new_recipe["ingredients"][i]["name"])
        if ingredient not in ingredient_kb:
            add_ingredient_kb(ingredient, ingredient_kb)
        for category in ingredient_kb[ingredient]["category"]:
            if category == "non_vegan":
                new_recipe["ingredients"][i]["name"] = str(ingredient_kb[ingredient]["substitutions"]["to vegan"])
    return new_recipe

def toVegetarian(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient = str(new_recipe["ingredients"][i]["name"])
        if ingredient not in ingredient_kb:
            add_ingredient_kb(ingredient, ingredient_kb)
        for category in ingredient_kb[ingredient]["category"]:
            if category == "meat":
                new_recipe["ingredients"][i]["name"] = str(ingredient_kb[ingredient]["substitutions"]["to vegetarian"])
    return new_recipe

def toMeaty(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient = str(new_recipe["ingredients"][i]["name"])
        if ingredient not in ingredient_kb:
            add_ingredient_kb(ingredient, ingredient_kb)
        for category in ingredient_kb[ingredient]["category"]:
            if category == "veggie":
                new_recipe["ingredients"][i]["name"] = "bacon"
            if category == "protein":
                new_recipe["ingredients"][i]["name"] = str(ingredient_kb[ingredient]["substitutions"]["to meaty"])

    # TO-DO need to add double quantity of meat


    return new_recipe


## ADD TO INGREDIENTS_KB
def add_ingredient_kb(name, kb):
    answer = input("Do you want to add "+ name + " to the knowledge base? [y or n] \t")

    if answer == 'n':
        return

    category = eval(input("What category (or categories) is this ingredient? Write your answer as a list containing ['protein', 'meat | vegetarian', 'dairy', 'veggie | non vegan'] \t"))
    styles = eval(input("In what style of cooking would you find is ingredient? Write your answer as a list ['italian', 'mexican', 'southern'] \t "))
    
    substitutes = {}
    for dimension in ["to vegan", "to vegetarian", "to healthy", "to southern", "to mexican", "to italian"]:
        response = input("What is a substitute for "+ name +" if you were to change this "+ dimension+"?: \t")
        substitutes[dimension] = response
     
    new_ingredient = {}
    new_ingredient["category"] = category
    new_ingredient["styles"] = styles
    new_ingredient["substitutions"] = substitutes
    
    kb[name] = new_ingredient
        
    with open('../categories.json', 'w') as outfile:
        json.dump(kb, outfile, indent=4, sort_keys=True)

ask_user(recipe_data)
