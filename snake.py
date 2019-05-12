#!/usr/bin/env python

import unicornhathd
import time, colorsys
from random import randint
import keyboard

SHOW_STATE_CHANGE_INDICATOR = True;
SLEEP_BETWEEN_FRAMES = .5

#############################
class Game:
    
    def __init__(self):
        self.state = "alive" # alive, lost, won
        self.snake = Snake() # create snake
        self.food = FoodItem() #  create food
    
    def advanceState(self):
        
        if (self.snake.isForwardOutOfBounds()):
            self.state = "lost"
        elif(self.snake.isForwardfood(self.food)):
            self.state = "won"
        else:    
            self.snake.moveForward()
        
        # todo potentially die
        # todo potentially eat, get longer, make new food
        # todo move snake
    
#############################
class Snake:
    
    def __init__(self):
        self.head = SnakeSegment()
        self.tail = self.head
        self.direction = "r" # options: udlr

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
        
    def isForwardfood(self, food):
        if(self.getNextX() == food.x and self.getNextY() == food.y):
            return True
        else:
            return False
        
    def isForwardSnake(self):
        x=1 # todo
        
    def isForwardOutOfBounds(self):
        if(self.getNextX() < 0 or self.getNextX() > 15
            or self.getNextY() < 0 or self.getNextY() > 15):
            return True
        else:
            return False

    def moveForward(self):
        newx = self.getNextX()
        newy = self.getNextY()
        
        self.head.x = newx
        self.head.y = newy
        # todo update snake segments moving in current direction
  
#############################
class SnakeSegment:
    
    def __init__(self):
        self.x = 3
        self.y = 3
        self.forwardSegment = 0
        self.backwardSegment = 0
        
#############################
class FoodItem:
    
    def __init__(self):
        self.x = 9
        self.y = 9
        
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
    
    # todo draw snake
    x = game.snake.head.x
    y = game.snake.head.y
    
    # sets the pixels on the unicorn hat
    unicornhathd.set_pixel(x, y, r, g, b)

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
            print ("up")
            game.snake.direction = "u"
        elif keyboard.is_pressed('s'):
            print ("down")
            game.snake.direction = "d"
        elif keyboard.is_pressed('a'):
            print ("left")
            game.snake.direction = "l"
        elif keyboard.is_pressed('d'):
            print ("right")
            game.snake.direction = "r"

        game.advanceState()

except KeyboardInterrupt:
    unicornhathd.off()



