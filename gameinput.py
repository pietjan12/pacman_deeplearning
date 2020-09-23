# gameinput Module
import pacman

JS_XAXIS=0 # axis 0 for left/right (default for most joysticks)
JS_YAXIS=1 # axis 1 for up/down (default for most joysticks)
JS_STARTBUTTON=0 # button number to start the game.

pacman.pygame.joystick.init()
joystick_count = pacman.pygame.joystick.get_count()

if(joystick_count > 0):
    joyin = pacman.pygame.joystick.Joystick(0)
    joyin.init()
else:
    joyin = None

def CheckIfCloseButton(events):
    for event in events:
        if event.type == pacman.pygame.QUIT:
            pacman.pygame.sys.exit(0)

def CheckInputs(game, player):
    if game.mode == 1:
        if pacman.pygame.key.get_pressed()[pacman.pygame.K_RIGHT] or (joyin != None and joyin.get_axis(JS_XAXIS) > 0):
            if not pacman.thisLevel.CheckIfHitWall(player.x + player.speed, player.y, player.nearestRow, player.nearestCol):
                player.velX = player.speed
                player.velY = 0

        elif pacman.pygame.key.get_pressed()[pacman.pygame.K_LEFT] or (joyin != None and joyin.get_axis(JS_XAXIS) < 0):
            if not pacman.thisLevel.CheckIfHitWall(player.x - player.speed, player.y, player.nearestRow, player.nearestCol):
                player.velX = -player.speed
                player.velY = 0

        elif pacman.pygame.key.get_pressed()[pacman.pygame.K_DOWN] or (joyin != None and joyin.get_axis(JS_YAXIS) > 0):
            if not pacman.thisLevel.CheckIfHitWall(player.x, player.y + player.speed, player.nearestRow, player.nearestCol):
                player.velX = 0
                player.velY = player.speed

        elif pacman.pygame.key.get_pressed()[pacman.pygame.K_UP] or (joyin != None and joyin.get_axis(JS_YAXIS) < 0):
            if not pacman.thisLevel.CheckIfHitWall(player.x, player.y - player.speed, player.nearestRow, player.nearestCol):
                player.velX = 0
                player.velY = -player.speed

    if pacman.pygame.key.get_pressed()[pacman.pygame.K_ESCAPE]:
        pacman.pygame.sys.exit(0)

    elif game.mode == 3:
        if pacman.pygame.key.get_pressed()[pacman.pygame.K_RETURN] or (joyin != None and joyin.get_button(JS_STARTBUTTON)):
            game.StartNewGame()