# imports
import pygame
import sys
import random
import asyncio

pygame.init()

# set up screen
screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth,screenHeight))

# clock 
clock = pygame.time.Clock()
fps = 60

# grid
grid = pygame.image.load("images/snake grid.png")
grid = pygame.transform.scale(grid, (screenWidth,screenHeight))
gridIntro = pygame.transform.scale(grid,(screenHeight + 250, screenHeight + 250))



#def intro():
#    font = pygame.font.Font("Retro gaming.ttf",70)
#    text = font.render("Snake",True,"black")
#    textRect = text.get_rect()
#    textRect.center = screenWidth/2 ,screenHeight / 2
#    run = True
#    while run:
#        screen.blit(gridIntro,(-200,-200))
#        for event in pygame.event.get():
#            if event.type == pygame.QUIT:
#                sys.exit()
#            if event.type == pygame.KEYDOWN:
#                if event.key == pygame.K_SPACE:
#                    main()
#                    run = False
#        
#        screen.blit(text, textRect)
#        pygame.display.update()



tileDim = 31.5789473684
spawnFruit = True
changeDirection = "LEFT"
direction = "LEFT"
moveSnake = True
ticks = 4

fruitPointsX = []
fruitPointsY = []

locationX = 20

for i in range(17):
    print(i)
    locationX = tileDim*i + 1 + 40
    if i not in (0,16):
        print (locationX / i)
        fruitPointsX.append(locationX)

locationY = screenWidth/19 * 4

for i in range(15):
    locationY = 30*i + 31 * 4 + 5
    if i not in (0,14):
        fruitPointsY.append(locationY)
    
class Snake():
    def __init__(self):
        self.position = [tileDim * 10 + 10, screenHeight/2]
        self.snakePoints = []
        self.image = pygame.image.load("images/snake_head.png")
        self.image = pygame.transform.scale(self.image,(35,35))
        self.image = pygame.transform.rotate(self.image, 270)
        self.ticksSpawn = 0
        self.spawnTick = 0

        for i in range(5):
            self.snakePoints.append([screenWidth/2 + 31*i,screenHeight/2])

    def update(self):
        self.ticksSpawn += 1
        #if self.ticksSpawn == 2:
        if spawnFruit == True or self.spawnTick > 0:
            self.spawnTick += 1
            print(self.spawnTick)
            if self.spawnTick == 3:
                self.spawnTick = 0
        else:
            self.snakePoints.pop(0)

        self.snakePoints.append((self.position[0],self.position[1]))
        self.ticksSpawn = 0

        for i in range(len(self.snakePoints)):
            if i != len(self.snakePoints) - 1:
                pygame.draw.rect(screen, "#006400", (self.snakePoints[i][0] + 10,self.snakePoints[i][1] + 5,tileDim - 15, tileDim - 15))
            else:
                screen.blit(self.image,(self.position[0] + 3,self.position[1]))

snake = Snake()

class Fruit():
    def __init__(self,x,y):
        self.image = pygame.image.load("images/apple.png")
        self.image = pygame.transform.scale(self.image, (25,25))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x - 7,y - 6)

    def update(self):
        screen.blit(self.image,self.rect)


fruit = Fruit(screenWidth/2 - 60, screenHeight/2)

def checkLoss(pointFront, points):
    if pointFront[0] <= 0 or pointFront[0] >= screenWidth - tileDim * 2 + 10:
        print("EDGECOLLISION")
        sys.exit()
    if pointFront[1] >= screenHeight - tileDim or pointFront[1] <= tileDim * 3 :
        print("EDGECOLLISION")
        sys.exit()

    for pointSnake in points:
        if pointFront[0] == pointSnake[0]:
            if pointFront[1] == pointSnake[1]:
                print("SELFCOLLISION")
                sys.exit()

def rotate(image, rotation):
    image = pygame.image.load("images/snake_head.png")
    image = pygame.transform.scale(image,(35,35))
    return pygame.transform.rotate(image,rotation)

async def main():
    global fruit, direction, ticks, changeDirection, snake
    run = True
    while run:
        screen.blit(grid,(0,0))
        snake.update()
        fruit.update()

        if moveSnake:
            if direction == "UP":
                snake.position[1] -= (tileDim - 1) / 7
            if direction == "DOWN":
                snake.position[1] += (tileDim - 1) / 7
            if direction == "LEFT":
                snake.position[0] -= (tileDim) / 7
            if direction == "RIGHT":
                snake.position [0] += (tileDim) / 7

            #ticks = 0
            checkLoss(snake.position, snake.snakePoints)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN" or event.key == pygame.K_w and direction != "DOWN":
                    changeDirection = "UP"
                    snake.image = rotate(snake.image,180)
                if event.key == pygame.K_DOWN and direction != "UP" or event.key == pygame.K_s and direction != "UP":
                    changeDirection = "DOWN"
                    snake.image = rotate(snake.image,0)
                if event.key == pygame.K_LEFT and direction != "RIGHT"or event.key == pygame.K_a and direction != "RIGHT":
                    changeDirection = "LEFT"
                    snake.image = rotate(snake.image,270)
                if event.key == pygame.K_RIGHT and direction != "LEFT" or event.key == pygame.K_d and direction != "LEFT":
                    changeDirection = "RIGHT"
                    snake.image = rotate(snake.image,90)

        ticks += 1
        if ticks == 7:
            direction = changeDirection
            ticks = 0
        
        
        
        spawnFruit = False

        if fruit.rect.colliderect(pygame.rect.Rect(snake.position[0],snake.position[1],10,10)):
            spawnFruit = True

        if spawnFruit:
            fruitX = random.choice(fruitPointsX)
            fruitY = random.choice(fruitPointsY)
            for points in snake.snakePoints:
                if (fruitX, fruitY) != points:
                    fruit = Fruit(fruitX, fruitY)
        
        clock.tick(50)
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
