#!/usr/bin/env python

import unicornhathd
import time, colorsys
from random import randint
import keyboard

SHOW_STATE_CHANGE_INDICATOR = True;
SLEEP_BETWEEN_FRAMES = .1
FOOD_COUNT_TO_WIN = 5

#############################
class Game:
    
    def __init__(self):
        self.state = "alive" # alive, lost, won
        self.snake = Snake() # create snake
        self.food = self.makeNewFood() #  create food
        self.ateCount = 0 # number of foods eaten
    
    def advanceState(self):
        
        moveOutcome = self.snake.moveForward(self.food)
                
        # outOfBounds, ate, ateSelf, moved
        if (moveOutcome == "outOfBounds" or moveOutcome == "ateSelf"):
            self.state = "lost"
        elif(moveOutcome == "ate" and self.ateCount+1 == FOOD_COUNT_TO_WIN):
            self.state = "won"
        elif(moveOutcome == "ate"):
            self.ateCount += 1
            self.food = self.makeNewFood()
            
    def makeNewFood(self):
        
        newFoodOverlapsWithSnake = True
        while(newFoodOverlapsWithSnake):
            x = randint(0,15)
            y = randint(0,15)
            newFoodOverlapsWithSnake = self.snake.doCoordsOverlap(x,y)
        
        return FoodItem(x,y)
    
#############################
class Snake:
    
    def __init__(self):
        self.head = SnakeSegment()
        self.tail = self.head
        self.direction = "r" # direction of head. options: udlr
        self.len = 1

    def setDirection(self, newDirection):
        if(self.len == 1):
            self.direction = newDirection
        else: # if len > 1
            if(self.direction == "l" and newDirection == "r"):
                return
            if(self.direction == "r" and newDirection == "l"):
                return
            if(self.direction == "u" and newDirection == "d"):
                return
            if(self.direction == "d" and newDirection == "u"):
                return
            self.direction = newDirection

    def doCoordsOverlap(self, x, y):
        currentSegment = self.head
        while(currentSegment != 0):
            if(currentSegment.x == x and currentSegment.y == y):
                return True
            currentSegment = currentSegment.backwardSegment
        return False

    def doCoordsOverlapExcludingTail(self, x, y):
        currentSegment = self.head
        while(currentSegment != 0 and currentSegment != self.tail):
            if(currentSegment.x == x and currentSegment.y == y):
                return True
            currentSegment = currentSegment.backwardSegment
        return False

    def changeDirection(self, direction):
        self.direction = direction

    def getNextX(self):
        if(self.direction == "u"):
            return self.head.x - 1
        elif(self.direction == "d"):
            return self.head.x + 1
        else:
            return self.head.x

    def getNextY(self):
        if(self.direction == "l"):
            return self.head.y - 1
        elif(self.direction == "r"):
            return self.head.y + 1
        else:
            return self.head.y
        
    def isForwardFood(self, food):
        if(self.getNextX() == food.x and self.getNextY() == food.y):
            return True
        else:
            return False
        
    def isForwardSnake(self):
        return self.doCoordsOverlapExcludingTail(self.getNextX(), self.getNextY())
        
    def isForwardOutOfBounds(self):
        if(self.getNextX() < 0 or self.getNextX() > 15
            or self.getNextY() < 0 or self.getNextY() > 15):
            return True
        else:
            return False

    # moves snake forward. can return strings: outOfBounds, ate, ateSelf, moved
    def moveForward(self, food):

        newx = self.getNextX()
        newy = self.getNextY()

        if (self.isForwardOutOfBounds()):
            return "outOfBounds"
        elif(self.isForwardSnake()):
            return "ateSelf"
        elif(self.isForwardFood(food)):
            # extend length by adding a head but keep tail in same place
            self.len += 1
           
            newHead = SnakeSegment()
            newHead.x = newx
            newHead.y = newy
            newHead.forwardSegment = 0
            newHead.backwardSegment = self.head
            self.head.forwardSegment = newHead
            self.head = newHead

            return "ate"
        else:
            
            if(self.len == 1):
                self.head.x = newx
                self.head.y = newy
            else:
                # maintain length by moving head forward and removing tail
                newHead = SnakeSegment()
                newHead.x = newx
                newHead.y = newy
                newHead.forwardSegment = 0
                newHead.backwardSegment = self.head
                self.head.forwardSegment = newHead
                self.head = newHead
                
                newTail = self.tail.forwardSegment
                newTail.backwardSegment = 0
                self.tail = newTail

            return "moved"
  
#############################
class SnakeSegment:
    
    def __init__(self):
        self.x = 3
        self.y = 3
        self.forwardSegment = 0
        self.backwardSegment = 0
        
#############################
class FoodItem:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
#############################
def drawSnake(game):
    
    h = 0.4 # color = blue
    s = 0.95 # saturation
    v = 1 # brightness

    # convert the hsv back to RGB
    rgb = colorsys.hsv_to_rgb(h, s, v) 
    
    # makes a 0-1 range into a 0-255 range
    # and rounds it to a whole number
    r = int(rgb[0]*255.0) 
    g = int(rgb[1]*255.0)
    b = int(rgb[2]*255.0)
    
    # draw snake
    currentSegment = game.snake.head
    while(currentSegment != 0):
        # sets the pixels on the unicorn hat
        unicornhathd.set_pixel(currentSegment.x, currentSegment.y, r, g, b)
        currentSegment = currentSegment.backwardSegment

#############################
def drawFood(game):
    x = game.food.x
    y = game.food.y

    unicornhathd.set_pixel_hsv(x,y,0.2,1,1) #xyhsv

#############################
def drawBlinker(blinkerState):
    unicornhathd.set_pixel_hsv(0,0,0.4,1,blinkerState*.1) #xyhsv

#############################
# init
unicornhathd.brightness(1)
#need to rotate the image to have the heart the right way up
unicornhathd.rotation(90)

game = Game()
blinkerState = 0

try:
    
    while True:
        
        unicornhathd.clear() # clear all pixels
        
        if(game.state == "alive"):
            drawSnake(game)
            drawFood(game)
        elif(game.state == "lost"):
            #todo display win or loss
            print ("You lost...!")
            raise Exception
        elif(game.state == "won"):
            #todo display win or loss
            print ("Yay! You WON!")
            raise Exception
        
        if (SHOW_STATE_CHANGE_INDICATOR):
            drawBlinker(blinkerState)
            blinkerState = 1 - blinkerState
        
        unicornhathd.show() # show the pixels
        time.sleep(SLEEP_BETWEEN_FRAMES)
        
        if keyboard.is_pressed('w'):
            game.snake.setDirection("u")
        elif keyboard.is_pressed('s'):
            game.snake.setDirection("d")
        elif keyboard.is_pressed('a'):
            game.snake.setDirection("l")
        elif keyboard.is_pressed('d'):
            game.snake.setDirection("r")

        game.advanceState()

except KeyboardInterrupt:
    unicornhathd.off()



