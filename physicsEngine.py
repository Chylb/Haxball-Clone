import math
import pygame

import gameHandler

playerList = []
ballList = []
postList = []
pointList = []
wallList = []
lineList = []
visualLineList = []
goalList = []
arcList = []
kickoffCircleList = []
kickoffPointList = []
kickoffLineList = []
kickoffArcList = []

pygame.init()

def timeToCollision_circle_circle(obj1, obj2):
    #circle, circle
    #d = a*x^2 + b*x + c

    a = (obj1.vx - obj2.vx)**2 + (obj1.vy - obj2.vy)**2
    if a == 0 : return 2
    
    b = 2 * (obj1.vx - obj2.vx) * (obj1.x - obj2.x) + 2 * (obj1.vy - obj2.vy) * (obj1.y - obj2.y)
    c = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    d = (obj1.r + obj2.r)**2

    c -= d
    delta = b**2 - 4 * a * c

    if delta >= 0 :

        t1 = (-b - math.sqrt(delta)) / 2 / a

        if 0 <= t1 and t1 < 1:
            return t1
    
    return 2

def timeToCollision_sCircle_circle(obj1, obj2):
    #static circle, circle
    #d = a*x^2 + b*x + c

    a = obj2.vx**2 + obj2.vy**2
    if a == 0 : return 2
    
    b = 2 * -obj2.vx * (obj1.x - obj2.x) + 2 * -obj2.vy * (obj1.y - obj2.y)
    c = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    d = (obj1.r + obj2.r)**2

    c -= d
    delta = b**2 - 4 * a * c

    if delta >= 0 :

        t1 = (-b - math.sqrt(delta)) / 2 / a

        if 0 <= t1 and t1 < 1:
            return t1
    
    return 2

def timeToCollision_point_circle(obj1, obj2):
    #point, circle
    #d = a*x^2 + b*x + c

    a = obj2.vx**2 + obj2.vy**2
    if a == 0 : return 2
    
    b = 2 * -obj2.vx * (obj1.x - obj2.x) + 2 * -obj2.vy * (obj1.y - obj2.y)
    c = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    d = (obj2.r)**2

    c -= d
    delta = b**2 - 4 * a * c

    if delta >= 0 :

        t1 = (-b - math.sqrt(delta)) / 2 / a

        if 0 <= t1 and t1 < 1:
            return t1
    
    return 2

def timeToCollision_kickoffPoint_player(obj1, obj2):
    #kickoff point, player
    #d = a*x^2 + b*x + c

    if gameHandler.kickedOff : return 2
    if gameHandler.whoseBall == obj1.team and gameHandler.whoseBall == obj2.team: return 2

    a = obj2.vx**2 + obj2.vy**2
    if a == 0 : return 2
    
    b = 2 * -obj2.vx * (obj1.x - obj2.x) + 2 * -obj2.vy * (obj1.y - obj2.y)
    c = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    d = (obj2.r)**2

    c -= d
    delta = b**2 - 4 * a * c

    if delta >= 0 :

        t1 = (-b - math.sqrt(delta)) / 2 / a

        if 0 <= t1 and t1 < 1:
            return t1
    
    return 2

def timeToCollision_kickoffLine_player(obj1, obj2):
    #kickoff line, player
    #t1 abs is positive
    #t2 abs is negative

    if gameHandler.kickedOff : return 2
    if gameHandler.whoseBall == obj1.team and obj1.team == obj2.team: return 2

    if obj1.A * obj2.vx + obj1.B * obj2.vy == 0: return 2

    t1 = obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t1 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    t2 = -obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t2 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    if (0 <= t1 and t1 <= t2 and t1 < 1):
        x = obj2.x + obj2.vx * t1
        y = obj2.y + obj2.vy * t1

        distance = (x - obj1.xm)**2 + (y - obj1.ym)**2
        if distance <= (obj1.r )/1 + obj2.r**2: return t1
    if (0 <= t2 and t2 <= t1 and t2 < 1):
        x = obj2.x + obj2.vx * t2
        y = obj2.y + obj2.vy * t2

        distance = (x - obj1.xm)**2 + (y - obj1.ym)**2
        if distance <= (obj1.r )/1 + obj2.r**2: return t2
    return 2

def timeToCollision_kickoffArc_player(obj1, obj2):
    #kickoff arc, player
    #d = a*x^2 + b*x + c
    if gameHandler.kickedOff: return 2
    if gameHandler.whoseBall == obj1.team and obj1.team == obj2.team: return 2

    a = obj2.vx**2 + obj2.vy**2
    if a == 0 : return 2
    
    b = 2 * -obj2.vx * (obj1.x - obj2.x) + 2 * -obj2.vy * (obj1.y - obj2.y)
    c1 = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    c2 = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    d1 = (obj1.r + obj2.r)**2
    d2 = (obj1.r - obj2.r)**2

    c1 -= d1
    c2 -= d2
    
    delta1 = b**2 - 4 * a * c1
    delta2 = b**2 - 4 * a * c2

    right = pygame.math.Vector2(1,0)

    if delta1 >= 0 :
        t1 = (-b - math.sqrt(delta1)) / 2 / a
        x1 = obj2.x + obj2.vx * t1
        y1 = obj2.y + obj2.vy * t1
        pos1 = pygame.math.Vector2(x1 - obj1.x, y1 - obj1.y)

        angle1 = pos1.angle_to(right)
        if angle1 < 0: angle1 += 360 #angle_to can return negative angle
        angle1 *= math.pi
        angle1 /= 180
        if obj1.a > obj1.a0:
            if obj1.a0 > angle1 or angle1 > obj1.a: t1 = 2
        else:
            if obj1.a < angle1 and angle1 < obj1.a0: t1 = 2
    else: t1 = 2

    if delta2 >= 0 :
        t2 = (-b + math.sqrt(delta2)) / 2 / a
        x2 = obj2.x + obj2.vx * t2
        y2 = obj2.y + obj2.vy * t2
        pos2 = pygame.math.Vector2(x2 - obj1.x, y2 - obj1.y)

        angle2 = pos2.angle_to(right)
        if angle2 < 0: angle2 += 360
        angle2 *= math.pi
        angle2 /= 180
 
        if obj1.a > obj1.a0:
            if obj1.a0 > angle2 or angle2 > obj1.a: t2 = 2
        else:
            if obj1.a < angle2 and angle2 < obj1.a0: t2 = 2
    else: t2 = 2

    if t1 < 0: t1 = 2

    if t2 < t1 and t2 >= 0: t1 = t2

    if t1 >= 0 and t1 < 1000: return t1

    return 2



def timeToCollision_ball_player(obj1, obj2):
    #ball, player
    #d = a*x^2 + b*x + c

    if obj2.kicking: d = (obj1.r + 1.12 * obj2.r)**2
    else: d = (obj1.r + obj2.r)**2

    c = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2

    if obj2.kicking:
        if c < d: return 0  #yes, you can kick the ball without really touching it

    a = (obj1.vx - obj2.vx)**2 + (obj1.vy - obj2.vy)**2
    if a == 0 : return 2
    
    b = 2 * (obj1.vx - obj2.vx) * (obj1.x - obj2.x) + 2 * (obj1.vy - obj2.vy) * (obj1.y - obj2.y)

    c -= d
    delta = b**2 - 4 * a * c

    if delta >= 0 :

        t1 = (-b - math.sqrt(delta)) / 2 / a

        if 0 <= t1 and t1 < 1:
            return t1
    
    return 2

def timeToCollision_wall_circle(obj1, obj2):
    #wall, circle
    #t1 abs is positive
    #t2 abs is negative

    d = obj1.A * obj2.x + obj1.B * obj2.y + obj1.C
    wall = pygame.math.Vector2(-obj1.B, obj1.A)
    v = pygame.math.Vector2(obj2.vx, obj2.vy)

    if v.length() == 0: return 2

    xo = obj1.B * (obj1.B * obj2.x - obj1.A * obj2.y) - obj1.A * obj1.C
    xo /= ( obj1.A**2 + obj1.B**2)
    yo = obj1.A * (-obj1.B * obj2.x + obj1.A * obj2.y) - obj1.B * obj1.C
    yo /= ( obj1.A**2 + obj1.B**2)

    normal = pygame.math.Vector2(obj2.x - xo, obj2.y - yo)

    if abs( normal.angle_to(v)) <= 90: return 2

    if (obj1.A * obj2.vx + obj1.B * obj2.vy) == 0 : return 2

    t1 = obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t1 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    t2 = -obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t2 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    if (0 <= t1 and t1 <= t2 and t1 < 1): return t1
    elif (0 <= t2 and t2 <= t1 and t2 < 1): return t2
    return 2

def timeToCollision_line_circle(obj1, obj2):
    #line, circle
    #t1 abs is positive
    #t2 abs is negative

    if obj1.A * obj2.vx + obj1.B * obj2.vy == 0: return 2

    t1 = obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t1 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    t2 = -obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t2 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    if (0 <= t1 and t1 <= t2 and t1 < 1):
        x = obj2.x + obj2.vx * t1
        y = obj2.y + obj2.vy * t1

        distance = (x - obj1.xm)**2 + (y - obj1.ym)**2
        if distance <= (obj1.r )/1 + obj2.r**2: return t1
    if (0 <= t2 and t2 <= t1 and t2 < 1):
        x = obj2.x + obj2.vx * t2
        y = obj2.y + obj2.vy * t2

        distance = (x - obj1.xm)**2 + (y - obj1.ym)**2
        if distance <= (obj1.r )/1 + obj2.r**2: return t2
    return 2

def timeToCollision_goal_ball(obj1, obj2):
    #goal, ball
    #t1 abs is positive
    #t2 abs is negative
    if gameHandler.isCelebrating: return 2
    if obj1.A * obj2.vx + obj1.B * obj2.vy == 0: return 2

    t1 = obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t1 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    t2 = -obj2.r * math.sqrt(obj1.A**2 + obj1.B**2) - obj1.A * obj2.x - obj1.B * obj2.y - obj1.C
    t2 /= (obj1.A * obj2.vx + obj1.B * obj2.vy)

    if (0 <= t1 and t1 <= t2 and t1 < 1):
        x = obj2.x + obj2.vx * t1
        y = obj2.y + obj2.vy * t1

        distance = (x - obj1.xm)**2 + (y - obj1.ym)**2
        if distance <= (obj1.r )/1 + obj2.r**2: return t1
    if (0 <= t2 and t2 <= t1 and t2 < 1):
        x = obj2.x + obj2.vx * t2
        y = obj2.y + obj2.vy * t2

        distance = (x - obj1.xm)**2 + (y - obj1.ym)**2
        if distance <= (obj1.r )/1 + obj2.r**2: return t2
    return 2

def timeToCollision_arc_circle(obj1, obj2):
    #arc, circle
    a = obj2.vx**2 + obj2.vy**2
    if a == 0 : return 2
    
    b = 2 * -obj2.vx * (obj1.x - obj2.x) + 2 * -obj2.vy * (obj1.y - obj2.y)
    c1 = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    c2 = (obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2
    d1 = (obj1.r + obj2.r)**2
    d2 = (obj1.r - obj2.r)**2

    c1 -= d1
    c2 -= d2
    
    delta1 = b**2 - 4 * a * c1
    delta2 = b**2 - 4 * a * c2

    right = pygame.math.Vector2(1,0)

    if delta1 >= 0 :
        t1 = (-b - math.sqrt(delta1)) / 2 / a
        x1 = obj2.x + obj2.vx * t1
        y1 = obj2.y + obj2.vy * t1
        pos1 = pygame.math.Vector2(x1 - obj1.x, y1 - obj1.y)

        angle1 = pos1.angle_to(right)
        if angle1 < 0: angle1 += 360 #angle_to can return negative angle
        angle1 *= math.pi
        angle1 /= 180
        if obj1.a > obj1.a0:
            if obj1.a0 > angle1 or angle1 > obj1.a: t1 = 2
        else:
            if obj1.a < angle1 and angle1 < obj1.a0: t1 = 2
    else: t1 = 2

    if delta2 >= 0 :
        t2 = (-b + math.sqrt(delta2)) / 2 / a
        x2 = obj2.x + obj2.vx * t2
        y2 = obj2.y + obj2.vy * t2
        pos2 = pygame.math.Vector2(x2 - obj1.x, y2 - obj1.y)

        angle2 = pos2.angle_to(right)
        if angle2 < 0: angle2 += 360
        angle2 *= math.pi
        angle2 /= 180

        if obj1.a > obj1.a0:
            if obj1.a0 > angle2 or angle2 > obj1.a: t2 = 2
        else:
            if obj1.a < angle2 and angle2 < obj1.a0: t2 = 2
    else: t2 = 2

    if t1 < 0: t1 = 2

    if t2 < t1 and t2 >= 0: t1 = t2

    if t1 >= 0 and t1 < 1000: return t1

    return 2

def collide_circle_circle(obj1, obj2):
    #circle, circle

    os = pygame.math.Vector2(obj2.x - obj1.x, obj2.y - obj1.y)
    os.normalize_ip()

    v1 = pygame.math.Vector2(obj1.vx, obj1.vy)
    v2 = pygame.math.Vector2(obj2.vx, obj2.vy)

    velRelativ = v1 - v2
    velRelativ *= 0.8

    v2 += os * math.cos((os.angle_to(velRelativ) * math.pi / 180)) * velRelativ.length()
    v1 -= os * math.cos((os.angle_to(velRelativ) * math.pi / 180)) * velRelativ.length()

    obj1.vx = v1.x
    obj1.vy = v1.y
    obj2.vx = v2.x
    obj2.vy = v2.y

def collide_ball_player(obj1, obj2):
    #ball, player
    gameHandler.kickedOff = True
    if obj2.team == "RED":
        gameHandler.lastRedTouch = 0
        gameHandler.lastRedTouchPlayer = playerList.index( obj2)
    elif obj2.team == "BLUE":
        gameHandler.lastBlueTouch = 0
        gameHandler.lastBlueTouchPlayer = playerList.index( obj2)
    
    os = pygame.math.Vector2(obj2.x - obj1.x, obj2.y - obj1.y)
    os.normalize_ip()

    v1 = pygame.math.Vector2(obj1.vx, obj1.vy)
    v2 = pygame.math.Vector2(obj2.vx, obj2.vy)
    
    if obj2.kicking:
        v1 = os * v2
        v1 *= os
        v1 *= 1.2

        v1 -= os * gameHandler.kickForce

        obj1.vx = v1.x
        obj1.vy = v1.y

        obj2.kicking = False
        obj2.hasKicked = True

        gameHandler.kickSound.play()

    else:
        velRelativ = v1 - v2
        velRelativ *= obj1.mass * obj2.mass
        velRelativ *= 1.2
        
        velRelativ /= (obj1.mass + obj2.mass)
        v2 += os * math.cos((os.angle_to(velRelativ) * math.pi / 180)) * velRelativ.length() / obj2.mass
        v1 -= os * math.cos((os.angle_to(velRelativ) * math.pi / 180)) * velRelativ.length() / obj1.mass

        obj1.vx = v1.x
        obj1.vy = v1.y
        obj2.vx = v2.x
        obj2.vy = v2.y

def collide_post_ball(obj1, obj2):
    #post, ball
    os = pygame.math.Vector2(obj2.x - obj1.x, obj2.y - obj1.y)
    os.normalize_ip()
    v = pygame.math.Vector2(obj2.vx, obj2.vy)
    
    dotproduct = os * v 
    dotproduct *= os
    dotproduct *= 1.4
    v -= dotproduct
    obj2.vx = v.x
    obj2.vy = v.y

def collide_sCircle_circle(obj1, obj2):
    #static circle, circle
    os = pygame.math.Vector2(obj2.x - obj1.x, obj2.y - obj1.y)
    os.normalize_ip()
    v = pygame.math.Vector2(obj2.vx, obj2.vy)
    
    dotproduct = os * v 
    dotproduct *= os

    #inner collision elasticity coefficient tweaking
    dotproduct *= 1.05 + (math.sin((os.angle_to(v) * math.pi / 180)))**2
    v -= dotproduct
    obj2.vx = v.x
    obj2.vy = v.y

def collide_point_circle(obj1, obj2):
    #point, circle
    os = pygame.math.Vector2(obj2.x - obj1.x, obj2.y - obj1.y)
    os.normalize_ip()
    v = pygame.math.Vector2(obj2.vx, obj2.vy)
    
    dotproduct = os * v 
    dotproduct *= os
    dotproduct *= 1.1
    v -= dotproduct
    obj2.vx = v.x
    obj2.vy = v.y

def collide_wall_circle(obj1, obj2):
    #wall, circle                       
    normal = pygame.math.Vector2(obj1.A, obj1.B)
    normal.normalize_ip()
    v = pygame.math.Vector2(obj2.vx, obj2.vy)
    dotproduct = normal * v 
    dotproduct *= normal
    dotproduct *= 1.2
    v -= dotproduct
    obj2.vx = v.x
    obj2.vy = v.y

def collide_line_circle(obj1, obj2):
    #line, circle

    normal = pygame.math.Vector2(obj1.A, obj1.B)
    normal.normalize_ip()
    v = pygame.math.Vector2(obj2.vx, obj2.vy) 
    
    dotproduct = normal * v 
    dotproduct *= normal
    dotproduct *= 1.5
    v -= dotproduct
    obj2.vx = v.x
    obj2.vy = v.y

def collide_goal_ball(obj1, obj2):
    #goal, ball
    
    gameHandler.goalSound.play()
  
    if obj1.team == "RED": gameHandler.score( "BLUE")
    else: gameHandler.score( "RED")

def update(previousKeys, currentKeys):

    for player in playerList:
        player.steer( previousKeys, currentKeys)

    time = 1

    while time > 0 :
        collisionMinTime = 2
        collisionType = ""
        collidedObj1 = None
        collidedObj2 = None

        for i in range(len(playerList) - 1):
            for j in range(i + 1, len(playerList)):
                thisTime = timeToCollision_circle_circle( playerList[i], playerList[j])
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "player_player"
                    collidedObj1 = playerList[i]
                    collidedObj2 = playerList[j]

        for ball in ballList:
            for player in playerList:
                thisTime = timeToCollision_ball_player( ball, player)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "ball_player"
                    collidedObj1 = ball
                    collidedObj2 = player

        for wall in wallList:
            for player in playerList:
                thisTime = timeToCollision_wall_circle( wall, player)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "wall_player"
                    collidedObj1 = wall
                    collidedObj2 = player
                    
        for post in postList:
            for ball in ballList:
                thisTime = timeToCollision_sCircle_circle( post, ball)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "post_ball"
                    collidedObj1 = post
                    collidedObj2 = ball

        for point in pointList:
            for ball in ballList:
                thisTime = timeToCollision_point_circle( point, ball)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "point_ball"
                    collidedObj1 = point
                    collidedObj2 = ball

        for post in postList:
            for player in playerList:
                thisTime = timeToCollision_sCircle_circle( post, player)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "post_player"
                    collidedObj1 = post
                    collidedObj2 = player

        for line in lineList:
            for ball in ballList:
                thisTime = timeToCollision_line_circle( line, ball)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "line_ball"
                    collidedObj1 = line
                    collidedObj2 = ball

        for goal in goalList:
            for ball in ballList:
                thisTime = timeToCollision_goal_ball( goal, ball)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "goal_ball"
                    collidedObj1 = goal
                    collidedObj2 = ball
    
        for arc in arcList:
            for ball in ballList:
                thisTime = timeToCollision_arc_circle( arc, ball)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "arc_ball"
                    collidedObj1 = arc
                    collidedObj2 = ball

        for kickoffPoint in kickoffPointList:
            for player in playerList:
                thisTime = timeToCollision_kickoffPoint_player( kickoffPoint, player)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "kickoffPoint_player"
                    collidedObj1 = kickoffPoint
                    collidedObj2 = player

        for kickoffArc in kickoffArcList:
            for player in playerList:
                thisTime = timeToCollision_kickoffArc_player( kickoffArc, player)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "kickoffArc_player"
                    collidedObj1 = kickoffArc
                    collidedObj2 = player

        for kickoffLine in kickoffLineList:
            for player in playerList:
                thisTime = timeToCollision_kickoffLine_player( kickoffLine, player)
                if thisTime < collisionMinTime:
                    collisionMinTime = thisTime
                    collisionType = "kickoffLine_player"
                    collidedObj1 = kickoffLine
                    collidedObj2 = player


        if collisionMinTime < time : 
            moveObjects( collisionMinTime)
            time -= collisionMinTime
                             
            if collisionType == "player_player":
                collide_circle_circle( collidedObj1, collidedObj2)
            elif collisionType == "ball_player":
                collide_ball_player( collidedObj1, collidedObj2)
            elif collisionType == "wall_player":
                collide_wall_circle( collidedObj1, collidedObj2)
            elif collisionType == "post_ball":
                collide_sCircle_circle( collidedObj1, collidedObj2)
            elif collisionType == "post_player":
                collide_sCircle_circle( collidedObj1, collidedObj2)
            elif collisionType == "line_ball":
                collide_line_circle( collidedObj1, collidedObj2)
            elif collisionType == "goal_ball":
                collide_goal_ball( collidedObj1, collidedObj2)
            elif collisionType == "point_ball":
                collide_point_circle( collidedObj1, collidedObj2)
            elif collisionType == "arc_ball":
                collide_sCircle_circle( collidedObj1, collidedObj2)
            elif collisionType == "kickoffPoint_player":
                collide_point_circle( collidedObj1, collidedObj2)
            elif collisionType == "kickoffArc_player":
                collide_sCircle_circle( collidedObj1, collidedObj2)
            elif collisionType == "kickoffLine_player":
                collide_line_circle( collidedObj1, collidedObj2)
        else :
            moveObjects( time)
            time = 0
            
    for player in playerList:
        player.vx *= gameHandler.playerDrag
        player.vy *= gameHandler.playerDrag

    for ball in ballList:
        ball.vx *= gameHandler.ballDrag
        ball.vy *= gameHandler.ballDrag

    physicObjects = {}
    physicObjects['players'] = playerList
    physicObjects['balls'] = ballList
    physicObjects['posts'] = postList
    physicObjects['points'] = pointList
    physicObjects['walls'] = wallList
    physicObjects['lines'] = lineList
    physicObjects['visualLines'] = visualLineList
    physicObjects['goals'] = goalList
    physicObjects['arcs'] = arcList
    physicObjects['kickoffPoints'] = kickoffPointList
    physicObjects['kickoffLines'] = kickoffLineList
    physicObjects['kickoffArcs'] = kickoffArcList
    return physicObjects

def moveObjects(time):

    for player in playerList:
        player.x += player.vx * time
        player.y += player.vy * time

    for ball in ballList:
        ball.x += ball.vx * time
        ball.y += ball.vy * time


    
    
    





