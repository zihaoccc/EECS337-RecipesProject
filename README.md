# EECS 337 Recipes Project (Group 10)

### Authors
Matt Nicholson, Megan Conlon, Yannick Mamudo, Zihao Chen

### Environment
Python 3

### Install dependencies
``` $ pip install -r requirements.txt ```
``` $ python -m nltk.downloader wordnet ```
NOTE: use python3 and pip3 if you dont have the default python set to Python3

### Run program
``` $ python main.py ```

### In Program
You will be prompted for a valid recipe URL from AllRecipes.com 
Next, the program will print the ingredients object, set of tools, set of cooking methods and directions.
Then, you will be asked whether you want to perform a transformation, and prompted to input a valid number corresponding to a transformation.
(Possible) if our program encounters ingredients missing from our knowledge base we will prompt you on whether you want to add this, and how you categorise it. This helps our program learn and perform better in future transformations.
Lastly, the program will print the whole transformed recipe.