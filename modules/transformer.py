import copy
import json
import re
from .URLparser import print_recipe

#with open("../parsedRecipe.json") as json_data:
#    recipe_data = json.load(json_data)
#    # print(recipe_data)

def reload_kb():
    with open("./categories.json") as json_data:
        ingredient_kb = json.load(json_data)
    return ingredient_kb

def ask_user(recipe):
    possible_transformation = ["to vegan", "to vegetarian", "to meaty", "to healthy", "to southern", "to mexican", "to italian", "no change"]
    
    print ("Please input the number of the transformation from the list below:")
    for i in range(len(possible_transformation)):
        print(str(i+1) + '. ' + possible_transformation[i])
    response = int(input())
    while (True):
        if response >= 1 and response <= len(possible_transformation):
            break;
        print("input is invalid, please input a number again: ")
        response = int(input())
        
    print("Transforming this recipe "+possible_transformation[response-1])
    transform_recipe(possible_transformation[response-1], recipe)
    

def transform_recipe(dimension, old_recipe):
    """
    
    """
    new_recipe = copy.deepcopy(old_recipe)
    ingredient_kb = reload_kb()

    # pick what transformations to make based on the dimension passed in    
    if dimension == "to vegan":
        #animal products -> alternatives
        new_recipe = toVegan(new_recipe, ingredient_kb)
        
    elif dimension == "to vegetarian":
        # meat_protein -> veggie_protein
        new_recipe = toVegetarian(new_recipe, ingredient_kb)
    
    
    elif dimension == "to meaty":
        # veggie -> bacon, double amount of meat
        new_recipe = toMeaty(new_recipe, ingredient_kb)

    elif dimension == "to healthy":
        # less oil/butter/etc
        #TO-DO
        new_recipe = toHealthy(new_recipe, ingredient_kb)

    elif dimension == "to southern":
        # add gravy
        #TO-DO
        new_recipe = toSouthern(new_recipe, ingredient_kb)
    elif dimension == "to mexican":
        # replace cheese with cojita
        # replace a spice with chili powder
        #TO-DO
        new_recipe = toMexican(new_recipe, ingredient_kb)
    elif dimension == "to italian":
        # add olive oil
        # cheese to parm
        #TO-DO
        new_recipe = toItalian(new_recipe, ingredient_kb)
    else:
        print("you dunce. You never specified a transformation.")
        


    print_recipe(new_recipe)


## TRANSFORMATION HELPERS
def toVegan(new_recipe, ingredient_kb):
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        if ingredient_flag:
            for category in ingredient_kb[ingredient]["category"]:
                if category == "non vegan":
                    new_ingredient = str(ingredient_kb[ingredient]["substitutions"]["to vegan"])
                    new_recipe["ingredients"][i]["name"] = new_ingredient
                    new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
                #new_recipe = #HELPER FUNCTION look for ingredient, swap out with ingredient_kb[ingredient]["substitutions"]["to vegan"]
                if category == "meat":
                    new_ingredient = str(ingredient_kb[ingredient]["substitutions"]["to vegetarian"])
                    new_recipe["ingredients"][i]["name"] = new_ingredient
                    new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
    return new_recipe

def toVegetarian(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True 
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        if ingredient_flag:
            for category in ingredient_kb[ingredient]["category"]:
                if category == "meat":
                    new_ingredient = str(ingredient_kb[ingredient]["substitutions"]["to vegetarian"])
                    new_recipe["ingredients"][i]["name"] = new_ingredient
                    new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
    return new_recipe

def toMeaty(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        if ingredient_flag:
            for category in ingredient_kb[ingredient]["category"]:
                if category == "veggie":
                    new_ingredient = "bacon"
                    new_recipe["ingredients"][i]["name"] = new_ingredient
                    new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
                if category == "meat":
                    new_quantity =  str(2 * new_recipe["ingredients"][i]["quantity"])
                    new_recipe["ingredients"][i]["quantity"] =   new_quantity
                    new_recipe = swap_ingredients_in_directions(new_recipe, str(new_recipe["ingredients"][i]["quantity"]), str(new_quantity))
    return new_recipe

def toHealthy(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        #catch individual ingredient
        if ingredient_flag:
            if ingredient == ("butter" or "sugar" or "oil" or "salt"):
                new_quantity = round(new_recipe["ingredients"][i]["quantity"] / 2.0, 2)
                new_recipe["ingredients"][i]["quantity"] =  new_quantity
                new_recipe = swap_ingredients_in_directions(new_recipe, str(new_recipe["ingredients"][i]["quantity"]), str(new_quantity))
        #catch other cases 
            for category in ingredient_kb[ingredient]["category"]:
                if category == ("non healthy" or "oil" or "sugar") :
                    new_quantity = round(new_recipe["ingredients"][i]["quantity"] / 2.0, 2)
                    new_recipe["ingredients"][i]["quantity"] =  new_quantity
                    new_recipe = swap_ingredients_in_directions(new_recipe, str(new_recipe["ingredients"][i]["quantity"]), str(new_quantity))
    return new_recipe


def toSouthern(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        if ingredient_flag:
            if not ingredient_kb[ingredient]["substitutions"]["to southern"] == "":
                new_ingredient = str(ingredient_kb[ingredient]["substitutions"]["to southern"])
                new_recipe["ingredients"][i]["name"] = new_ingredient
                new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
        """
         for category in ingredient_kb[ingredient]["category"]:
            if category == "non healthy":
                new_recipe["ingredients"][i]["name"] = str(ingredient_kb[ingredient]["substitutions"]["to healthy"])
        """      
    return new_recipe
    
    
def toMexican(new_recipe, ingredient_kb):
    
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        if ingredient_flag:
            if not ingredient_kb[ingredient]["substitutions"]["to mexican"] == "":
                new_ingredient = str(ingredient_kb[ingredient]["substitutions"]["to mexican"])
                new_recipe["ingredients"][i]["name"] = new_ingredient
                new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
    return new_recipe

def toItalian(new_recipe, ingredient_kb):
    for i in range(len(new_recipe["ingredients"])):
        ingredient_flag = True
        ingredient = str(new_recipe["ingredients"][i]["name"]).lower()
        if ingredient not in ingredient_kb:
            ingredient_flag = add_ingredient_kb(ingredient, ingredient_kb)
            ingredient_kb = reload_kb()
        if ingredient_flag:
            if not ingredient_kb[ingredient]["substitutions"]["to italian"] == "":
                new_ingredient = str(ingredient_kb[ingredient]["substitutions"]["to italian"])
                new_recipe["ingredients"][i]["name"] = new_ingredient
                new_recipe = swap_ingredients_in_directions(new_recipe, ingredient, new_ingredient)
    return new_recipe
    
    
## ADD TO INGREDIENTS_KB
def add_ingredient_kb(name, kb):
    categories = ['protein', 'meat', 'vegetarian', 'dairy', 'veggie',  'non vegan', 'spice', 'oil']
    styles = ['italian', 'mexican', 'southern']

    print()
    answer = input("Do you want to add "+ name + " to the knowledge base? [y or n] ")

    if answer == 'n':
        return False


    print("What category (or categories) is this ingredient? Write your answer as a list of numbers separated by a space. (Press Enter to skip)")
    print("1: protein\n2: meat\n3: vegetarian\n4: dairy\n5: veggie\n6: non vegan\n7: spice\n8: oil")
    print("e.g. given chicken, input: 1 2 6")
    category_input = input().split(" ")
    ingredient_category = []

    while(True):
        if category_input[0] == '':
            break
        
        for num in category_input:
            if num.isdigit() and int(num) > 0 and int(num) <= len(categories):
                ingredient_category.append(categories[int(num)-1])
            else:
                print("Wrong input please try again")
                category_input = input().split(" ")
                ingredient_category = []
                continue
        break


    print("In what style of cooking would you find this ingredient? Write your answer as a list of numbers separated by a space. (Press Enter to skip)")
    print("1: italian \n2: mexican \n3: southern")
    print("e.g. given pasta, input: 1")
    styles_input = input("").split(" ")
    ingredient_styles = []

    while(True):
        if styles_input[0] == '':
            break
        
        for num in styles_input:
            if num.isdigit() and int(num) > 0 and int(num) <= len(styles):
                ingredient_styles.append(styles[int(num)-1])
            else:
                print("Wrong input please try again")
                styles_input = input().split(" ")
                ingredient_styles = []
                continue
        break
    
    substitutes = {}
    for dimension in ["to vegan", "to vegetarian", "to healthy", "to southern", "to mexican", "to italian"]:
        response = input("What is a substitute for "+ name +" if you were to change this "+ dimension+"? (Press enter to skip) ")
        substitutes[dimension] = response
     
    new_ingredient = {}
    new_ingredient["category"] = ingredient_category
    new_ingredient["styles"] = ingredient_styles
    new_ingredient["substitutions"] = substitutes
    
    kb[name] = new_ingredient
        
    with open('./categories.json', 'w') as outfile:
        json.dump(kb, outfile, indent=4, sort_keys=True)

    return True

def swap_ingredients_in_directions(recipe, old_ingredient, new_ingredient):

    for idx, direction in enumerate(recipe["instructions"]):
        insensitive_ingredient = re.compile(old_ingredient, re.IGNORECASE)
        new_direction = insensitive_ingredient.sub(new_ingredient, direction)
        recipe["instructions"][idx] = new_direction

    return recipe
