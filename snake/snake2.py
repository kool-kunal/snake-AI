import pygame
import sys
import random
import time
import neat
import os
os.environ["PATH"] += os.pathsep + 'D:/softwares/Graphviz2.38/bin'
import math
import pickle
import visualize


class Snake:
    def __init__(self):
        self.position = [100, 50]
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.changeDirectionTo = self.direction

    def changeDirection(self, dir):
        if dir == "RIGHT" and not self.direction == "LEFT":
            self.direction = "RIGHT"
        if dir == "LEFT" and not self.direction == "RIGHT":
            self.direction = "LEFT"
        if dir == "UP" and not self.direction == "DOWN":
            self.direction = "UP"
        if dir == "DOWN" and not self.direction == "UP":
            self.direction = "DOWN"

    def move(self, foodPos):
        if self.direction == "RIGHT":
            self.position[0] += 10
        if self.direction == "LEFT":
            self.position[0] -= 10
        if self.direction == "UP":
            self.position[1] -= 10
        if self.direction == "DOWN":
            self.position[1] += 10

        self.body.insert(0, list(self.position))

        if self.position == foodPos:
            return 1
        else:
            self.body.pop()
            return 0

    def checkCollision(self):
        if self.position[0] > 490 or self.position[0] < 0:
            return 1
        elif self.position[1] > 490 or self.position[1] < 0:
            return 1

        for bodyPart in self.body[1:]:
            if self.position == bodyPart:
                return 1

        return 0

    def getHeadPos(self):
        return self.position

    def getBody(self):
        return self.body


class FoodSpawner:
    def __init__(self, snake):
        self.position = [random.randrange(
            1, 49)*10, random.randrange(1, 49)*10]
        x = True
        while x:
            if self.position not in snake.body:
                x = False
            else:
               self.position = [random.randrange(1, 49)*10, random.randrange(1, 49)*10] 
        self.isFoodOnScreen = True

    def spawnFood(self, snake):
        if self.isFoodOnScreen == False:
            self.position = [random.randrange(
                1, 49)*10, random.randrange(1, 49)*10]
            x = True
            while x:
                if self.position not in snake.body:
                    x = False
                else:
                    self.position = [random.randrange(1, 49)*10, random.randrange(1, 49)*10]
            self.isFoodOnScreen = True
        return self.position

    def setFoodOnScreen(self, b):
        self.isFoodOnScreen = b


def gameOver():
    pygame.quit()
    sys.exit()


def distances(snake):
    dist_f = 500
    dist_l = 500
    dist_r = 500
    if snake.direction == "RIGHT":
        if 490 - snake.position[0] < 30:
            dist_f = 490 - snake.position[0]
        if 490 - snake.position[1] < 30:
            dist_r = 490 - snake.position[1]
        if snake.position[1] < 30:
            dist_l = snake.position[1]
        for i in range(10,31,10):
            if [snake.position[0]+i,snake.position[1]] in snake.body:
                dist_f = i
                break
        for i in range(10,31,10):
            if [snake.position[0],snake.position[1]+i] in snake.body:
                dist_r = i
                break
        for i in range(10,31,10):
            if [snake.position[0],snake.position[1]-i] in snake.body:
                dist_l = i
                break
    if snake.direction == "LEFT":
        if snake.position[0] < 30:
            dist_f = snake.position[0]
        if snake.position[1] < 30:
            dist_r = snake.position[1]
        if 490 - snake.position[1] < 30:
            dist_l = 490 - snake.position[1]
        for i in range(10,31,10):
            if [snake.position[0]-i,snake.position[1]] in snake.body:
                dist_f = i
                break 
        for i in range(10,31,10):
            if [snake.position[0],snake.position[1]-i] in snake.body:
                dist_r = i
                break
        for i in range(10,31,10):
            if [snake.position[0],snake.position[1]+i] in snake.body:
                dist_r = i
                break  
    if snake.direction == "DOWN":
        if 490 - snake.position[1] < 30:
            dist_f = 490 - snake.position[1]
        if snake.position[0] < 30:
            dist_r = snake.position[0]
        if 490 - snake.position[0] < 30:
            dist_l = 490 - snake.position[0]
        for i in range(10,31,10):
            if [snake.position[0],snake.position[1]+i] in snake.body:
                dist_f = i
                break
        for i in range(10,31,10):
            if [snake.position[0]+i,snake.position[1]] in snake.body:
                dist_l = i
                break
        for i in range(10,31,10):
            if [snake.position[0]-i,snake.position[1]] in snake.body:
                dist_r = i
                break
    if snake.direction == "UP":
        if snake.position[1] < 30:
            dist_f = snake.position[1]
        if snake.position[0] < 30:
            dist_l = snake.position[0]
        if 490 - snake.position[0] < 30:
            dist_r = 490 - snake.position[0]
        for i in range(10,31,10):
            if [snake.position[0],snake.position[1]-i] in snake.body:
                dist_f = i
                break  
        for i in range(10,31,10):
            if [snake.position[0]+i,snake.position[1]] in snake.body:
                dist_r = i
                break
        for i in range(10,31,10):
            if [snake.position[0]-i,snake.position[1]] in snake.body:
                dist_l = i
                break
    return dist_f, dist_l, dist_r

def main_human():
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Snake")
    fps = pygame.time.Clock()
    score = 0
    snake = Snake()
    foodSpawner = FoodSpawner(snake)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.changeDirection("RIGHT")
                if event.key == pygame.K_UP:
                    snake.changeDirection("UP")
                if event.key == pygame.K_DOWN:
                    snake.changeDirection("DOWN")
                if event.key == pygame.K_LEFT:
                    snake.changeDirection("LEFT")

        foodPos = foodSpawner.spawnFood(snake)
        if snake.move(foodPos):
            score += 1
            foodSpawner.setFoodOnScreen(False)

        window.fill(pygame.Color(255, 255, 255))

        dist_f, dist_l, dist_r = distances(snake)
        if dist_f < 30:
            print("forward: "+ str(dist_f))
        if dist_l < 30:
            print("left: "+ str(dist_l))
        if dist_r < 30:
            print("right: "+ str(dist_r))
        for pos in snake.getBody():
            pygame.draw.rect(window, pygame.Color(0, 255, 0),pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(window, pygame.Color(255, 0, 0),pygame.Rect(foodPos[0], foodPos[1], 10, 10))
        if(snake.checkCollision()==1):
            gameOver()

        pygame.display.set_caption("Score: "+ str(score))
        pygame.display.flip()
        fps.tick(20)


def main(genome, config):
    global x
    window = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Snake")
    fps = pygame.time.Clock()

    net = neat.nn.feed_forward.FeedForwardNetwork.create(genome,config)
    score = 0
    snake = Snake()
    foodSpawner = FoodSpawner(snake)
    genome.fitness = 0
    count = 500
    run = True
    
    while run:
        if count is 0:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if x>=200:
                        x-=100
                elif event.key == pygame.K_UP:
                    if x<=900:
                        x+=100
        sx, sy = snake.getHeadPos()[0], snake.getHeadPos()[1]
        fx, fy = foodSpawner.position[0], foodSpawner.position[1]
        dist_f, dist_l, dist_r = distances(snake)
        output = net.activate((sx-fx,sy-fy, dist_f, dist_l, dist_r))

        maxpos = output.index(max(output))
        if maxpos == 0:
            snake.changeDirection("RIGHT")
            
        elif maxpos == 1:
            snake.changeDirection("LEFT")
                # dist_fWall = snake.position[0]

        elif maxpos == 2:
            snake.changeDirection("UP")
    

        elif maxpos == 3:
            snake.changeDirection("DOWN")


        foodPos = foodSpawner.spawnFood(snake)
        if snake.move(foodPos):
            score += 1
            count = 500
            foodSpawner.setFoodOnScreen(False)

        window.fill(pygame.Color(255, 255, 255))

        for pos in snake.getBody():
            pygame.draw.rect(window, pygame.Color(0, 255, 0),pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(window, pygame.Color(255, 0, 0),pygame.Rect(foodPos[0], foodPos[1], 10, 10))
        if(snake.checkCollision()==1):
            break
        count-=1
        pygame.display.set_caption("Score: "+ str(score))
        pygame.display.flip()
        fps.tick(x)
        # with open("genome"+str(genomeId)+".pkl", 'wb') as output:
        #     pickle.dump(genome, output, 1)
x=1000
currentdir = os.getcwd()
configdir = currentdir + '\\config-feedforward.txt'
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configdir)
genome  = pickle.load(open(currentdir + '\\winner1.pkl', 'rb'))
main(genome, config)
