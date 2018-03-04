import json
from bs4 import BeautifulSoup
import urllib.request

def parseRecipes(url):
    recipePage = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(recipePage)
    
    return soup

def getRecipeName(soup):
    name = soup.find("h1",{"itemprop":"name"})
    return name.text

def getRecipeRating(soup):
    rating = soup.find("meta", {"itemprop":"ratingValue"})['content']
    return rating

def getIngredients(soup):
    ingredients = []
    temp = soup.find_all("span",{"itemprop":"ingredients"})
    for i in temp:
        ingredients.append(i.text)
        
    return ingredients

def getDirections(soup):
    directions = []
    temp = soup.find_all("span", {"class":"recipe-directions__list--item"})
    for i in temp:
        directions.append(i.text)
        
    return directions



a = parseRecipes("https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/")

print(getRecipeName(a))
print(getRecipeRating(a))
print(getIngredients(a))
print()

for i in getDirections(a):
    print(i)