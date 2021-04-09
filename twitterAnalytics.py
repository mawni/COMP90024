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
    twt_arr.append([i["value"]["geometry"]["coordinates"][0], i["value"]["geometry"]["coordinates"][1], i["doc"]["text"]])
    # only take in the latitude, longitude, and tweet text. Put into array
    # note that text for tweets is stored twice. Other location is i["value"]["properties"]["text"]
#twt_arr[[lat,long,text],..[]]

# conduct analysis on each tweet
for i in twt_arr:
    1==1
print("\n" + "number of tweets = " + str(len(twt_arr)))