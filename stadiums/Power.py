
lineWidth = 5

Ball( 0, 0, 18, (255, 255, 0))

Line( -611, 281, 611, 281, LINE_GREEN, lineWidth, True)
Line( -611, -281, 611, -281, LINE_GREEN, lineWidth, True)

Line( -611, -281, -611, -106, LINE_GREEN, lineWidth, True)
Line( -611, 106, -611, 281, LINE_GREEN, lineWidth, True)

Line( 611, -281, 611, -106, LINE_GREEN, lineWidth, True)
Line( 611, 106, 611, 281, LINE_GREEN, lineWidth, True)

VisualLine( 0, -281, 0, 281, LINE_GREEN, lineWidth, True)
VisualLine( -611, -281, -611, 281, LINE_GREEN, lineWidth, True)
VisualLine( 611, -281, 611, 281, LINE_GREEN, lineWidth, True)

KickoffArc( 0, 0, 123.5, math.pi/2, math.pi * 3 / 2, "RED", LINE_GREEN, lineWidth, True)
KickoffArc( 0, 0, 123.5, math.pi * 3 / 2, math.pi/2, "BLUE", LINE_GREEN, lineWidth, True)

KickoffLine( 0, -281, 0, -123.5, "NONE", LINE_GREEN, lineWidth, True)
KickoffLine( 0, 123.5, 0, 281, "NONE", LINE_GREEN, lineWidth, True)
KickoffLine( 0, -332, 0, -281, "NONE", WHITE, 0, False)
KickoffLine( 0, 281, 0, 332, "NONE", WHITE, 0, False)

Arc( -611, -106 + 52, 52, math.pi / 2, math.pi, BLACK, 7, True)
Arc( -611, 106 - 52, 52, math.pi, 3 * math.pi / 2, BLACK, 7, True)
Line( -611 - 49, -106 + 52, -611 - 49, 106 - 52, BLACK, 7, True)

Arc( 611, -106 + 52, 52, 0, math.pi / 2, BLACK, 7, True)
Arc( 611, 106 - 52, 52, 3 * math.pi / 2, 0, BLACK, 7, True)
Line( 611 + 49, -106 + 52, 611 + 49, 106 - 52, BLACK, 7, True)

Post( -611, -106, 15, POST_RED)
Post( -611, 106, 15, POST_RED)
Post( 611, -106, 15, POST_BLUE)
Post( 611, 106, 15, POST_BLUE)

Goal("RED", -629, -106, -629, 106)
Goal("BLUE", 629, -106, 629, 106)

Wall( 0, 1, 333) #up
Wall( 0, -1, 333) #down
Wall( 1, 0, 695) #left
Wall( -1, 0, 695) #right

gameHandler.kickForce = 7



