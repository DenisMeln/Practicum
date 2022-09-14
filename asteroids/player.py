import pygame
import math

rocket = pygame.image.load("pics/rocket.png")
rocket = pygame.transform.scale(rocket, (100, 100))

class Player(object):
    def __init__(self):
        self.img = rocket
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = 400
        self.y = 400
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosinus = math.cos(math.radians(self.angle + 90))
        self.sinus = math.sin(math.radians(self.angle + 90))
        self.top = (self.x + self.cosinus * self.width // 2, self.y - self.sinus * self.height // 2)

    def draw(self, window):
        window.blit(self.rotatedSurf, self.rotatedRect)

    def left(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self. y)
        self.cosinus = math.cos(math.radians(self.angle + 90))
        self.sinus = math.sin(math.radians(self.angle + 90))
        self.top = (self.x + self.cosinus * self.width // 2, self.y - self.sinus * self.height // 2)

    def right(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self. y)
        self.cosinus = math.cos(math.radians(self.angle + 90))
        self.sinus = math.sin(math.radians(self.angle + 90))
        self.top = (self.x + self.cosinus * self.width // 2, self.y - self.sinus * self.height // 2)

    def move(self):
        self.x += self.cosinus * 5
        self.y -= self.sinus * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosinus = math.cos(math.radians(self.angle + 90))
        self.sinus = math.sin(math.radians(self.angle + 90))
        self.top = (self.x + self.cosinus * self.width // 2, self.y - self.sinus * self.height // 2)

    def checkBorders(self):
        if self.x > 850:
            self.x = 0
        elif self.x < 0 - self.width:
            self.x = 800
        elif self.y < 0 - self.height:
            self.y = 800
        elif self.y > 850:
            self.y = 0