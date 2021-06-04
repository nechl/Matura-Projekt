import json
  
# Opening JSON file
f = open('data_recipe.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data['recipe']:
    print(i)
  
# Closing file
f.close()