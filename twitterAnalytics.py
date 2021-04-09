import re, json, operator
#from mpi4py import MPI


# make dictionary of words and their scores from AFINN.txt
words_file = open('AFINN.txt','r').readlines()
sentimentDict = {}
for line in words_file:
    word,score = line.strip().split("\t")
    sentimentDict[word]=[score]
#print(sentimentDict['lol'])


# Make dictionary for the grid info 
grid_json = open('melbGrid.json')
grid_dict = json.load(grid_json) #this makes a dictionary out of the json
# { "type": "Feature"
#   "properties": { "id": "A1", "xmin": 144.700000, "xmax": 144.850000, "ymin": -37.650000, "ymax": -37.500000 }
#   "geometry": { "type": "Polygon", "coordinates": [ [ [ 144.7, -37.5 ], [ 144.85, -37.5 ], [ 144.85, -37.65 ], [ 144.7, -37.65 ], [ 144.7, -37.5 ] ] ] } },

# for i in grid_dict['features']:
#     print(i['properties']['id'] + "\n")
    
# Make list for the twitter info 
twt_json = open('tinyTwitter.json', encoding='utf-8')
data = json.load(twt_json) #this makes a dictionary out of the json
twt_arr = []
for i in data["rows"]:
    # print(i["id"])
    twt_dict[]
    
    # we only want to use the tweet text and location (lat,long)
    
#print(data["rows"])
    #twt_dict = {}
    
#print(json.dumps(tweets_dict, indent = 4, sort_keys=True))
# for i in tweets_dict:
#     print(i)
    
    
    
    
    
