import pygame
import glob, os
import zlib
import _pickle as pickle

import menu
import physicsEngine
import render
from render import WIDTH, HEIGHT

from constants import *
from classes import *

pygame.mixer.pre_init(22050, -16, 2, 800)
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=800)

kickSound = pygame.mixer.Sound('./assets/sounds/kick.wav')
goalSound = pygame.mixer.Sound('./assets/sounds/goal.wav')
joinedSound = pygame.mixer.Sound('./assets/sounds/joined.wav')
leftSound = pygame.mixer.Sound('./assets/sounds/left.wav')

run = True #main loop guard

#DEFAULT OPTIONS
stadium = "Classic"
whoseBall = "RED"

timeLimit = 3
scoreLimit = 3


redScore = 0
blueScore = 0

redPlayersCount = 0
bluePlayersCount = 0
spectatorsCount = 0

started = False
kickedOff = False
paused = True

resuming = False
timeToResume = 0 

isCelebrating = False
celebrationTime = 0
celebrationLength = 0

isEnding = False
timeToEnd = 0
overtime = False

time = 0 #match time

physicObjects = []
menuMatch = []
menuMatchTick = 0
matchRecord = []

defaultZoom = 1
stadiumWidth = 0
stadiumHeight = 0

replaysTurnedOn = True
inReplay = False
replayTick = 0
lastRedTouch = 0
lastBlueTouch = 0
scorer = 0
lastRedTouchPlayer = 0
lastBlueTouchPlayer = 0
lastScorerTouch = 0

#MATCH EVENTS
def startNewMatch():
    global started
    global kickedOff
    global paused
    global resuming
    global isCelebrating
    global isEnding
    global time
    global blueScore
    global redScore
    global whoseBall
    global inReplay
    
    started = True
    kickedOff = False
    paused = False
    resuming = False
    isCelebrating = False
    isEnding = False
    time = 0
    blueScore = 0
    redScore = 0
    whoseBall = "RED"
    inReplay = False
    toStartingPositions()

def pauseMatch():
    global paused 
    paused = True

def resumeMatch():
    global paused
    global resuming
    global timeToResume
    
    paused = False
    resuming = True
    timeToResume = 2000

def score( team):
    global redScore
    global blueScore
    global whoseBall

    global isCelebrating
    global celebrationTime
    global celebrationLength

    global replayTick
    global scorer
    global lastScorerTouch
    
    if not isCelebrating:
        
        if team == "RED":
            redScore += 1
            whoseBall = "BLUE"
            menu.upperInfo.string = "Red"
            replayTick = lastRedTouch + 400
            lastScorerTouch = lastRedTouch
            scorer = lastRedTouchPlayer
        elif team == "BLUE":
            blueScore += 1
            whoseBall = "RED"
            menu.upperInfo.string = "Blue"
            replayTick = lastBlueTouch + 400
            scorer = lastBlueTouchPlayer
            lastScorerTouch = lastBlueTouch
            
        menu.lowerInfo.string = "Scores!"
        isCelebrating = True
        celebrationTime = 0
        celebrationLength = 2000

def toStartingPositions():
    physicsEngine.ballList[0].x = 0
    physicsEngine.ballList[0].y = 0
    physicsEngine.ballList[0].vx = 0
    physicsEngine.ballList[0].vy = 0

    redX = physicsEngine.goalList[0].x1 + 200
    blueX = physicsEngine.goalList[1].x1 - 200

    redGap = stadiumHeight / (redPlayersCount +1)
    blueGap = stadiumHeight / (bluePlayersCount +1)
    redIte = 1
    blueIte = 1
    
    for player in physicsEngine.playerList:
        if player.team == "RED":
            player.x = redX
            player.y = -stadiumHeight/2 + redGap * redIte
            redIte += 1
        
        elif player.team == "BLUE": 
            player.x = blueX
            player.y = -stadiumHeight/2 + blueGap * blueIte
            blueIte += 1
        else:
            player.x = 100000        

        player.vx = 0
        player.vy = 0

def putPlayerOnPitch( player):
    if player.team == "RED":
        player.x = physicsEngine.goalList[0].x1  - 20
    elif player.team == "BLUE":
        player.x = physicsEngine.goalList[1].x1 + 20
    else: player.x = -10000
    player.y = 0
              
def resetReplay():
    global matchRecord
    global lastRedTouch 
    global lastBlueTouch 
    global lastRedTouchPlayer 
    global lastBlueTouchPlayer

    matchRecord.clear()
    lastRedTouch = 0
    lastBlueTouch = 0 
    lastRedTouchPlayer = 0 
    lastBlueTouchPlayer = 0
    
def update( win, clock, previousKeys, currentKeys):
    global redScore
    global blueScore

    global started
    global kickedOff
    global paused 

    global resuming 
    global timeToResume
    global isEnding

    global isCelebrating
    global celebrationTime
    global celebrationLength

    global overtime
    global time

    global physicObjects
    global menuMatch
    global menuMatchTick
    global matchRecord

    global inReplay
    global replayTick 
    global lastRedTouch 
    global lastBlueTouch
    global scorer
    global lastRedTouchPlayer 
    global lastBlueTouchPlayer
    global lastScorerTouch
  
    #PHYSICS UPDATE
    if menu.gameSection == 2 and gameHandler.started and not gameHandler.paused and not gameHandler.resuming and not inReplay:
        physicObjects = physicsEngine.update( previousKeys, currentKeys)
        if replaysTurnedOn:
            matchRecord.insert(0, pickle.loads( pickle.dumps( physicObjects, -1))) #it's much more efficient way of copying
            
        if len( matchRecord) > 1200:
            matchRecord.pop()

        lastRedTouch += 1
        lastBlueTouch += 1
        if isCelebrating:
            lastScorerTouch += 1       

    menu.upperInfo.x = -1000
    menu.lowerInfo.x = -1000
    menu.upperShadow.x = -1000
    menu.lowerShadow.x = -1000
    menu.pauseBar.x = -1000
    menu.upperInfo.update()
    menu.lowerInfo.update()
    menu.upperShadow.update()
    menu.lowerShadow.update()
    menu.pauseBar.update()

    if started and (paused or resuming):
        menu.upperInfo.x = WIDTH/2
        menu.lowerInfo.x = WIDTH/2
        menu.upperInfo.string = "Game"
        menu.lowerInfo.string = "Paused"
        menu.upperInfo.textColor = WHITE
        menu.lowerInfo.textColor = WHITE
        menu.upperInfo.update()
        menu.lowerInfo.update()

        menu.upperShadow.x = WIDTH/2 + 5
        menu.lowerShadow.x = WIDTH/2 + 5
        menu.upperShadow.string = "Game"
        menu.lowerShadow.string = "Paused"
        menu.upperShadow.update()
        menu.lowerShadow.update()

    if started and not paused:
        if resuming: 
            if timeToResume <= 0:
                resuming = False
            else:
                menu.pauseBar.w = timeToResume / 20
                menu.pauseBar.x = WIDTH/2 - timeToResume / 40
                menu.pauseBar.update()
                timeToResume -= clock.get_time()
        elif isCelebrating:
            if celebrationTime >= celebrationLength: #end of celebration
                isCelebrating = False
                toStartingPositions()
                kickedOff = False

                if replaysTurnedOn:
                    inReplay = True

                if isEnding:
                    menu.gameSection = 1
                    menu.startGame( menu.startButton, None) #It actually stops the game by simulating pressing the stop button
                    menu.upperInfo.x = -1000
                    isEnding = False
    
            else:
                celebrationTime += clock.get_time()
     
                if isEnding and celebrationTime > 2000:
                    if whoseBall == "RED":
                        menu.upperInfo.string = "Blue is"
                        menu.upperShadow.string = "Blue is"
                        menu.upperInfo.textColor = PLAYER_BLUE
                        menu.lowerInfo.textColor = PLAYER_BLUE             
                    elif whoseBall == "BLUE":
                        menu.upperInfo.string = "Red is"
                        menu.upperShadow.string = "Red is"
                        menu.upperInfo.textColor = PLAYER_RED
                        menu.lowerInfo.textColor = PLAYER_RED
                        
                    menu.lowerInfo.string = "Victorious!"
                    menu.lowerShadow.string = "Victorious!"
                    
                    menu.upperInfo.x = WIDTH/2 + ((celebrationTime-3000)**3)/1000000
                    menu.lowerInfo.x = WIDTH/2 - ((celebrationTime-3000)**3)/1000000
                    menu.upperShadow.x = WIDTH/2 + ((celebrationTime-3000)**3)/1000000 + 5
                    menu.lowerShadow.x = WIDTH/2 - ((celebrationTime-3000)**3)/1000000 + 5
                else:
                    if whoseBall == "RED":
                        menu.upperInfo.string = "Blue"
                        menu.upperShadow.string = "Blue"
                        menu.upperInfo.textColor = PLAYER_BLUE
                        menu.lowerInfo.textColor = PLAYER_BLUE
                    elif whoseBall == "BLUE":
                        menu.upperInfo.string = "Red"
                        menu.upperShadow.string = "Red"
                        menu.upperInfo.textColor = PLAYER_RED
                        menu.lowerInfo.textColor = PLAYER_RED
                        
                    menu.lowerInfo.string = "Scores!"
                    menu.lowerShadow.string = "Scores!"
                    
                    menu.upperInfo.x = WIDTH/2 + ((celebrationTime-1000)**3)/1000000
                    menu.lowerInfo.x = WIDTH/2 - ((celebrationTime-1000)**3)/1000000
                    menu.upperShadow.x = WIDTH/2 + ((celebrationTime-1000)**3)/1000000 + 5
                    menu.lowerShadow.x = WIDTH/2 - ((celebrationTime-1000)**3)/1000000 + 5
                    
                menu.upperInfo.update()
                menu.lowerInfo.update()
                menu.upperShadow.update()
                menu.lowerShadow.update()
        else:
            if kickedOff == True:
                time += clock.get_time()
        
        if not isEnding and not overtime and time > timeLimit * 60000 and timeLimit != 0: #triggers overtime
            overtime = True
            menu.overtimeSprite.string = "OVERTIME!"
            menu.overtimeSprite.update()
            
        if (not isEnding and scoreLimit != 0 and (redScore >= scoreLimit or blueScore >= scoreLimit)) or (overtime and blueScore != redScore):
            isCelebrating = True
            celebrationTime = 0
            celebrationLength = 4000
            isEnding = True
            overtime = False
            menu.overtimeSprite.string = ""
            menu.overtimeSprite.update()
        
    menu.scoreBar.string = str(redScore) + " - " + str(blueScore)
    minutes = time//60000
    seconds = (time - minutes * 60000)//1000
    minutes = str(minutes)
    seconds = str(seconds)
    if len( minutes) == 1: minutes = "0" + minutes
    if len( seconds) == 1: seconds = "0" + seconds
    menu.timeBar.string = str( minutes + ":" + seconds)
    menu.scoreBar.update()
    menu.timeBar.update()
    
    if menu.gameSection == 0:
        if menuMatchTick < 0:
            menuMatchTick = len( menuMatch) - 1

        render.screenUpdate( win, 0, 0, 1, menuMatch[ menuMatchTick])
        menuMatchTick -= 1
 
    elif menu.gameSection == 2 or menu.gameSection == 1 and started:
        if inReplay:
            if replayTick < 0:
                inReplay = False
                resetReplay()
            else:
                if replayTick > len( matchRecord) - 1:
                    replayTick =  len( matchRecord) - 1
                
                if replayTick < lastScorerTouch:
                    cameraX = matchRecord[ replayTick]['balls'][0].x
                    cameraY = matchRecord[ replayTick]['balls'][0].y
                else:
                    cameraX = matchRecord[ replayTick]['players'][ scorer].x
                    cameraY = matchRecord[ replayTick]['players'][ scorer].y
                    
                if whoseBall == "RED":
                    goalX = matchRecord[ replayTick]['goals'][0].x1
                    goalY1 = matchRecord[ replayTick]['goals'][0].y1
                    goalY2 = matchRecord[ replayTick]['goals'][0].y2
                elif whoseBall == "BLUE":
                    goalX = matchRecord[ replayTick]['goals'][1].x1
                    goalY1 = matchRecord[ replayTick]['goals'][1].y1
                    goalY2 = matchRecord[ replayTick]['goals'][1].y2

                distanceX = cameraX - goalX
                distanceY1 = cameraY - goalY1
                distanceY2 = cameraY - goalY2
                    
                if distanceX < 0: distanceX *= -1
                if distanceY1 < 0: distanceY1 *= -1
                if distanceY2 < 0: distanceY2 *= -1

                zoomX = 0.45 * WIDTH / distanceX
                zoomY1 = 0.46 * HEIGHT / distanceY1
                zoomY2 = 0.46 * HEIGHT / distanceY2

                cameraZoom = zoomX
                if zoomY1 < cameraZoom:
                    cameraZoom = zoomY1
                if zoomY2 < cameraZoom:
                    cameraZoom = zoomY2  
                    
                if cameraZoom > 2:
                        cameraZoom = 2    
                    
                render.screenUpdate( win, cameraX, cameraY, cameraZoom, matchRecord[ replayTick])
                    
                if menu.gameSection == 2 and not paused and not resuming and started:
                    replayTick -= 1
        else:
            render.screenUpdate( win, 0, 0, defaultZoom, physicObjects)
    else:
        render.screenUpdate( win, 0, 0, 1, None)

#OTHER FUNCTIONS

def saveRecord():
    compressed = zlib.compress( pickle.dumps( matchRecord))
    with open('./records/record', 'wb') as fp:
        pickle.dump( compressed, fp)
        
def loadRecord(path):    
    with open ( path, 'rb') as fp:
        compressed = pickle.load(fp)
        
    return pickle.loads( zlib.decompress(compressed)) 

def setDefaultSettings():
    global playerAcceleration
    global kickForce
    global playerDrag
    global ballDrag
    global stadiumWidth
    global stadiumHeight
    
    playerAcceleration = 0.045
    kickForce = 3.5
    playerDrag = 0.98
    #playerDrag = 1
    ballDrag = 0.995
    stadiumWidth =  1390
    stadiumHeight = 666

def deletePhysicObjects():
    physicsEngine.ballList.clear()
    physicsEngine.postList.clear()
    physicsEngine.pointList.clear()
    physicsEngine.wallList.clear()
    physicsEngine.lineList.clear()
    physicsEngine.visualLineList.clear()
    physicsEngine.goalList.clear()
    physicsEngine.arcList.clear()
    physicsEngine.kickoffCircleList.clear()
    physicsEngine.kickoffPointList.clear()
    physicsEngine.kickoffLineList.clear()
    physicsEngine.kickoffArcList.clear()

def stadiums():
    res = []
    for file in os.listdir("./stadiums"):
        if file.endswith(".py"):
            res.append( file[:-3])
    return res
    
def loadStadium( name):
    deletePhysicObjects()
    setDefaultSettings()
    render.background_image = pygame.image.load("./assets/bg.png").convert_alpha()
    
    global stadium
    stadium = name
    
    path = "./stadiums/"
    path += name
    path += ".py"

    exec(open( path).read())

    global defaultZoom
    zx = WIDTH / stadiumWidth
    zy = HEIGHT / stadiumHeight

    if zx > zy: defaultZoom = zy
    else: defaultZoom = zx
    
