from ball import *
from paddle import *

import pygame
from pygame.locals import *

class CollisionHandler:
    _balls = []
    _objects = []
    
    def __init__(self):
        pass
    
    def addBall(self, ball):
        self._balls.append(ball)
    
    def addObject(self, object):
        self._objects.append(object)
    
    def update(self):
        i = 1
        for ball in self._balls:
            for obj in self._objects:
                self._ballOnObject(ball, obj)
            for ball2 in self._balls[i:]:
                self._ballOnBall(ball, ball2)
            i += 1
    
    def _ballOnObject(self, ball, obj):
        if ball.x - ball.radius > obj.x + obj.w: # Om bollen ar till hoger om objectet...
            if ball.x - ball.radius + ball.vx < obj.x + obj.w: # Och kommer att vara krocka nasta gang...
                if ball.y >= obj.y and ball.y <= obj.y + obj.h: # Och ligger ratt i y-led
                    ball.vx *= -1
        if ball.x + ball.radius < obj.x: # Om bollen ar till vanster om objectet...
            if ball.x + ball.radius + ball.vx > obj.x: # Och kommer att vara krocka nasta gang...
                if ball.y >= obj.y and ball.y <= obj.y + obj.h: # Och ligger ratt i y-led
                    ball.vx *= -1
        if ball.y - ball.radius > obj.y + obj.h: # Om bollen ar under objectet...
            if ball.y - ball.radius + ball.vy < obj.y + obj.h: # Och kommer att vara krocka nasta gang...
                if ball.x >= obj.x and ball.x <= obj.x + obj.w: # Och ligger ratt i x-led
                    ball.vy *= -1
        if ball.y + ball.radius < obj.y: # Om bollen ar till ovanfor objectet...
            if ball.y + ball.radius + ball.vy > obj.y: # Och kommer att vara krocka nasta gang...
                if ball.x >= obj.x and ball.x <= obj.x + obj.w: # Och ligger ratt i x-led
                    ball.vy *= -1
    
    def _ballOnBall(self, ball1, ball2):
        pass
