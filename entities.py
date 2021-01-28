import math
import random

#ship entity
class Ship(object):
    
    attackStates = ["Loop", "Zigzag", "Run"]
    
    def __init__(self, direction, center, sector):
        #use an angle and center to draw ships and handle interactions
        self.direction = direction
        self.center = center
        self.sector = sector
        self.width = 40
        self.height = 70
        self.radius = self.width / 2
        
        self.speed = 3
        self.rotateSpeed = 15
        self.color = "brown"
        self.cannons = 5
        
        #keeps track of points on the ship
        self.coords = getCoords(self.direction, self.center, self.width, self.height)
        self.portsideCoords = coordsToSideCoords(self.coords, self.height, self.direction, self.cannons, "Left")
        self.starboardCoords = coordsToSideCoords(self.coords, self.height, self.direction, self.cannons, "Right")
        
        self.health = 20
        self.cannonballs = 100
        self.cannonDamage = 5
        self.firing = False
        
        #AI
        self.attacking = False
        self.attackPattern = None
        self.timer = 0
        
        #loop
        self.rotateDir = None
        
        #zigzag
        self.distanceTravelled = 0
        self.turnDistance = 80 * self.speed
        
    def updateCoords(self):
        self.coords = getCoords(self.direction, self.center, self.width, self.height)
        self.portsideCoords = coordsToSideCoords(self.coords, self.height, self.direction, self.cannons, "Left")
        self.starboardCoords = coordsToSideCoords(self.coords, self.height, self.direction, self.cannons, "Right")
    
    def move(self):
        speedX = self.speed * math.cos(math.radians(self.direction))
        speedY = self.speed * math.sin(math.radians(self.direction))
        self.center = (self.center[0] + speedX, self.center[1] + speedY)
        self.updateCoords()
        return (speedX, speedY)
        
    def rotate(self, direction):
        if direction == "Left":
            self.direction -= self.rotateSpeed
            if self.direction <= -360:
                self.direction = self.direction + 360
            if self.direction >= 360:
                self.direction = self.direction - 360
        elif direction == "Right":
            self.direction += self.rotateSpeed
        self.updateCoords()
    
    def fire(self, side):
        if side == "Left":
            coords = self.portsideCoords
            angleChange = -90
        else:
            coords = self.starboardCoords
            angleChange = 90
        
        bullets = []
        for coord in coords:
            newBullet = Bullet(self.direction + angleChange, coord)
            bullets.append(newBullet)
        return bullets
    
    def draw(self, canvas):
        canvas.create_polygon(self.coords, fill = self.color, width = "0")
        center = [(self.center[0] - self.radius), (self.center[1] - self.radius),
                    (self.center[0] + self.radius), (self.center[1] + self.radius)]
        # canvas.create_oval(center, fill = "red")
        canvas.create_line(self.coords[0], self.coords[1], fill = "yellow")
        
    def detDirection(self, other):
        x1, y1 = self.center[0], self.center[1]
        x2, y2 = self.radius * math.cos(math.radians(self.direction)), self.radius * math.sin(math.radians(self.direction))
        
        slope = ((x2 - x1) / (y2 - y1)) // 1
        b = y1 - slope * x1
        
        if other.center[1] < other.center[0] * slope + b:
            return "Right"
        else:
            return "Left"
        
    def takeDamage(self, damage):
        self.health -= damage
    
    def getHashables(self):
        return (self.direction, self.center)
    
    def __hash__(self):
        return hash(self.getHashables())

#slightly altered ship class for player
class Player(Ship):
    def __init__(self, direction ,center, sector):
        super().__init__(direction, center, sector)
        self.health = 50
        self.speed = 4
        self.cannonDamage = 10
        self.color = "goldenrod4"
        self.gold = 0

#drops that drop when an enemy is killed
class Drop(object):
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.type = random.choice(["Coin", "Ammo"])
        
    def __hash__(self):
        return hash(self.center)
        
    def draw(self, canvas):
        if self.type == "Coin":
            canvas.create_oval(self.center[0] - self.radius, self.center[1] - self.radius, 
                        self.center[0] + self.radius, self.center[1] + self.radius, fill = "gold")
        
        if self.type == "Ammo":
            canvas.create_rectangle(self.center[0] - self.radius, self.center[1] - self.radius, 
                        self.center[0] + self.radius, self.center[1] + self.radius, fill = "brown")
                        
    def collide(self, other):
        if distance(self.center[0], self.center[1], other.center[0], other.center[1]) < self.radius + other.radius:
            return True
            
#islands - main obstacle in the game
class Island(object):
    def __init__(self, center, length, sector):
        self.center = center
        self.length = length
        self.sector = sector
        self.color = "dark green"
        
    def draw(self, canvas):
        canvas.create_rectangle(self.center[0] - self.length, self.center[1] - self.length, 
                                    self.center[0] + self.length, self.center[1] + self.length, fill = self.color, width = "0")
        # canvas.create_oval(self.center[0] - self.length, self.center[1] - self.length, 
                                    # self.center[0] + self.length, self.center[1] + self.length, fill = "red", width = "0")
    
    def getHashables(self):
        return (self.center, self.length)
        
    def collide(self, other):
        if distance(self.center[0], self.center[1], other.center[0], other.center[1]) < self.length + other.radius:
            return True
    
    def __hash__(self):
        return hash(self.getHashables())

#cannonballs
class Bullet(object):
    
    damage = 5
    
    def __init__(self, direction, center):
        self.center = center
        self.direction = direction
        self.radius = 3
        self.speed = 10
        self.distanceTravelled = 0
        self.range = 400
        self.dead = False
        
    def move(self):
        speedX = self.speed * math.cos(math.radians(self.direction))
        speedY = self.speed * math.sin(math.radians(self.direction))
        self.center = (self.center[0] + speedX, self.center[1] + speedY)
        self.distanceTravelled += self.speed
        if self.distanceTravelled >= self.range:
            self.dead = True
        
    def draw(self, canvas):
        canvas.create_oval(self.center[0] - self.radius, self.center[1] - self.radius, 
                            self.center[0] + self.radius, self.center[1] + self.radius, fill = "red")
        
    def collide(self, other):
        if distance(self.center[0], self.center[1], other.center[0], other.center[1]) < self.radius + other.radius:
            return True
    
    
    def getHashables(self):
        return (self.direction, self.center)
    
    def __hash__(self):
        return hash(self.getHashables())

#uses trig to get new coords for points on the ship via its angle and center
def getCoords(direction, center, width, height):
    
    w = width / 2
    h = height / 2
    
    deviation = math.degrees(math.atan(w/h))
    
    distanceFromCenter = (w**2 + h**2)**(1 / 2)
    
    coords = []
    
    a = direction + deviation
    b = direction - deviation
    coords.append(a if a <= 360 else a - 360)
    coords.append(b if b <= 360 else b - 360)
    coords.append(a + 180 if a <= 360 else a + 180 - 360)
    coords.append(b + 180 if b <= 360 else b + 180 - 360)
    
    newCoords = []
    
    for coord in coords:
        newCoord = (distanceFromCenter * math.cos(math.radians(coord)) + center[0], 
                        distanceFromCenter * math.sin(math.radians(coord)) + center[1])
        
        newCoords.append(newCoord)

    return newCoords

# this takes care of the output points on the ship for cannonballs
def coordsToSideCoords(coords, length, direction, numberOfCannons, side):
    if side == "Left":
        start = coords[2]
    else:
        start = coords[3]
        
    margin = (length / numberOfCannons) / 2
    
    marginX = margin * math.cos(math.radians(direction))
    marginY = margin * math.sin(math.radians(direction))
    
    dx = (length * math.cos(math.radians(direction))) / numberOfCannons
    dy = (length * math.sin(math.radians(direction))) / numberOfCannons
    
    sidePoints = []
    
    for i in range(numberOfCannons):
        newCoords = (start[0] + i * dx + marginX, start[1] + i * dy + marginY)
        sidePoints.append(newCoords)
    
    return sidePoints
    
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**(1/2)
    
    
    
    
    
    
    