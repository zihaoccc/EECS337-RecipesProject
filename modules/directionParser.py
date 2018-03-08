import string

TOOLS_WORDS = ['pan', 'bowl', 'baster', 'saucepan', 'knife', 'beanpot', 'chip','pan', 'cookie', 'sheet', 'cooking', 'pot', 'crepe', 'pan', 'double', 'boiler', 
               'doufeu', 'dutch', 'oven', 'food', 'processor', 'frying', 'skillet', 'griddle', 'karahi', 'kettle', 'pressure' 'cooker', 'ramekin', 'roasting', 
               'roasting', 'rack', 'splayed', 'saute','souffle', 'dish', 'springform', 'stockpot', 'tajine', 'tube', 'panwok', 	
               'wonder', 'apple', 'corer', 'cutter', 'baster', 'biscuit', 'biscuit' 'press', 'baking', 'bread', 'browning', 'tray', 	
               'butter', 'curler', 'cake', 'and', 'pie', 'server', 'cheese', 'cheesecloth', 'cherry', 'pitter', 'chinoise', 'cleaver', 'corkscrew', 
               'cutting', 'board', 'dough', 'scraper', 'egg', 'poacher', 'separator', 'slicer', 'timer', 'fillet', 'fish', 'scaler', 'slice', 
               'flour', 'sifter', 'food', 'mill', 'funnel', 'garlic', 'press', 'grapefruit', 'grater', 'gravy', 'strainer', 'ladle', 'lame', 'lemon', 'reamer', 
               'squeezer', 'mandoline', 'mated', 'colander', 'measuring', 'cup', 'measuring', 'spoon', 'grinder', 'tenderiser', 'thermometer', 'melon', 'baller',
               'mortar', 'pestle', 'nutcracker', 'nutmeg', 'grater', 'glove', 'blender', 'fryer', 'pastry', 'bush', 'wheel', 'peeler', 'pepper', 
               'pizza', 'masher', 'potato' ,'ricer', 'pot-holder', 'rolling', 'pin', 'salt', 'shaker', 'sieve', 'fork', 'spatula', 'spider', 'tin', 'opener',
               'tongs', 'whisk', 'wooden', 'zester', 'microwave', 'cylinder', 'Aluminum' ,'foil', 'steamer', 'shallow', 'glass', 'broiler', 'wok']
TOOLS = ['pan', 'bowl', 'baster', 'saucepan', 'knife', 'oven', 'beanpot', 'chip pan', 'cookie sheet', 'cooking pot', 'crepe pan', 'double boiler', 'doufeu', 	
         'dutch oven', 'food processor', 'frying pan', 'skillet', 'griddle', 'karahi', 'kettle', 'pan', 'pressure cooker', 'ramekin', 'roasting pan', 
         'roasting rack', 'saucepansauciersaute pan', 'splayed saute pan', 'souffle dish', 'springform pan', 'stockpot', 'tajine', 'tube panwok', 	
         'wonder pot', 'pot', 'apple corer', 'apple cutter', 'baster', 'biscuit cutter', 'biscuit press', 'baking dish', 'bread knife', 'browning tray', 	
         'butter curler', 'cake and pie server', 'cheese knife', 'cheesecloth', 'knife', 'cherry pitter', 'chinoise', 'cleaver', 'corkscrew', 
         'cutting board', 'dough scraper', 'egg poacher', 'egg separator', 'egg slicer', 'egg timer', 'fillet knife', 'fish scaler', 'fish slice', 
         'flour sifter', 'food mill', 'funnel', 'garlic press', 'grapefruit knife', 'grater', 'gravy strainer', 'ladle', 'lame', 'lemon reamer', 
         'lemon squeezer', 'mandoline', 'mated colander pot', 'measuring cup', 'measuring spoon', 'grinder', 'tenderiser', 'thermometer', 'melon baller',
         'mortar and pestle', 'nutcracker', 'nutmeg grater', 'oven glove', 'blender', 'fryer', 'pastry bush', 'pastry wheel', 'peeler', 'pepper mill', 
         'pizza cutter', 'masher', 'potato ricer', 'pot-holder', 'rolling pin', 'salt shaker', 'sieve', 'spoon', 'fork', 'spatula', 'spider', 'tin opener',
         'tongs', 'whisk', 'wooden spoon', 'zester', 'microwave', 'cylinder', 'Aluminum foil', 'steamer', 'broiler rack', 'grate', 'shallow glass dish', 'wok', 
         'dish', 'broiler tray']

PRIMARY_COOKING_METHODS = ['bake', 'steam', 'grill', 'roast', 'boil', 'fry', 'barbeque', 'baste', 'broil', 'poach', 'freeze', 'cure', 'saute']
SECONDARY_COOKING_METHODS = ['chop', 'grate', 'cut', 'shake', 'mince', 'stir', 'mix', 'crush', 'squeeze', 'beat', 'blend', 'caramelize', 'dice', 'dust',
                             'glaze', 'knead', 'pare', 'shred', 'toss', 'whip', 'sprinkle', 'grease', 'arrange', 'microwave', 'coat', 'turning','preheat', 
                             'broil', 'marinate', 'brushing', 'slice']

point_words = ['in', 'In', 'into', 'Into', 'place', 'Place', 'bottom of', 'Bottom of', 'to', 'To', 'place', 'Place', 'top of', 'Top of', 'fill', 'Fill', 'from',
               'From']

tool_list = []
primary_methods = []
secondary_method = []

def process_direction(direction_line):
    words_in_direction = direction_line.split(' ')
    get_tools(words_in_direction) 
    get_methods(words_in_direction)
    return tool_list, primary_methods, secondary_method


def get_tools(words_in_direction):
    for i in range(len(words_in_direction)):
        if ((words_in_direction[i] == 'bottom' or words_in_direction[i] == 'top') and (i < len(words_in_direction))):
            if words_in_direction[i+1] == 'of':
                diff = len(words_in_direction) - 1 - i
                temp = ''
                length = 5
                if (diff < length):
                    length = diff
                isTool = False
                for j in range(1,length+1):
                    cur_word = words_in_direction[i+j].strip(string.punctuation)
                    if cur_word in TOOLS_WORDS:
                        temp += cur_word
                        temp += ' '
                        isTool = True
                    elif isTool == True:                       
                        break
                temp = temp.strip()
                if temp in TOOLS:
                    tool_list.append(temp)                
        elif words_in_direction[i] in point_words:
            diff = len(words_in_direction) - 1 - i
            temp = ''
            length = 5
            if (diff < length):
                length = diff
            isTool = False
            for j in range(1, length+1):
                cur_word = words_in_direction[i+j].strip(string.punctuation)
                if cur_word in TOOLS_WORDS:
                    if cur_word == 'and':
                        if words_in_direction[i+j+1].strip(string.punctuation) not in TOOLS_WORDS:
                            break
                    temp += cur_word
                    temp += ' '
                    isTool = True
                elif isTool == True:                      
                    break
            temp = temp.strip()
            if temp in TOOLS:
                tool_list.append(temp)            

def get_methods(words_in_direction):
    for i in words_in_direction:
        cur_word = i.lower()
        cur_word = cur_word.strip(string.punctuation)
        if cur_word in PRIMARY_COOKING_METHODS:
            primary_methods.append(cur_word)
        elif cur_word in SECONDARY_COOKING_METHODS:
            secondary_method.append(cur_word)
            

def get_steps(words_in_direction):
    pass