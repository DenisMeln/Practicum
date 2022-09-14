import pygame
import random

asteroid = pygame.image.load("pics/asteroid.png")
asteroid = pygame.transform.scale(asteroid, (80, 80))

class Asteroid(object):
    def __init__(self):
        self.img = asteroid
        self.width = 50
        self.height = 50
        self.place = random.choice([(random.randrange(0, 800 - self.width), random.choice([-1 * self.height - 5, 805])),
                                    (random.choice([-1 * self.width - 5, 805]), random.randrange(0, 800 - self.height))])
        self.x, self.y = self.place
        if self.x < 400:
            self.x_direction = 1
        else: self.x_direction = -1
        if self.y < 400:
            self.y_direction = 1
        else: self.y_direction = -1
        self.x_new = self.x_direction * random.randrange(1, 3)
        self.y_new = self.y_direction * random.randrange(1, 3)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def checkBorders(self):
        if self.x > 850:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = 800
        elif self.y < 0 - self.height:
            self.y = 800
        elif self.y > 850:
            self.y = 0