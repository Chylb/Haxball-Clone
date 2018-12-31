lineWidth = 5

Ball( 0, 0, 18, WHITE)

Line( -480, 195, 480, 195, LINE_GREEN, lineWidth, True)
Line( -480, -195, 480, -195, LINE_GREEN, lineWidth, True)

Line( -480, -195, -480, -195, LINE_GREEN, lineWidth, True)
Line( -480, 106, -480, 195, LINE_GREEN, lineWidth, True)

Line( 480, -195, 480, -106, LINE_GREEN, lineWidth, True)
Line( 480, 106, 480, 195, LINE_GREEN, lineWidth, True)

VisualLine( 0, -195, 0, 195, LINE_GREEN, lineWidth, True)
VisualLine( -480, -195, -480, 195, LINE_GREEN, lineWidth, True)
VisualLine( 480, -195, 480, 195, LINE_GREEN, lineWidth, True)

KickoffArc( 0, 0, 105, math.pi/2, math.pi * 3 / 2, "RED", LINE_GREEN, lineWidth, True)
KickoffArc( 0, 0, 105, math.pi * 3 / 2, math.pi/2, "BLUE", LINE_GREEN, lineWidth, True)

KickoffLine( 0, -195, 0, -105, "NONE", LINE_GREEN, lineWidth, True)
KickoffLine( 0, 105, 0, 195, "NONE", LINE_GREEN, lineWidth, True)
KickoffLine( 0, -332, 0, -195, "NONE", WHITE, 0, False)
KickoffLine( 0, 195, 0, 332, "NONE", WHITE, 0, False)

Arc( -480, -83 + 52, 52, math.pi / 2, math.pi, BLACK, 7, True)
Arc( -480, 83 - 52, 52, math.pi, 3 * math.pi / 2, BLACK, 7, True)
Line( -480 - 49, -83 + 52, -480 - 49, 83 - 52, BLACK, 7, True)

Arc( 480, -83 + 52, 52, 0, math.pi / 2, BLACK, 7, True)
Arc( 480, 83 - 52, 52, 3 * math.pi / 2, 0, BLACK, 7, True)
Line( 480 + 49, -83 + 52, 480 + 49, 83 - 52, BLACK, 7, True)

Post( -480, -83, 15, POST_RED)
Post( -480, 83, 15, POST_RED)
Post( 480, -83, 15, POST_BLUE)
Post( 480, 83, 15, POST_BLUE)

Goal("RED", -498, -83, -498, 83)
Goal("BLUE", 498, -83, 498, 83)

Wall( 0, 1, 245) #up
Wall( 0, -1, 245) #down
Wall( 1, 0, 560) #left
Wall( -1, 0, 560) #right

gameHandler.stadiumWidth = 1120
gameHandler.stadiumHeight = 490

