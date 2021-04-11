import json, ijson
#from mpi4py import MPI


# make dictionary of words and their scores from AFINN.txt
words_file = open('AFINN.txt','r').readlines()
sentimentDict = {}
for line in words_file:
    word,score = line.strip().split("\t")
    sentimentDict[word]=[score]
#print(sentimentDict['lol'])



# Make 2d list for the grid info 
grid_json = open('melbGrid.json')
data1 = json.load(grid_json) #make JSON object from file: key/value pairs
grid_arr = []
for i in data1["features"]:
    grid_arr.append([i["properties"]["id"], i["properties"]["xmin"], i["properties"]["xmax"], i["properties"]["ymin"], i["properties"]["ymax"]])
# grid_arr is [[id, xmin, xmax, ymin, ymax],..,[]]

# test print
# for i in grid_arr:
#     print(i)
#     print("\n")


# Make 2d list for twitter info 
twt_json = open('tinyTwitter.json', encoding='utf-8')
data2 = json.load(twt_json) #make JSON object: key/value pairs
twt_arr = []
for i in data2["rows"]:
    twt_arr.append([i["value"]["geometry"]["coordinates"][0], i["value"]["geometry"]["coordinates"][1], i["doc"]["text"]])
    # note that text for tweets is stored twice. Other location is i["value"]["properties"]["text"]
    # the one I chose to parse is cleaner
#twt_arr is [[lat,long,text],..,[]]

# test print
# for i in twt_arr:
#     print(i)
#     print("\n")
# print("\n" + "number of tweets = " + str(len(twt_arr)))

# conduct analysis on each tweet
for i in twt_arr:
    1==1