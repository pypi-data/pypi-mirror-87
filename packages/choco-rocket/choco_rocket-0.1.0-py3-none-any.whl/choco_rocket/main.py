# choco_rocket_beta.py

import pygame
import sys
import random
from pygame.locals import *


class Enemies:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('images/meteor.png'), (80, 55))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Player:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load('images/p1.png'), (70, 80))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

def main():
    pygame.init()
    pygame.font.init()

    # DISPLAY
    WIDTH, HEIGHT = 700, 400
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ChocoRocket")

    # Background
    BG = pygame.transform.scale(pygame.image.load("images/bg.png"), (WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    lives = 3
    score = 0
    font = pygame.font.SysFont("comicsans", 40)
    
    x, y = 0, 200 
    vel = 5
    vel_meteor = 4
    p1 = Player(0, 200)
    meteor = Enemies(660, random.randint(10, 200))

    def redraw_window():
        WIN.blit(BG, (0, 0))
        # label score and lives on the screen
        lives_label = font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = font.render(f"Score: {score}", 1, (255, 255, 255))
        
        WIN.blit(lives_label, (10, 10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10, 10))

        # drawing the player
        p1.draw(WIN)
        
        # drawing the meteor
        meteor.draw(WIN)
        pygame.display.update()


    # Game loop
    while True:
        clock.tick(60)
        redraw_window()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and p1.y - vel > 20:
            p1.y -= vel
        if keys[pygame.K_DOWN] and p1.y + vel + 80 < HEIGHT:
            p1.y += vel
        
        meteor.x -= vel_meteor

        if meteor.x == p1.x or meteor.x < p1.x:
            meteor.y = random.randint(32, 400-55)
            meteor.x = 660
            score += 1
            vel_meteor +=  0.5
            if vel_meteor > 12:
                vel_meteor = 12


if __name__ == "__main__":
    main()
