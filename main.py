import time
import pygame

import menu
import physicsEngine
import gameHandler
import render

from constants import *
from classes import *

pygame.init()

win = pygame.display.set_mode(( render.WIDTH, render.HEIGHT))
pygame.display.set_caption("Haxclone")

clock = pygame.time.Clock()

menu.init()
gameHandler.loadStadium( gameHandler.stadium)
gameHandler.menuMatch = gameHandler.loadRecord("./assets/menu_match")
render.logo = pygame.image.load("./assets/images/haxball.png").convert_alpha()

currentKeys = pygame.key.get_pressed()
mousePressed = pygame.mouse.get_pressed()

Player("Player 1", "RED", ARROWS)
#Player("Player 2", "BLUE", WASD)

while gameHandler.run:
    clock.tick(120)

    events = pygame.event.get()

    previousKeys = currentKeys
    currentKeys = pygame.key.get_pressed()
    mouseWasPressed = mousePressed
    mousePressed = pygame.mouse.get_pressed()
        
    menu.update( previousKeys, currentKeys, mouseWasPressed, mousePressed, events)
    gameHandler.update( win, clock, previousKeys, currentKeys)  
    
    pygame.display.update()
pygame.quit()

#created by Tomasz Ociepka 2018
