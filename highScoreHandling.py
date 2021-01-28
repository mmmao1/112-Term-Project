####################################
# these are I/O functions taken from the "Strings" module
#from the 15-112 course page online: "https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO"
####################################

def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
        
#code below is not taken

#this function will update the scores.txt with a new player entry
#it will max out the scores at ten, also matches will be handled
#by having the most recent score come out on top
def updateScores(newScore):
    contentsRead = readFile("scores.txt")
    scores = contentsRead.split("\n")
    
    if len(contentsRead) == 0:
        newContentsRead = newScore
        writeFile("scores.txt", newContentsRead)
        
    else:
        num = eval(newScore.split("-")[1])
    
        curScore = scores[0]
        index = None
        for i in range(len(scores)):
            curScore = scores[i]
            curNum = eval(curScore.split("-")[1])
            if curNum <= num:
                index = i
                break
        if not index == None:
            scores.insert(index, newScore)
        else:
            scores += [newScore]
        
        if len(scores) > 10:
            scores.pop()
        
        output = ""
        for i in range(len(scores)):
            if i != 0:
                output += "\n" + str(scores[i])
            else:
                output += str(scores[i])
                
        writeFile("scores.txt", output)


    



    

