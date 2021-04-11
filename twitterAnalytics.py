import json, ijson
#from mpi4py import MPI

############## I HAVEN"T HANDLED THE EDGE CASES################
def check_grid(coordinates, grid_arr):
    #grid_arr is [[id, xmin, xmax, ymin, ymax, totalTweets, totalScore],..,[]]
    #coordinates is [lat,long]
    for index, val in enumerate(grid_arr):
        if val[1] <= coordinates[0] and coordinates[0] <= val[2]:
            # the latitude is within range
            if val[3] <= coordinates[1] and coordinates[1] <= val[4]:
                # the longitude is within range
                return index 
                # grid found
                
### Make dictionary of words and their scores from AFINN.txt
###
words_file = open('AFINN.txt','r').readlines()
sentimentDict = {}
for line in words_file:
    word,score = line.strip().split("\t")
    sentimentDict[word]=[score]
#print(sentimentDict['lol'])
###



### Make 2d list for the grid info
###
grid_json = open('melbGrid.json')
data1 = json.load(grid_json) #make JSON object from file: key/value pairs
grid_arr = []
for i in data1["features"]:
    grid_arr.append([i["properties"]["id"], i["properties"]["xmin"], i["properties"]["xmax"], i["properties"]["ymin"], i["properties"]["ymax"], 0, 0])
# grid_arr is [[id, xmin, xmax, ymin, ymax, totalTweets, totalScore],..,[]]

# test print
# for i in grid_arr:
#     print(i)
#     print("\n")
###


### Tweets analysed tweet by tweet
###
twt_json = open('tinyTwitter.json', encoding='utf-8')
data2 = json.load(twt_json) # make JSON object: key/value pairs
coordinates = [] # [lat,long]
text = []
for i in data2["rows"]:
    coordinates = i["value"]["geometry"]["coordinates"]
    text = i["doc"]["text"]
    score = 0
    # print(coordinates)
    # print("\n")
    print(text)
    print("\n")
    # note that text for tweets is stored twice. Other location is i["value"]["properties"]["text"]
    # the one I chose to parse is cleaner
    
    # check which grid
    grid_index = check_grid(coordinates, grid_arr)
    #print(grid_index)
    
    # check the words
    x = text.split(" ")
    # for j in x:
        
    # rstrip("!,?.'")
    # rstrip('"')
    
    grid_arr[grid_index][5] += 1 #increment total tweets
    # update grid totalScore
    









