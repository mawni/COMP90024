import json, math

### Return the index of the grid of the tweet in grid_arr
###
def check_grid(coordinates, grid_arr):
    #grid_arr is [[id, xmin, xmax, ymin, ymax, totalTweets, totalScore],..,[]]
    #coordinates is [lat,long]
    for index, val in enumerate(grid_arr):
        if val[1] <= coordinates[0] and coordinates[0] <= val[2]:
            # the longitude is within range
            if val[3] <= coordinates[1] and coordinates[1] <= val[4]:
                # the latitude is within range
                if coordinates[1]==val[3]: #equals ymin i.e. minimum latitude
                    if val[0]!="C1" and val[0]!="C2" and ('D' in val[0])==False:
                        continue
                        #tweet latitude is at ymin of grid. 
                        #Skip current loop so that it goes to the grid below where tweet lat = ymax
                        #C1,C2,D3-5 have no cells, below, so don't skip current loop
                return index 
                # grid found
    return None #grid not found
                
                
### Make dictionary of words and their scores from AFINN.txt
###
words_file = open('AFINN.txt','r').readlines()
sentimentDict = {}
for line in words_file:
    word,score = line.strip().split("\t")
    sentimentDict[word]=score
###


### Make 2d list for the grid info
###
grid_json = open('melbGrid.json')
data1 = json.load(grid_json) #make JSON object from file: key/value pairs
grid_arr = []
for i in data1["features"]:
    grid_arr.append([i["properties"]["id"], i["properties"]["xmin"], i["properties"]["xmax"], i["properties"]["ymin"], i["properties"]["ymax"], 0, 0])
# grid_arr is [[id, xmin, xmax, ymin, ymax, totalTweets, totalScore],..,[]]
# note x is longitude, y is latitude


### Tweets analysed tweet by tweet
###
#big_data = open('tinyTwitter.json', encoding='utf-8') #open 1st to get total length
#big_data = big_data.readlines() #skip first line

#length = len(big_data)
length = 20
#print("total length = " + str(length))

big_data = open('tinyTwitter.json', encoding='utf-8') #open 1st to get total length
#big_data = big_data.readlines()[1:] #skip first line

coordinates = [] # [long,lat]
text = []

# def printRanges(length, x):
#     step = length/8
#     readIndexL = math.floor(1 + x*step)
#     readIndexR = math.floor(step*(x+1)+1)
#     #note right index is excluded in the readlines iterator
#     if x==7: #if last rank
#         readIndexR = length #because right index is not inclusive
#     print("for rank " + str(x))
#     print(" L = " + str(readIndexL))
#     print(" R = " + str(readIndexR))
# for x in range(8):
#     printRanges(length,x)
    
#ctr = 1
ctr = 0
    
for line in big_data:
    print(ctr)
    if ctr==0:
        ctr+=1
        continue
    if len(line)<=3: #this is in case the last line is just some brackets for example
        continue
    elif line.endswith(',\n') or line.endswith(','):
        line = line[:-2]
    elif line.endswith('\n'):
        line = line[:-1]
    if ctr == length-1:
        #ignore the last two brackets of the very last line
        line = line[:-2]
    ctr+=1
    data = json.loads(line)
    # print(line)
    # print(n)

    coordinates = data["value"]["geometry"]["coordinates"]
    text = data["doc"]["text"]
    score = 0
    
    # note that text for tweets is stored twice. Other location is i["value"]["properties"]["text"]
    # the one I chose to parse is cleaner
    
    # check which grid
    grid_index = check_grid(coordinates, grid_arr)
    #print(grid_index)
    
    if grid_index==None:
            #if tweet is not found in melb grid, ignore it
            continue
    
    # check the words
    words = text.split(" ") #split words based on spaces
    for word in words:
        word = word.rstrip("!,?.'")
        word = word.rstrip('"')
        word = word.lower()
        # remove special characters from the ends of each word. make lowercase
        
        #print(word + " score = " + str(sentimentDict.get(word, 0)))            
        score += int(sentimentDict.get(word, 0))
        # if word key exists in dictionary, add score. If not, add 0 (i.e. no change)
    
    grid_arr[grid_index][5] += 1 # increment total tweets
    grid_arr[grid_index][6] += score # update grid totalScore
    
### Final output
###
print("Cell   #Total Tweets    #Overall Sentiment Score")
for i in grid_arr:
    print(i[0] + "\t" + str(i[5]) + "\t\t" + str("{:+d}".format(i[6])))