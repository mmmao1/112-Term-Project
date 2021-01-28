# Updated Animation Starter Code

from tkinter import *
import random
import math
import entities
import copy
import highScoreHandling

####################################
# customize these functions
####################################

def init(data):
    
    #game states
    data.gameStates = ["StartScreen", "GameScreen", "EndScreen", "Winscreen", "HighScores", "NameInput"]
    data.currentState = data.gameStates[0]
    #player statuses
    data.statuses = ["Meh", "Interesting", "Considerable", "Afeared", "Terrifying", "Legendary"]
    data.status = data.statuses[0]
    
    #entities
    data.player = entities.Player(0, (data.width / 2, data.height / 2), (0, 0))
    data.enemies = []
    data.bullets = []
    data.islands = []
    data.drops = []
    data.dropR = data.width / 50
    
    #map data
    data.chunks = set()
    data.mapLength = 800
    data.mapX = data.width / 2
    data.mapY = data.height / 2
    
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i != 0 or j!= 0:
                newChunk = (i, j)
                data.chunks.add(newChunk)
                
    data.emptyChunks = []
    
    #map generation parameters
    data.maxIslands = 1
    data.islands += generateNewIslands(data, data.chunks, data.maxIslands, data.mapLength / 20, data.mapLength / 10)
    data.chunks.add((0, 0))
    
    #time things
    data.timerDelay = 20
    data.firingDelay = 1600
    data.respawnDelay = 20000
    data.timer = 0
    
    #positions for text
    data.margin = 80
    data.anchorPositions = {"NW": (data.margin, data.margin), 
                    "NE": (data.width - data.margin, data.margin),
                    "SW": (data.margin, data.height - data.margin), 
                    "SE": (data.width - data.margin, data.height - data.margin),
                    "Top-Center": (data.width / 2, data.margin)}
    
    #miscellaneous values
    data.killScore = 10
    data.hindrance = 1
    data.goldWorth = 10
    data.ammoWorth = 10
    data.claimed = False
    data.name = ""
    
    #keyboard parameters
    data.letters = []
    char = "a"
    
    for i in range(3):
        bar = []
        for j in range(9):
            bar += [char]
            char = chr(ord(char) + 1)
        data.letters += [copy.copy(bar)]
    data.letters[2][8] = "DELETE"

#this function generates random islands per map chunk
#is limited in frequency by data.maxIslands
def generateNewIslands(data, setOfChunks, maxIslands, minSize, maxSize):
    output = []
    for chunk in setOfChunks:
        x = chunk[0] * data.mapLength - data.mapLength / 2 + data.mapX
        y = chunk[1] * data.mapLength - data.mapLength / 2 + data.mapY
        numberOfIslands = random.randint(0, maxIslands)
        for i in range(numberOfIslands):
            randLength = random.randint(minSize // 1, maxSize // 1)
            randCx = random.randint(randLength, data.mapLength - randLength)
            randCy = random.randint(randLength, data.mapLength - randLength)
            island = entities.Island((x + randCx, y + randCy), randLength, chunk)
            output.append(island)
    return output

def mousePressed(event, data):
    #start screen
    if data.currentState == data.gameStates[0]:
        
        #start game
        if event.x  > 0 and event.x < 100:
            if event.y > 0 and event.y < 50:
                data.currentState = data.gameStates[1]
                
        #view scores
        if event.x > data.width - 100 and event.x < data.width:
            if event.y > 0 and event.y < 50:
                data.currentState = data.gameStates[4]
                
        #enter name screen
        if event.x > 0 and event.x < 100:
            if event.y > (data.height * 1/5) - 25 and event.y < (data.height * 1/5) + 25:
                data.currentState = data.gameStates[5]
    
    #either the game over or win screen
    if data.currentState == data.gameStates[2] or data.currentState == data.gameStates[3]:
        
        #start new game
        y1 = (4/5 * data.height) - 40
        y2 = (4/5 * data.height) + 40
        x1 = (1/2 * data.width) - 80
        x2 = (1/2 * data.width) + 80
        
        if event.x  > x1 and event.x < x2:
            if event.y > y1 and event.y < y2:
                name = data.name
                init(data)
                data.name = name
                data.currentState = data.gameStates[1]
        
        #home screen
        y3 = (1/5 * data.height) - 40
        y4 = (1/5 * data.height) + 40
        
        if event.x  > x1 and event.x < x2:
            if event.y > y3 and event.y < y4:
                init(data)
                data.currentState = data.gameStates[0]
    
    #view the scores
    if data.currentState == data.gameStates[4]:
        
        #home
        if event.x  > 0 and event.x < 100:
            if event.y > 0 and event.y < 50:
                data.currentState = data.gameStates[0]
    
    #name generator page
    if data.currentState == data.gameStates[5]:
        
        x1 = data.width / 6
        y1 = 1/2 * data.height - 40
        width = data.width * 4/6
        height = data.height * 1/3
        col = width / 9
        row = height / 3
        
        #keys / keyboard
        for i in range(3):
            for j in range(9):
                if event.x > x1 + j * col and  event.x < x1 + (j+1) * col:
                    if event.y > y1 + i * row and event.y < y1 + (i+1) * row:
                        if i == 2 and j == 8:
                            data.name = data.name[:len(data.name) - 1]
                        else:
                            data.name += data.letters[i][j]
        #submit button
        if event.x > data.width / 2 - 50 and event.x < data.width / 2 + 50:
            if event.y > data.height * (5/6) - 25 and event.x < data.height * (5/6) + 25:
                data.currentState = data.gameStates[0]
    
def keyPressed(event, data):
    #player rotation
    if event.keysym == "Left":
        data.player.rotate("Left")
    if event.keysym == "Right":
        data.player.rotate("Right")
    
    #cannon firing
    if event.keysym == "z":
        if data.player.cannonballs > 0 and not data.player.firing:
            data.bullets += data.player.fire("Left")
            data.player.cannonballs -= data.player.cannons
            data.player.firing = True
    if event.keysym == "x":
        if data.player.cannonballs > 0 and not data.player.firing:
            data.bullets += data.player.fire("Right")
            data.player.cannonballs -= data.player.cannons
            data.player.firing = True
    

def timerFired(data):
    if data.currentState == data.gameStates[1]:
        #move bullets
        if data.bullets:
            for bullet in data.bullets:
                bullet.move()
                
        #move enemies
        if data.enemies:
            for enemy in data.enemies:
                enemy.move()
                
        #bullet collisions with all ship entities
        removeBullets = set()
        remove = set() 
        for i in range(len(data.bullets)):
            bullet = data.bullets[i]
            for j in range(len(data.enemies)):
                ship = data.enemies[j]
                if ship != 0 and bullet.collide(ship):
                    removeBullets.add(i)
                    ship.takeDamage(entities.Bullet.damage)
                    if ship.health <= 0:
                        newDrop = entities.Drop((ship.center[0], ship.center[1]), data.dropR)
                        data.drops += [newDrop]
                        data.enemies.pop(j)
                        data.enemies.insert(j, 0)
            if bullet.collide(data.player):
                removeBullets.add(i)
                data.player.takeDamage(entities.Bullet.damage)
                if data.player.health <= 0:
                    data.currentState = data.gameStates[2]
                    highScoreHandling.updateScores(data.name + "-" + str(data.player.gold))
                    break
                    
        #removes placeholder enemies
        while(0 in data.enemies):
            data.enemies.remove(0)
        
        #player collects drop
        if data.drops:
            for drop in data.drops:
                if drop.collide(data.player):
                    i = data.drops.index(drop)
                    data.drops.pop(i)
                    data.drops.insert(i, 0)
                    if drop.type == "Coin":
                        data.player.gold += data.goldWorth
                    if drop.type == "Ammo":
                        data.player.cannonballs += data.ammoWorth
        
        while(0 in data.drops):
            data.drops.remove(0)
            
        
        #remove bullets
        newL = []
        if removeBullets:
            for j in range(len(data.bullets)):
                if j not in removeBullets:
                    newL += [data.bullets[j]]
            data.bullets = newL
    
        #camera movement
        mapChanges = data.player.move()
        
        # move player
        data.player.center = (data.player.center[0] - mapChanges[0], data.player.center[1] - mapChanges[1])
        # move map
        data.mapX -= mapChanges[0]
        data.mapY -= mapChanges[1]
        # move islands
        for island in data.islands:
            island.center = (island.center[0] - mapChanges[0], island.center[1] - mapChanges[1])
        # move drops on map
        for drop in data.drops:
            drop.center = (drop.center[0] - mapChanges[0], drop.center[1] - mapChanges[1])
        # move enemies and bullets
        for enemy in data.enemies:
            enemy.center = (enemy.center[0] - mapChanges[0], enemy.center[1] - mapChanges[1])
        for bullet in data.bullets:
            bullet.center = (bullet.center[0] - mapChanges[0], bullet.center[1] - mapChanges[1])
                
        # get the current chunk the player is in and add new chunks if needed
        # also, if the player enters a chunk with an enemy in it, enemy will
        # start attacking
        
        newChunks = set()
        
        for chunk in data.chunks:
            if chunk != data.player.sector:
                x = chunk[0] * data.mapLength + data.mapX
                y = chunk[1] * data.mapLength + data.mapY
                if entities.distance(x, y, data.player.center[0], data.player.center[1]) < data.mapLength / 2:
                    data.player.sector = chunk
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if i != 0 or j != 0:
                                newChunk = (chunk[0] + i, chunk[1] + j)
                                if newChunk not in data.chunks:
                                    newChunks.add(newChunk)
                    #check if current chunk has a baddie in it
                    for enemy in data.enemies:
                        if enemy.sector == chunk:
                            enemy.attacking = True
                            enemy.attackPattern = random.choice(entities.Ship.attackStates)
                            enemy.cannons = data.player.cannons - data.hindrance
                            enemy.speed = data.player.speed - data.hindrance
                            
                            #set up patterns of enemy
                            if enemy.attackPattern == "Loop":
                                enemy.rotateSpeed = random.randint(0, 4)
                                direction = ["Left", "Right"]
                                enemy.rotateDir = random.choice(direction)
                                
                            if enemy.attackPattern == "Zigzag":
                                enemy.speed = data.player.speed - data.hindrance
                                enemy.rotateSpeed = 90
                                direction = ["Left", "Right"]
                    
                    break
        
        #spawn new islands and ships
        newIslands = generateNewIslands(data, newChunks, data.maxIslands, data.mapLength / 20, data.mapLength / 10)
        data.islands += newIslands
        newValues = spawnNewShips(data, newChunks, newIslands)
        data.enemies += newValues[0]
        data.emptyChunks += newValues[1]
        #add new chunks to master chunk list
        data.chunks = data.chunks.union(newChunks)
        
        # check player-island crash
        for island in data.islands:
            if island.sector == data.player.sector:
                if island.collide(data.player):
                    highScoreHandling.updateScores(data.name + "-" + str(data.player.gold))
                    data.currentState = data.gameStates[2]
                    break
                    
        # check enemy-island crashes
        for island in data.islands:
            for enemy in data.enemies:
                if not isinstance(enemy, int) and island.collide(enemy):
                    j = data.enemies.index(enemy)
                    data.enemies.pop(j)
                    data.enemies.insert(j, 0)
                        
        while(0 in data.enemies):
            data.enemies.remove(0)
                
        #bulletRemoval
        removeList = []
        if data.bullets:
            for i in range(len(data.bullets)):
                if data.bullets[i].dead:
                    removeList += [i]
        newBullets = []
        for i in range(len(data.bullets)):
            if i not in removeList:
                newBullets += [data.bullets[i]]
        data.bullets = newBullets
            
        data.timer += data.timerDelay
        if data.enemies:
            for enemy in data.enemies:
                if enemy.attacking:
                    enemy.timer += data.timerDelay
        
        #AI
        for enemy in data.enemies:
            if enemy.attacking:
                #update enemy behavior
                    
                if enemy.attackPattern == "Loop":
                    enemy.rotate(enemy.rotateDir)
                    
                if enemy.attackPattern == "Zigzag":
                    enemy.distanceTravelled += enemy.speed
                    if enemy.distanceTravelled % enemy.turnDistance > 0 and enemy.distanceTravelled > enemy.turnDistance:
                        enemy.rotate(enemy.rotateDir)
                        enemy.rotateDir = "Left" if enemy.rotateDir == "Right" else "Right"
                        enemy.distanceTravelled = 0
                        
                if enemy.attackPattern == "Run":
                    enemy.distanceTravelled += enemy.speed
                    if enemy.distanceTravelled % enemy.turnDistance > 0 and enemy.distanceTravelled > enemy.turnDistance:
                        if enemy.detDirection(data.player) == "Right":
                            enemy.rotateDir = "Left"
                            angleChange = -90 + abs(data.player.direction - enemy.direction)
                        else:
                            enemy.rotateDir = "Right"
                            angleChange = 90 - abs(data.player.direction - enemy.direction)
                        
                        enemy.rotateSpeed = angleChange
                        enemy.rotate(enemy.rotateDir)
                        
                        enemy.distanceTravelled = 0
        
        #update player firing delay and have enemies fire
        if data.timer >= data.firingDelay and data.timer % data.firingDelay == 0:
            data.player.firing = False
        
        #enemies fire
        if data.enemies:
            for enemy in data.enemies:
                if enemy.attacking:
                    if enemy.timer >= data.firingDelay and enemy.timer % data.firingDelay > 0:
                        data.bullets += enemy.fire("Left")
                        data.bullets += enemy.fire("Right")
                        enemy.timer = 0
                        
        #respawn
        if data.timer >= data.respawnDelay and data.timer % data.firingDelay == 0:
            
            actualEmptyChunks = copy.copy(data.emptyChunks)
            
            for chunk in data.emptyChunks:
                for enemy in data.enemies:
                    if enemy.sector == chunk:
                        actualEmptyChunks.remove(chunk)
                        break
            
            data.enemies += spawnNewShips(data, actualEmptyChunks, [])[0]
            
        #upgrades and enemy buffs
        if data.player.gold == 20 and not data.claimed:
            data.status = data.statuses[1]
            data.player.speed += 1
            data.player.cannons += 1
            data.hindrance -= 1
            data.claimed = True
        if data.player.gold == 60:
            data.status = data.statuses[2]
            data.claimed = False
        if data.player.gold == 100 and not data.claimed:
            data.status = data.statuses[3]
            data.player.speed += 1
            data.player.cannons += 1
            data.hindrance -= 1
            data.claimed = True
        if data.player.gold == 200:
            data.status = data.statuses[4]
            data.claimed = False
        if data.player.gold == 300 and not data.claimed:
            data.status = data.statuses[5]
            data.player.speed += 1
            data.player.cannons += 1
            data.hindrance -= 1
            data.claimed = True
        if data.player.gold == 350:
            data.currentState = data.gameStates[3]
            highScoreHandling.updateScores(data.name + "-" + str(data.player.gold))
        
        #remove enemies that go too far
        if data.enemies:
            for enemy in data.enemies:
                if enemy.attacking:
                    if entities.distance(enemy.center[0], enemy.center[1], data.player.center[0], data.player.center[1]) >= 1000:
                        j = data.enemies.index(enemy)
                        data.enemies.pop(j)
                        data.enemies.insert(j, 0)

        while(0 in data.enemies):
            data.enemies.remove(0)
        
        #remove drops that go too far
        if data.drops:
            for drop in data.drops:
                if entities.distance(drop.center[0], drop.center[1], data.player.center[0], data.player.center[1]) >= 800:
                        j = data.drops.index(drop)
                        data.drops.pop(j)
                        data.drops.insert(j, 0)

        while(0 in data.drops):
            data.drops.remove(0)
        
        #reset timer to save calculations
        if data.timer > 50000:
            data.timer = 0

# takes new group of chunks and sees which ones are empty
# and adds ships to those chunks
def spawnNewShips(data, chunks, islands) :
    emptyChunks = copy.copy(list(chunks))
    for chunk in chunks:
        for island in islands:
            if island.sector == chunk:
                emptyChunks.remove(chunk)
                break
    output = []
    for chunk in emptyChunks:
        center = (chunk[0] * data.mapLength + data.mapX, chunk[1] * data.mapLength + data.mapY)
        direction = random.choice([-180, 180, -90, 90])
        newEnemy = entities.Ship(direction, center, chunk)
        newEnemy.speed = 0
        output += [newEnemy]
    return (output, emptyChunks)    
    
def redrawAll(canvas, data):
    #start screen
    if data.currentState == data.gameStates[0]:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "pink")
        canvas.create_rectangle(0, 0, 100, 50, fill = "yellow")
        canvas.create_text(50, 25, anchor = "center", text = "PRESS TO START", font = "times 10")
        canvas.create_rectangle(data.width - 100, 0, data.width, 50, fill = "yellow")
        canvas.create_text(data.width - 50, 25, anchor = "center", text = "HIGH SCORES", font = "times 10")
        
        margin = 20
        
        canvas.create_text(data.width / 2, data.height / 2 - 3 * margin, 
                                    text = "PIRACY: THE GAME", font = "Papyrus 40", fill = "RED")
        
        canvas.create_text(data.width / 2, data.height / 2, 
                                    text = "Press z to fire your left cannons and x to fire your right cannons", 
                                    font = "Papyrus 20")
        canvas.create_text(data.width / 2, data.height / 2 +  2 * margin, 
                                    text = "Murder, destroy, and pillage: traverse the seas of Detroit and claim your rightful glory!", font = "Papyrus 20")
        
        canvas.create_rectangle(0, (data.height * 1/5) - 25, 100, (data.height * 1/5) + 25, fill = "yellow")
        canvas.create_text(50, data.height * (1/5), text = "CREATE NAME", font = "times 10")
        
        #name
        canvas.create_text(data.width / 2, 1/4 * data.height, text = "NAME: " + data.name, font = "Papyrus 40 bold")
        
        
    #high scores
    if data.currentState == data.gameStates[4]:
        
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "pink")
        
        canvas.create_rectangle(0, 0, 100, 50, fill = "yellow")
        canvas.create_text(50, 25, anchor = "center", text = "BACK", font = "times 10")
        
        canvas.create_text(data.width / 2, data.height / 10, text = "HIGH SCORES", 
                                font = "papyrus 40 bold", fill = "GREEN")
                            
        
        #scores
        
        scoreText = highScoreHandling.readFile("scores.txt")
        
        newText = ""
        index = 1
        for score in scoreText.split("\n"):
            newText += str(index) + ": " + score + "\n"
            index += 1
            
        
        canvas.create_text(data.width / 2, data.height / 3, text = newText)
    
    #death screen
    if data.currentState == data.gameStates[2]:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "brown")
        canvas.create_text(data.width / 2, data.height / 2, font = "Times 30", anchor = "center", text = "YE DIED")
        canvas.create_text(data.width / 2, data.height / 2 + 40, font = "Times 25", anchor = "center", text = "Ye be remembered as a " + data.status + " pirate")
        
        y1 = (4/5 * data.height) - 40
        y2 = (4/5 * data.height) + 40
        x1 = (1/2 * data.width) - 80
        x2 = (1/2 * data.width) + 80
        
        canvas.create_rectangle(x1, y1, x2, y2, fill = "pink")
        canvas.create_text(1/2 * data.width, 4/5 * data.height, text = "PLAY AGAIN", font = "Times 20")
        
        y3 = (1/5 * data.height) - 40
        y4 = (1/5 * data.height) + 40
        
        canvas.create_rectangle(x1, y3, x2, y4, fill = "pink")
        canvas.create_text(1/2 * data.width, 1/5 * data.height, text = "HOME", font = "Times 20")
    
    #win screen
    if data.currentState == data.gameStates[3]:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "gold")
        canvas.create_text(data.width / 2, data.height / 2, font = "Times 30", anchor = "center", text = "YOURE THE GREATEST PIRATE WHO EVER LIVED", fill = "cyan")
        
        y1 = (4/5 * data.height) - 40
        y2 = (4/5 * data.height) + 40
        x1 = (1/2 * data.width) - 80
        x2 = (1/2 * data.width) + 80
        
        canvas.create_rectangle(x1, y1, x2, y2, fill = "pink")
        canvas.create_text(1/2 * data.width, 4/5 * data.height, text = "PLAY AGAIN", font = "Times 20")
        
        y3 = (1/5 * data.height) - 40
        y4 = (1/5 * data.height) + 40
        
        canvas.create_rectangle(x1, y3, x2, y4, fill = "pink")
        canvas.create_text(1/2 * data.width, 1/5 * data.height, text = "HOME", font = "Times 20")
        
        
    #name input:
    if data.currentState == data.gameStates[5]:
        
        canvas.create_rectangle(0, 0, data.width, data.height, fill = "lavender", width = "0")
        
        x1 = data.width / 6
        y1 = 1/2 * data.height - 40
        
        width = data.width * 4/6
        height = data.height * 1/3
        
        col = width / 9
        row = height / 3
        
        for i in range(3):
            for j in range(9):
                
                
                canvas.create_rectangle(x1 + j * col, y1 + i * row, x1 + (j+1) * col, y1 + (i+1) * row)
                canvas.create_text(x1 + j * col + col / 2, y1 + i * row + row / 2, text = data.letters[i][j])
                
        canvas.create_text(data.width / 2, 1/4 * data.height, text = "NAME: " + data.name, font = "Papyrus 40 bold")
        
        canvas.create_rectangle(data.width / 2 - 50, data.height * (5/6) - 25, data.width / 2 + 50, data.height * (5/6) + 25, fill = "pink")
        canvas.create_text(data.width / 2, data.height * (5/6), text = "SUBMIT")
    
    #main game
    if data.currentState == data.gameStates[1]:
        
        #draw map
        drawMap(data, canvas)
        
        drawEntities(data, canvas)
        
        drawStats(data, canvas)

#draw the background map and the islands
def drawMap(data, canvas):
    for chunk in data.chunks:
        x1, y1 = chunk[0] * data.mapLength - data.mapLength / 2 + data.mapX, chunk[1] * data.mapLength - data.mapLength / 2 + data.mapY
        x2, y2 = chunk[0] * data.mapLength + data.mapLength / 2 + data.mapX, chunk[1] * data.mapLength + data.mapLength / 2 + data.mapY
        canvas.create_rectangle(x1, y1, x2, y2, fill = "lightblue", width = "0")
    for island in data.islands:
        island.draw(canvas)

#draw the entities onto the map
def drawEntities(data, canvas):
    if data.bullets:
        for bullet in data.bullets:
            bullet.draw(canvas)
        
    data.player.draw(canvas)
        
    if data.enemies:
        for enemy in data.enemies:
            if not isinstance(enemy, int):
                enemy.draw(canvas)
    
    if data.drops:
        for drop in data.drops:
            drop.draw(canvas)

#draw all the current player stats
def drawStats(data, canvas):
    fontcolor = "black"
    canvas.create_text(data.anchorPositions["NE"], text = "Gold: " + str(data.player.gold), 
                            anchor = "center", font = "Papyrus 20 bold", fill = fontcolor)
    canvas.create_text(data.anchorPositions["SW"], text = "Health: " + str(data.player.health), 
                            anchor = "center", font = "Papyrus 20 bold", fill = fontcolor)
    canvas.create_text(data.anchorPositions["SE"], text = "Balls: " + str(data.player.cannonballs), 
                            anchor = "center", font = "Papyrus 20 bold", fill = fontcolor)
    if data.player.firing == False:
        reloading = "READY"
    else:
        reloading = "RELOADING"
    canvas.create_text(data.anchorPositions["NW"], text = "CANNONS: " + reloading, 
                            anchor = "center", font = "Papyrus 15", fill = fontcolor)
    
    canvas.create_text(data.anchorPositions["Top-Center"], text = "You're " + data.status, anchor = "cen", font = "Papyrus 30 bold", fill = fontcolor) 
    
    
####################################
# this is a run function taken from the "Animation Part 2: Time-Based Animations"
#from the 15-112 course page online: "https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html"
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    
    init(data)
    
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
        
    
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 600)