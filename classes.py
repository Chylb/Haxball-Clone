import pygame
import physicsEngine
import math
import menu
import gameHandler

#MENU CLASSES

class Button(object):
    def __init__(self, section, x, y, w, h, string, alignLeft, font, textColor, color, colorOver, colorPressed, f, argument):
        self.section = section
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.string = string
        self.alignLeft = alignLeft
        self.font = font
        self.textColor = textColor

        self.label = self.font.render( self.string, True, self.textColor)
        self.label_rect = self.label.get_rect( center=( x + w/2, y + h/2))
        if self.alignLeft:
            self.label_rect.left = self.x + 5
        
        self.color = color
        self.colorPressed = colorPressed
        self.colorOver = colorOver

        self.wasPressed = False
        self.isPressed = False
        self.isOver = False

        self.f = f
        self.argument = argument
        
        menu.buttonList.append(self)

    def update(self):
        self.label = self.font.render( self.string, True, self.textColor)
        self.label_rect = self.label.get_rect( center=( self.x + self.w/2, self.y + self.h/2))
        if self.alignLeft:
            self.label_rect.left = self.x + 5

class PlayerBar(object):
    def __init__(self, player):
        self.player = player
    
        if player.team == "RED":
            self.pos = gameHandler.redPlayersCount
        elif player.team == "BLUE":
            self.pos = gameHandler.bluePlayersCount
        else:
            self.pos = gameHandler.spectatorsCount

        self.isOver = False
        self.colorOver = (27, 35, 40)
        self.color = (17,22,25)

        self.x = 0
        self.y = 0
        self.w = 220
        self.h = 25

        self.updateCoordinates()

        self.updateName()
        
        menu.playerBarList.append(self)

    def updateName(self):
        self.label = menu.lightFont.render( self.player.nick, True, (255,255,255))
        self.label_rect = self.label.get_rect( center=( self.x + self.w/2, self.y + self.h/2))
        self.label_rect.left = self.x + 5

    def updateCoordinates(self):
        if self.player.team == "RED":
            self.x = menu.redTeamBox.x
        elif self.player.team == "BLUE":
            self.x = menu.blueTeamBox.x
        else:
            self.x = menu.spectatorTeamBox.x
        self.y = menu.spectatorTeamBox.y + (self.pos - 1) * self.h

    def openOptions(self):
        menu.gameSection = 4
        menu.selectedPlayerBar = self
        menu.nickBox.string = self.player.nick
        menu.nickBox.update()

class DropdownItem(object):
    def __init__(self, x, y, w, h, string, font, color, colorOver, f, argument):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.string = string
        self.font = font

        self.label = self.font.render( self.string, True, (255,255,255))
        self.label_rect = self.label.get_rect( center=( x + w/2, y + h/2))
        self.label_rect.left = self.x + 5
        
        self.color = color
        self.colorOver = colorOver

        self.wasPressed = False
        self.isPressed = False
        self.isOver = False

        self.f = f
        self.argument = argument
        
        menu.dropdownList.append(self)
        
#PHYSIC OBJECTS CLASSES
        
class Player(object):
    def __init__(self, nick, team, keys):
        self.nick = nick
        self.team = team
        self.kicking = False
        
        self.x = 100000
        self.y = 100000
        
        self.vx = 0
        self.vy = 0
        self.r = 26
        self.mass = 25

        self.keyUp = keys[0]
        self.keyDown = keys[1]
        self.keyLeft = keys[2]
        self.keyRight = keys[3]
        self.keyKick = keys[4]
        
        if team == "RED":
            gameHandler.redPlayersCount += 1
        elif team == "BLUE":
            gameHandler.bluePlayersCount += 1
        else:
            gameHandler.spectatorsCount += 1
        
        self.hasKicked = False #only for rendering purpose

        physicsEngine.playerList.append(self)
        
        PlayerBar( self)

    def steer(self, previousKeys, currentKeys):
        vertical = 0
        horizontal = 0
        
        if currentKeys[self.keyUp]:
            vertical -= gameHandler.playerAcceleration
        if currentKeys[self.keyDown]:
            vertical += gameHandler.playerAcceleration
        if currentKeys[self.keyLeft]:
            horizontal -= gameHandler.playerAcceleration
        if currentKeys[self.keyRight]:
            horizontal += gameHandler.playerAcceleration
        if currentKeys[self.keyKick]:
            if self.kicking:
                self.kicking = True
            elif previousKeys[self.keyKick]:
                self.kicking = False
                #if you've kicked the ball you have to press the key once again in order to kick the ball
            else:
                self.kicking = True
        else:
            self.kicking = False

        self.hasKicked = False

        if self.kicking:
            vertical *= 0.7
            horizontal *= 0.7
        if horizontal != 0 and vertical != 0:
            vertical /= 1.41421356237
            horizontal /= 1.41421356237

        self.vx += horizontal
        self.vy += vertical
        
class Ball(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        
        self.vx = 0
        self.vy = 0
        self.r = r
        
        self.mass = 15
        self.color = color
        physicsEngine.ballList.append(self)

class Post(object):
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        
        self.color = color
        physicsEngine.postList.append(self)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        physicsEngine.pointList.append(self)

class Wall(object):
    #A * x + B * y + C = 0
    def __init__(self, a, b, c):
        self.A = a
        self.B = b
        self.C = c

        physicsEngine.wallList.append(self)

class Line(object):
    def __init__(self, x1, y1, x2, y2, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.xm = (x1 + x2)/2
        self.ym = (y1 + y2)/2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2 )**1

        self.color = color
        self.width = width
        self.visible = visible

        physicsEngine.lineList.append(self)

class VisualLine(object):
    def __init__(self, x1, y1, x2, y2, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.color = color
        self.width = width
        self.visible = visible

        physicsEngine.visualLineList.append(self)

class Goal(object):
    def __init__(self, team, x1, y1, x2, y2):
        self.team = team
        self.score = 0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.xm = (x1 + x2)/2
        self.ym = (y1 + y2)/2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2 )**1

        physicsEngine.goalList.append(self)

class Arc(object):
    def __init__(self, x, y, r, a0, a, color, width, visible):
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a = a

        self.color = color
        self.width = width
        self.visible = visible

        self.point1 = Point( x + r * math.cos(a0), y - r * math.sin(a0))
        self.point2 = Point( x + r * math.cos(a), y - r * math.sin(a))
        
        physicsEngine.arcList.append(self)

class KickoffPoint(object):
    def __init__(self, x, y, team):
        self.x = x
        self.y = y
        self.team = team
        
        physicsEngine.kickoffPointList.append(self)

class KickoffLine(object):
    def __init__(self, x1, y1, x2, y2, team, color, width, visible):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.xm = (x1 + x2)/2
        self.ym = (y1 + y2)/2

        self.A = self.y2 - self.y1
        self.B = self.x1 - self.x2
        self.C = self.x2 * self.y1 - self.x1 * self.y2

        self.r = ((self.x1 - self.xm)**2 + (self.y1 - self.ym)**2 )**1
        self.team = team
        self.color = color
        self.width = width
        self.visible = visible

        physicsEngine.kickoffLineList.append(self)     

class KickoffArc(object):
    def __init__(self, x, y, r, a0, a, team, color, width, visible):
        self.x = x
        self.y = y
        self.r = r
        self.a0 = a0
        self.a = a

        self.point1 = KickoffPoint( x + r * math.cos(a0), y - r * math.sin(a0), team)
        self.point2 = KickoffPoint( x + r * math.cos(a), y - r * math.sin(a), team)

        self.team = team
        self.color = color
        self.width = width
        self.visible = visible
        
        physicsEngine.kickoffArcList.append(self)
