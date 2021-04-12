import json, math
from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size() #amount of tasks
rank = comm.Get_rank() #current task. Range (1, size-1)

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
    return None
                
                
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


def sumGrid(grid_arr1, grid_arr2):
    #grid_arr1 is from master. grid_arr2 is from slave
    #grid_arr is [[id, xmin, xmax, ymin, ymax, totalTweets, totalScore],..,[]]
    
    sumArr = grid_arr1
    
    for index, grid in enumerate(grid_arr2):
        sumArr[index][5] += grid[5] #add tweet count
        sumArr[index][6] += grid[6] #add tweet score
    
    return sumArr


def giveRanges(length, x, size):
    step = length/size
    readIndexL = math.floor(1 + x*step)
    readIndexR = math.floor(step*(x+1)+1)
    #note right index is excluded in the readlines iterator
    if x==0: # if first rank
        readIndexL=0
    if x==size-1: #if last rank
        readIndexR = length #because right index is not inclusive
    return (readIndexL, readIndexR) #return a tuple

    # print("for rank " + str(x))
    # print(" L = " + str(readIndexL))
    # print(" R = " + str(readIndexR))


# hard code number of lines in bigTwitter
length = 4233611

#commented code below was used as a precalculation to determine the file's line length
# big_data = open('bigTwitter.json', encoding='utf-8')
# bigCtr = 0
# for line in big_data:
#     bigCtr+=1
# print(bigCtr)
# length=bigCtr

### wait for all nodes to reach this point
comm.Barrier()

if size==1:
    #################################
    #ONE CORE. NO PARALLEL PROCESSING
    #################################
    
    ### Tweets analysed tweet by tweet. open file again for processing
    ###
    big_data = open('bigTwitter.json', encoding='utf-8')
    coordinates = [] # [long,lat]
    text = []
    ctr = 0
    for line in big_data:
        if ctr==0:
            ctr+=1
            continue
        if len(line)<=3: #this is in case the last line is just some brackets for example
            continue
        elif line.endswith(',\n') or line.endswith(','):
            line = line[:-2]
        elif line.endswith('\n'):
            line = line[:-1]
        if ctr == length-1: #the last line will have extra brackets
            line = line[:-2]
        ctr+=1
        
        data = json.loads(line)
    
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
        print(i[0] + "\t\t " + str(i[5]) + "\t\t\t\t\t" + str("{:+d}".format(i[6])))
else:
    ###################################
    #MULTI-CORE. DO PARALLEL PROCESSING
    ###################################
    
    #get range of lines to read in file given rank
    rangeOutput = giveRanges(length, rank, size)
    readIndexL = rangeOutput[0]
    readIndexR = rangeOutput[1]
    
    big_data = open('bigTwitter.json', encoding='utf-8')
    #each core including master will do processing for equally divided number of tweets from json
    
    coordinates = [] # [long,lat]
    text = []
    ctr = 0
    
    ### Tweets analysed tweet by tweet
    ###
    for line in big_data:
        if ctr==0 or ctr<readIndexL or ctr>=readIndexR:
            #skip any lines that are not readIndexL <= big_data lines < ReadIndexR
            ctr+=1
            continue
        if len(line)<=3: #this is in case the last line is just some brackets for example
            continue
        elif line.endswith(',\n') or line.endswith(','):
            line = line[:-2]
        elif line.endswith('\n'):
            line = line[:-1]
        if ctr == length-1: 
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
        
        grid_arr[grid_index][5] += 1 # increment total tweets by amount from each slave
        grid_arr[grid_index][6] += score # update grid totalScore by amount from each slave

    ### wait for all ranks to reach this point --> all ranks to finish processing their tweets
    comm.Barrier()
    data = comm.gather(grid_arr, root=0) # gather data
    
    if rank == 0:
        # master                
        for i in range(1,size):
            grid_arr = sumGrid(grid_arr, data[i])
            ###compile each rank's grid_arr and sum the total tweets and the scores  
        
        ### Final output
        ###
        print("Cell   #Total Tweets    #Overall Sentiment Score")
        for i in grid_arr:
            print(i[0] + "\t" + str(i[5]) + "\t\t" + str("{:+d}".format(i[6])))
            
            