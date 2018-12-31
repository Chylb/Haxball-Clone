import time
import pygame

import physicsEngine
import gameHandler

from render import WIDTH
from render import HEIGHT

import functools
from classes import *
from constants import *
 
pygame.init()

regularFont = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf",20)
semiboldFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UNirkOUuhp.ttf",20)
boldFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",20)

lightFont = pygame.font.Font("./assets/fonts/mem8YaGs126MiZpBA-UFVZ0b.ttf",18)
buttonFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",18)
bigFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",22)
gigaFont = pygame.font.Font("./assets/fonts/mem5YaGs126MiZpBA-UN7rgOUuhp.ttf",100)

buttonList = []
playerBarList = []
dropdownList = []

selectedPlayerBar = None

isTyping = False
textBox = None
textBoxUnicode = True
typedObject = None
typedObjectAttribute = None
typedObjectUpdate = None
typeOnce = False
typeRawInput = False
typeResult = None
typedInO = None
typedInTB = None

isDragging = False
dragPointX = 0
dragPointY = 0

isDropdownListActive = False
dropdownListBox = None
dropdownSelectedItem = None
dropdownListX = 0
dropdownListY = 0
dropdownListW = 0
dropdownListH = 0
overDropdownList = False

redTeamBox = None
spectatorTeamBox = None
blueTeamBox = None

gameSection = 0

#these 2 functions comes from a reply by @unutbu on https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects 
def rsetattr(obj, attr, val): 
    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)

def rgetattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))

#BUTTON FUNCTIONS

def goToSection( button, argument):
    global gameSection
    gameSection = argument

def goToExit( button, argument):
    gameHandler.saveRecord()
    gameHandler.run = False

def addPlayer( button, argument):
    gameHandler.joinedSound.play()
    Player("Player " + str(gameHandler.redPlayersCount+gameHandler.bluePlayersCount+gameHandler.spectatorsCount + 1), "NONE", NO_KEYS,)

def doNothing( button, argument):
    pass

def changeNick( button, argument):
    global isTyping
    global textBox
    global textBoxUnicode
    global typedObject
    global typedObjectAttribute
    global typedObjectUpdate
    global typeResult 
    global typeOnce
    global typeRawInput
    global selectedPlayerBar
    
    isTyping = True
    textBox = button
    textBoxUnicode = True
    typedObject = selectedPlayerBar
    typedObjectAttribute = "player.nick"
    typedObjectUpdate = selectedPlayerBar.updateName
    typeResult = selectedPlayerBar.player.nick
    typeOnce = False
    typeRawInput = False
    
def goToPlayerControls( button, argument):
    global gameSection
    global selectedPlayerBar
    gameSection = 5

    global upKeyBox
    global downKeyBox 
    global leftKeyBox 
    global rightKeyBox 
    global kickKeyBox

    upKeyBox.string = pygame.key.name( selectedPlayerBar.player.keyUp)
    downKeyBox.string = pygame.key.name( selectedPlayerBar.player.keyDown)
    leftKeyBox.string = pygame.key.name( selectedPlayerBar.player.keyLeft)
    rightKeyBox.string = pygame.key.name( selectedPlayerBar.player.keyRight)
    kickKeyBox.string = pygame.key.name( selectedPlayerBar.player.keyKick)

    upKeyBox.update()
    downKeyBox.update()
    leftKeyBox.update()
    rightKeyBox.update()
    kickKeyBox.update()

def changePlayerControls( button, argument):
    global isTyping
    global textBox
    global textBoxUnicode
    global typedObject
    global typedObjectAttribute
    global typedObjectUpdate
    global typeResult 
    global typeOnce
    global typeRawInput
    global selectedPlayerBar
    
    isTyping = True
    textBox = button
    textBoxUnicode = False
    typedObject = selectedPlayerBar
    typedObjectUpdate = selectedPlayerBar.updateName #does it work?
     
    typeOnce = True
    typeRawInput = True
    
    global upKeyBox
    global downKeyBox 
    global leftKeyBox 
    global rightKeyBox 
    global kickKeyBox
    
    if argument == 0:
        textBox = upKeyBox
        typedObjectAttribute = "player.keyUp"
    elif argument == 1:
        textBox = downKeyBox
        typedObjectAttribute = "player.keyDown"
    elif argument == 2:
        textBox = leftKeyBox
        typedObjectAttribute = "player.keyLeft"
    elif argument == 3:
        textBox = rightKeyBox
        typedObjectAttribute = "player.keyRight"
    elif argument == 4:
        textBox = kickKeyBox
        typedObjectAttribute = "player.keyKick"

def deletePlayer( button, argument):
    gameHandler.leftSound.play()
    global selectedPlayerBar
    if selectedPlayerBar.player.team == "BLUE":
        gameHandler.bluePlayersCount -= 1
    elif selectedPlayerBar.player.team == "RED":  
        gameHandler.redPlayersCount -= 1
    else: 
        gameHandler.spectatorsCount -= 1
 
    for bar in playerBarList:
        if bar.player.team == selectedPlayerBar.player.team:
            if bar.pos > selectedPlayerBar.pos:
                bar.pos -= 1
                bar.updateCoordinates()
                bar.updateName()
    physicsEngine.playerList.remove( selectedPlayerBar.player)
    playerBarList.remove( selectedPlayerBar)

    goToSection( button, 1)

def startGame( button, argument):
    global gameSection
    
    if not gameHandler.started:
        gameSection = 2
        
        gameHandler.startNewMatch()
        button.color = RED_BUTTON
        button.colorOver = RED_OVER
        button.colorPressed = RED_PRESSED
        button.string = "Stop game"
        button.update()
    else:
        gameHandler.started = False
        
        button.color = GREEN_BUTTON
        button.colorOver = GREEN_OVER
        button.colorPressed = GREEN_PRESSED
        button.string = "Start game"
        button.update()

def switchReplay( button, argument):
    if gameHandler.replaysTurnedOn:
        button.string = "Replays OFF"
        gameHandler.replaysTurnedOn = False
    else:
        button.string = "Replays ON"
        gameHandler.replaysTurnedOn = True
    button.update()
    
def dropdownTimeLimit( button, argument):
    if not gameHandler.started:
        global dropdownList
        global isDropdownListActive
        global dropdownListBox
        global dropdownSelectedItem

        button.string = str(gameHandler.timeLimit)
        button.update()

        dropdownList.clear()
        isDropdownListActive = True
        dropdownListBox = button
        
        for i in range (argument):
            DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, str(i), button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setTimeLimit, i)
        dropdownSelectedItem = dropdownList[ gameHandler.timeLimit]
    
def dropdownScoreLimit( button, argument):
    if not gameHandler.started:
        global dropdownList
        global isDropdownListActive
        global dropdownListBox
        global dropdownSelectedItem

        button.string = str(gameHandler.scoreLimit)
        button.update()

        dropdownList.clear()
        isDropdownListActive = True
        dropdownListBox = button
        
        for i in range (argument):
            DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, str(i), button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setScoreLimit, i) 
        dropdownSelectedItem = dropdownList[ gameHandler.scoreLimit]

def dropdownStadiums( button, argument):
    if not gameHandler.started:
        global dropdownList
        global isDropdownListActive
        global dropdownListBox
        global dropdownSelectedItem

        button.string = str(gameHandler.stadium)
        button.update()

        dropdownList.clear()
        isDropdownListActive = True
        dropdownListBox = button

        for i, stadium in enumerate(gameHandler.stadiums()):
            if stadium == gameHandler.stadium:
                dropdownSelectedItem = DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, stadium, button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setStadium, stadium)
            else:
                DropdownItem( button.x, button.y + (i+1)*button.h, button.w, button.h, stadium, button.font, BOX_DARKGRAY, DROPDOWN_BLUE, setStadium, stadium)
    
#DROPDOWN LIST FUNCTIONS

def setTimeLimit( argument):
    gameHandler.timeLimit = argument

def setScoreLimit( argument):
    gameHandler.scoreLimit = argument

def setStadium( argument):
    gameHandler.stadium = argument
    gameHandler.loadStadium( argument)  

############################################################################################################################################################################################################################################
#MENU FUNCTIONS 

def init():
    
    #MAIN MENU
    Button( 0, WIDTH/2 - 150, HEIGHT/2 - 200,300,400, "", False, buttonFont, WHITE, (26,33,37), (26,33,37), (26,33,37), doNothing, None)
    Button( 0, WIDTH/2 + 50, HEIGHT/2 - 235,0,0, "CLONE", False, bigFont, WHITE, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)   
    Button( 0, WIDTH/2 - 60, HEIGHT/2 - 150,120,60, "Play", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), goToSection, 1)
    Button( 0, WIDTH/2 - 60, HEIGHT/2 - 50,120,60, "Settings", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), goToSection, 3)
    Button( 0, WIDTH/2 - 60, HEIGHT/2 + 50,120,60, "Exit", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), goToExit, None)

    #LOBBY
    global redTeamBox
    global spectatorTeamBox
    global blueTeamBox
    global startButton
    
    Button( 1, WIDTH/2 - 450, HEIGHT/2 - 275,900,550, "", False, buttonFont, WHITE, (26,33,37), (26,33,37), (26,33,37), doNothing, None)

    Button( 1, WIDTH/2 - 230 - 60, HEIGHT/2 - 210,120,25, "Red", False, buttonFont, LABEL_RED, GRAY_BUTTON, GRAY_BUTTON, GRAY_BUTTON, doNothing, None)
    Button( 1, WIDTH/2 - 60, HEIGHT/2 - 210,120,25, "Spectators", False, buttonFont, WHITE, GRAY_BUTTON, GRAY_BUTTON, GRAY_BUTTON, doNothing, None)
    Button( 1, WIDTH/2 + 170, HEIGHT/2 - 210,120,25, "Blue", False, buttonFont, LABEL_BLUE, GRAY_BUTTON, GRAY_BUTTON, GRAY_BUTTON, doNothing, None)
    redTeamBox = Button( 1, WIDTH/2 - 340, HEIGHT/2 - 180,220,290, "", False, buttonFont, WHITE, (17,22,25), (17,22,25), (17,22,25), doNothing, None)
    spectatorTeamBox = Button( 1, WIDTH/2 - 110, HEIGHT/2 - 180,220,290, "", False, buttonFont, WHITE, (17,22,25), (17,22,25), (17,22,25), doNothing, None)
    blueTeamBox = Button( 1, WIDTH/2 + 120, HEIGHT/2 - 180,220,290, "", False, buttonFont, WHITE, (17,22,25), (17,22,25), (17,22,25), doNothing, None)

    Button( 1, WIDTH/2 - 445, HEIGHT/2 - 140,100,25, "Add Player", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_OVER, BLUE_PRESSED, addPlayer, None)
    Button( 1, WIDTH/2 + 340, HEIGHT/2 - 265,100,25, "Leave", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_OVER, BLUE_PRESSED, goToSection, 0)

    Button( 1, WIDTH/2 - 190, HEIGHT/2 + 125,150,20, "Time limit", True, lightFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    Button( 1, WIDTH/2 - 190, HEIGHT/2 + 150,150,20, "Score limit", True, lightFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    Button( 1, WIDTH/2 - 190, HEIGHT/2 + 175,150,20, "Stadium", True, lightFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    startButton = Button( 1, WIDTH/2 - 65, HEIGHT/2 + 220,130,25, "Start game", False, buttonFont, WHITE, (58,153,51), (70,184,61), (46,122,41), startGame, None)
    
    timeLimitBox = Button( 1, WIDTH/2 - 75, HEIGHT/2 + 125,150,20, str(gameHandler.timeLimit), True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, dropdownTimeLimit, 6)
    scoreLimitBox = Button( 1, WIDTH/2 - 75, HEIGHT/2 + 150,150,20, str(gameHandler.scoreLimit), True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, dropdownScoreLimit, 6)
    stadiumBox = Button( 1, WIDTH/2 - 75, HEIGHT/2 + 175,150,20, str(gameHandler.stadium), True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, dropdownStadiums, None)

    #GAME
    global scoreBar
    global timeBar
    global overtimeSprite
    global upperShadow
    global lowerShadow
    global upperInfo
    global lowerInfo
    global pauseBar
    
    Button( 2, WIDTH/2 - 220,0,440,40, "", False, buttonFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    scoreBar = Button( 2, WIDTH/2 - 180,0,50,40, "Score", False, bigFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    timeBar = Button( 2, WIDTH/2 + 160,0,50,40, "Time", False, bigFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    overtimeSprite = Button( 2, WIDTH/2 + 35,0,50,40, "", False, bigFont, WHITE, MENU_GRAY, MENU_GRAY, MENU_GRAY, doNothing, None)
    upperShadow = Button( 2, WIDTH/2 + 5, HEIGHT/2 - 50 + 5,0,0, "", False, gigaFont, BLACK, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    lowerShadow = Button( 2, WIDTH/2 + 5, HEIGHT/2 + 50 + 5,0,0, "", False, gigaFont, BLACK, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    upperInfo = Button( 2, WIDTH/2, HEIGHT/2 - 50,0,0, "", False, gigaFont, WHITE, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    lowerInfo = Button( 2, WIDTH/2, HEIGHT/2 + 50,0,0, "", False, gigaFont, WHITE, BACKGROUND_GREEN, BACKGROUND_GREEN, BACKGROUND_GREEN, doNothing, None)
    pauseBar = Button( 2, WIDTH/2, HEIGHT/2 + 100,0,10, "", False, buttonFont, WHITE, WHITE, WHITE, WHITE, doNothing, None)

    Button( 2, WIDTH/2 - 215,10,25,25, "", False, buttonFont, WHITE, PLAYER_RED, PLAYER_RED, PLAYER_RED, doNothing, None)
    Button( 2, WIDTH/2 - 120,10,25,25, "", False, buttonFont, WHITE, PLAYER_BLUE, PLAYER_BLUE, PLAYER_BLUE, doNothing, None)

    #SETTINGS
    Button( 3, WIDTH/2 - 150, HEIGHT/2 - 200,300,400, "", False, buttonFont, WHITE, (26,33,37), (26,33,37), (26,33,37), doNothing, None)
    Button( 3, WIDTH/2 - 60, HEIGHT/2 - 150,120,60, "Replays ON", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), switchReplay, None)
    Button( 3, WIDTH/2 - 60, HEIGHT/2 - 50,120,60, "Close", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), goToSection, 0)

    #PLAYER SETTINGS
    global nickBox
    
    Button( 4, WIDTH/2 - 150, HEIGHT/2 - 275,300,550, "", False, buttonFont, WHITE, (26,33,37), (26,33,37), (26,33,37), doNothing, None)   
    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 250,50,60, "Nick:", False, buttonFont, WHITE, (36,73,103), (36,73,103), (36,73,103), doNothing, None)
    nickBox = Button( 4, WIDTH/2 - 60, HEIGHT/2 - 250,180,60, "", True, lightFont, WHITE, (17,22,25), (17,22,25), (17,22,25), changeNick, None)

    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 170,220,60, "Change controls", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), goToPlayerControls, None)
    #Button( 4, WIDTH/2 - 110, HEIGHT/2 - 90,220,60, "Change avatar", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), goToSection, 1)
    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 90,220,60, "Close", False, buttonFont, WHITE,(36,73,103), (47,94,133), (25,52,73), goToSection, 1)
    Button( 4, WIDTH/2 - 110, HEIGHT/2 - 10,220,60, "Delete player", False, buttonFont, WHITE, (36,73,103), (47,94,133), (25,52,73), deletePlayer, None)

    #CONTROLS
    global upKeyBox
    global downKeyBox 
    global leftKeyBox 
    global rightKeyBox 
    global kickKeyBox
    
    Button( 5, WIDTH/2 - 150, HEIGHT/2 - 275,300,550, "", False, buttonFont, WHITE, (26,33,37), (26,33,37), (26,33,37), doNothing, None)   
    Button( 5, WIDTH/2 - 110, HEIGHT/2 - 250,80,60, "Up", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_BUTTON, BLUE_BUTTON, doNothing, None)
    Button( 5, WIDTH/2 - 110, HEIGHT/2 - 170,80,60, "Down", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_BUTTON, BLUE_BUTTON, doNothing, None)
    Button( 5, WIDTH/2 - 110, HEIGHT/2 - 90,80,60, "Left", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_BUTTON, BLUE_BUTTON, doNothing, None)
    Button( 5, WIDTH/2 - 110, HEIGHT/2 - 10,80,60, "Right", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_BUTTON, BLUE_BUTTON, doNothing, None)
    Button( 5, WIDTH/2 - 110, HEIGHT/2 + 70,80,60, "Kick", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_BUTTON, BLUE_BUTTON, doNothing, None)
    Button( 5, WIDTH/2 - 110, HEIGHT/2 + 150,220,60, "Close", False, buttonFont, WHITE, BLUE_BUTTON, BLUE_OVER, BLUE_PRESSED, goToSection, 4)

    upKeyBox = Button( 5, WIDTH/2 - 30, HEIGHT/2 - 250,160,60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 0)
    downKeyBox = Button( 5, WIDTH/2 - 30, HEIGHT/2 - 170,160,60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 1)
    leftKeyBox = Button( 5, WIDTH/2 - 30, HEIGHT/2 - 90,160,60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 2)
    rightKeyBox = Button( 5, WIDTH/2 - 30, HEIGHT/2 - 10,160,60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 3)
    kickKeyBox = Button( 5, WIDTH/2 - 30, HEIGHT/2 + 70,160,60, "", True, lightFont, WHITE, BOX_DARKGRAY, BOX_DARKGRAY, BOX_DARKGRAY, changePlayerControls, 4)
    
def update(previousKeys, currentKeys, mouseWasPressed, mousePressed, events):
    global isDragging
    global dragPointX
    global dragPointY

    global isTyping
    global textBox
    global textBoxUnicode
    global typedObject
    global typedObjectAttribute
    global typedObjectUpdate
    global typeResult 
    global typeOnce
    global typeRawInput
    global selectedPlayerBar
    global typedInO
    global typedInTB

    global isDropdownListActive 
    global dropdownListBox 
    global dropdownSelectedItem 
    
    global redTeamBox
    global blueTeamBox
    global spectatorTeamBox

    mousePos = pygame.mouse.get_pos()

    #FROM GAME TO MENU
    if gameSection == 2 and currentKeys[pygame.K_ESCAPE] and not previousKeys[pygame.K_ESCAPE]:
        goToSection( None, 1)
        gameHandler.pauseMatch()
    elif gameSection == 1 and currentKeys[pygame.K_ESCAPE] and not previousKeys[pygame.K_ESCAPE] and gameHandler.started:
        goToSection( None, 2)
        gameHandler.resumeMatch()
        
    if gameSection == 2 and currentKeys[pygame.K_p] and not previousKeys[pygame.K_p] and not gameHandler.paused:
        gameHandler.pauseMatch()
    elif gameSection == 2 and currentKeys[pygame.K_p] and not previousKeys[pygame.K_p]:
        gameHandler.resumeMatch()

    #MENU LOGIC
    if isTyping:
        if currentKeys[pygame.K_ESCAPE] or currentKeys[pygame.K_RETURN] or mousePressed[0] and ( textBox.x > mousePos[0] or  mousePos[0] > textBox.x + textBox.w or textBox.y > mousePos[1] or mousePos[1] > textBox.y + textBox.h ):
            isTyping = False
            
            rsetattr( typedObject, typedObjectAttribute, typeResult)
            typedObjectUpdate()
            
        else:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if typeRawInput:
                        typedInO = event.key
                    else:
                        typedInO = event.unicode
                        
                    if textBoxUnicode:
                        typedInTB = event.unicode
                    else:
                        typedInTB = pygame.key.name(event.key)
                    
                    if typeOnce:
                        textBox.string = typedInTB
                        typeResult = typedInO
                        rsetattr( typedObject, typedObjectAttribute, typeResult)
                        typedObjectUpdate()
                        isTyping = False
                    else:
                        if event.key == 8: #backspace
                            textBox.string = textBox.string[0:-1]
                            typeResult = typeResult[0:-1]
                        else:
                            textBox.string += typedInTB
                            typeResult += typedInO
                    textBox.update()     
            
    for button in buttonList:
        button.isOver = False

        if button.section == gameSection and not isDropdownListActive :    
            if button.x <= mousePos[0] and  mousePos[0] <= button.x + button.w:
                if button.y <= mousePos[1] and  mousePos[1] <= button.y + button.h:
                    button.isOver = True

            if mouseWasPressed[0] and not mousePressed[0]:
                if button.isOver and button.isPressed:
                    button.f( button, button.argument)
                button.isPressed = False
                
            elif not mouseWasPressed[0] and mousePressed[0] and button.isOver:
                button.isPressed = True

    if isDropdownListActive and gameSection == 1:
        overDropdownList = False
            
        for item in dropdownList:
            if item.x <= mousePos[0] and  mousePos[0] <= item.x + item.w:
                if item.y <= mousePos[1] and  mousePos[1] <= item.y + item.h:
                    dropdownSelectedItem = item
                    overDropdownList = True

                    if mouseWasPressed[0] and not mousePressed[0]:
                        item.f( item.argument)
                        dropdownListBox.string = item.string
                        dropdownListBox.update()
                        isDropdownListActive = False
                        
        if mousePressed[0] and not overDropdownList:
            isDropdownListActive = False
    
    if isDragging:
        if not mousePressed[0]:
            isDragging = False

            if redTeamBox.isOver or blueTeamBox.isOver or spectatorTeamBox.isOver:
                if selectedPlayerBar.player.team == "RED":
                    gameHandler.redPlayersCount -= 1
                elif selectedPlayerBar.player.team == "NONE":
                    gameHandler.spectatorsCount -= 1
                else:
                    gameHandler.bluePlayersCount -= 1
                
                for bar in playerBarList:
                    if bar.player.team == selectedPlayerBar.player.team:
                        if bar.pos > selectedPlayerBar.pos:
                            bar.pos -= 1
                            bar.updateCoordinates()
                            bar.updateName()

                if redTeamBox.isOver:
                    gameHandler.redPlayersCount += 1
                    if selectedPlayerBar.player.team != "RED":
                        selectedPlayerBar.player.team = "RED"
                        gameHandler.putPlayerOnPitch( selectedPlayerBar.player)
                    selectedPlayerBar.pos = gameHandler.redPlayersCount
                elif spectatorTeamBox.isOver:
                    gameHandler.spectatorsCount += 1
                    if selectedPlayerBar.player.team != "NONE":
                        selectedPlayerBar.player.team = "NONE"
                        gameHandler.putPlayerOnPitch( selectedPlayerBar.player)
                    selectedPlayerBar.pos = gameHandler.spectatorsCount
                elif blueTeamBox.isOver:
                    gameHandler.bluePlayersCount += 1
                    if selectedPlayerBar.player.team != "BLUE":
                        selectedPlayerBar.player.team = "BLUE"
                        gameHandler.putPlayerOnPitch( selectedPlayerBar.player)
                    selectedPlayerBar.pos = gameHandler.bluePlayersCount

            selectedPlayerBar.updateCoordinates()
            selectedPlayerBar.updateName()
                            
        else:
            selectedPlayerBar.x = mousePos[0] - dragPointX
            selectedPlayerBar.y = mousePos[1] - dragPointY
            selectedPlayerBar.updateName()

    for bar in playerBarList:
        bar.isOver = False
        if bar.x <= mousePos[0] and  mousePos[0] <= bar.x + bar.w and not isDragging:
            if bar.y <= mousePos[1] and  mousePos[1] <= bar.y + bar.h:
                bar.isOver = True
        if bar == selectedPlayerBar and isDragging:
            bar.isOver = True

        if gameSection == 1 and bar.isOver and mousePressed[0] and not mouseWasPressed[0]:
            isDragging = True
            selectedPlayerBar = bar
            playerBarList[ playerBarList.index( bar) ], playerBarList[ len(playerBarList)-1]  = playerBarList[ len(playerBarList)-1], playerBarList[ playerBarList.index( bar) ]
            #swaping dragged player bar with the last in the list so it won't be overlapped
            dragPointX = mousePos[0] - bar.x
            dragPointY = mousePos[1] - bar.y

        if bar.isOver and mousePressed[2] and not mouseWasPressed[2]:
            bar.openOptions()
