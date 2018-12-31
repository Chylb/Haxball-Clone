import pygame

import menu
import physicsEngine
from constants import *

pygame.init()
background_image = None
logo = None

WIDTH = 1400
HEIGHT = 900

def drawButton(window, button):
    if button.section == menu.gameSection:
        if button.isPressed:
            pygame.draw.rect( window, button.colorPressed, (button.x, button.y, button.w, button.h))
        elif button.isOver:
            pygame.draw.rect( window, button.colorOver, (button.x, button.y, button.w, button.h))
        else:
            pygame.draw.rect( window, button.color, (button.x, button.y, button.w, button.h))

        window.blit( button.label, button.label_rect)

def drawPlayerBar(window, bar):
    if menu.gameSection == 1:
        if bar.isOver:
            color = bar.colorOver
        else:
            color = bar.color
            
        pygame.draw.rect( window, color, ( bar.x , bar.y, bar.w, bar.h))

        window.blit( bar.label, bar.label_rect)

def drawDropdownItem(window, item):
    if menu.isDropdownListActive:
        if item == menu.dropdownSelectedItem:
            pygame.draw.rect( window, item.colorOver, (item.x, item.y, item.w, item.h))
        else:
            pygame.draw.rect( window, item.color, (item.x, item.y, item.w, item.h))
        window.blit( item.label, item.label_rect)     

def drawPlayer(window, x, y, zoom, player):
    if player.kicking or player.hasKicked: 
        pygame.draw.circle(window, WHITE, ( int((player.x - x) * zoom), int((player.y - y) * zoom)), int(player.r * zoom), 0)
        if player.hasKicked:
            player.hasKicked = False
    else:
        pygame.draw.circle(window, BLACK, ( int((player.x - x) * zoom), int((player.y - y) * zoom)), int(player.r * zoom), 0) 

    if player.team == "RED":      
        pygame.draw.circle(window, PLAYER_RED, ( int((player.x - x) * zoom), int((player.y - y) * zoom)), int( (player.r - 3) * zoom), 0) 
    elif player.team == "BLUE":
        pygame.draw.circle(window, PLAYER_BLUE, ( int((player.x - x) * zoom), int((player.y - y) * zoom)), int( (player.r - 3) * zoom), 0)

def drawPlayerNick(window, x, y, zoom, player):
    font = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf", int(18 * zoom))
    label = font.render( player.nick, True, WHITE)
    window.blit( label, label.get_rect( center=( (player.x - x) * zoom, (player.y - y + 40) * zoom)))

def drawBall(window, x, y, zoom, ball):
    pygame.draw.circle(window, BLACK, ( int((ball.x - x) * zoom), int((ball.y - y) * zoom)), int(ball.r * zoom), 0)
    pygame.draw.circle(window, ball.color, ( int((ball.x - x) * zoom), int((ball.y - y) * zoom)), int((ball.r - 3) * zoom), 0)

def drawPost(window, x, y, zoom, post):
    pygame.draw.circle(window, BLACK, ( int((post.x - x) * zoom), int((post.y - y) * zoom)), int(post.r * zoom), 0)
    pygame.draw.circle(window, post.color, ( int((post.x - x) * zoom), int((post.y - y) * zoom)), int((post.r - 3) * zoom), 0)

def drawLine(window, x, y, zoom, line):
    if line.visible: pygame.draw.line(window, line.color, [ int((line.x1 - x) * zoom), int((line.y1 - y) * zoom) ], [ int((line.x2 - x) * zoom), int((line.y2 - y) * zoom) ], int(line.width * zoom))

def drawArc(window, x, y, zoom, arc):
    if arc.visible: pygame.draw.arc(window, arc.color, ( int( (arc.x - x - arc.r) * zoom), int( (arc.y - y - arc.r) * zoom), int(2 * arc.r * zoom) , int(2 * arc.r * zoom)), arc.a0, arc.a, int(arc.width * zoom))

def screenUpdate(window, x, y, zoom, physicObjects):
    window.fill( BACKGROUND_GREEN)

    bgW = int(background_image.get_rect().size[0] * zoom)
    bgH = int(background_image.get_rect().size[1] * zoom)
    bimg = pygame.transform.scale( background_image, (bgW, bgH))

    x -= (WIDTH / 2) / zoom
    y -= (HEIGHT / 2) / zoom

    x0 = int( (-x * zoom) % bgW - bgW)
    y0 = int( (-y * zoom) % bgH - bgH)
    
    for xb in range( x0, WIDTH, bgW):
        for yb in range( y0, HEIGHT, bgH):
            window.blit(bimg, (xb, yb))

    if physicObjects is not None:
        
        for line in physicObjects['lines']:
            drawLine(window, x, y, zoom, line)

        for visualLine in physicObjects['visualLines']:
            drawLine(window, x, y, zoom, visualLine)

        for kickoffline in physicObjects['kickoffLines']:
            drawLine(window, x, y, zoom, kickoffline)

        for arc in physicObjects['arcs']:
            drawArc(window, x, y, zoom, arc)

        for kickoffArc in physicObjects['kickoffArcs']:
            drawArc(window, x, y, zoom, kickoffArc)
        
        for player in physicObjects['players']:
            drawPlayer(window, x, y, zoom, player)

        for ball in physicObjects['balls']:
            drawBall(window, x, y, zoom, ball)

        for post in physicObjects['posts']:
            drawPost(window, x, y, zoom, post)

        for player in physicObjects['players']:
            drawPlayerNick(window, x, y, zoom, player)
        
    #MENU

    for button in menu.buttonList:
        drawButton(window, button)

    for bar in menu.playerBarList:
        drawPlayerBar(window, bar)

    for item in menu.dropdownList:
        drawDropdownItem(window, item)

    if menu.gameSection == 0:
        window.blit( logo, (WIDTH/2 - logo.get_rect().size[0]/2, HEIGHT/2 - logo.get_rect().size[1]/2 - 300))

