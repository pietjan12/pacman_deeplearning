import random, tile_ids, pacman, sounds

class level():

    def __init__(self):
        self.lvlWidth = 0
        self.lvlHeight = 0
        self.edgeLightColor = (255, 255, 0, 255)
        self.edgeShadowColor = (255, 150, 0, 255)
        self.fillColor = (0, 255, 255, 255)
        self.pelletColor = (255, 255, 255, 255)

        self.map = {}

        self.pellets = 0
        self.powerPelletBlinkTimer = 0

    def SetMapTile(self, row, col, newValue):
        self.map[(row * self.lvlWidth) + col] = newValue

    def GetMapTile(self, row, col):
        if row >= 0 and row < self.lvlHeight and col >= 0 and col < self.lvlWidth:
            return self.map[(row * self.lvlWidth) + col]
        else:
            return 0

    def IsWall(self, row, col):

        if row > pacman.thisLevel.lvlHeight - 1 or row < 0:
            return True

        if col > pacman.thisLevel.lvlWidth - 1 or col < 0:
            return True

        # check the offending tile ID
        result = pacman.thisLevel.GetMapTile(row, col)

        # if the tile was a wall
        if result >= 100 and result <= 199:
            return True
        else:
            return False

    def CheckIfHitWall(self, possiblePlayerX, possiblePlayerY, row, col):

        numCollisions = 0

        # check each of the 9 surrounding tiles for a collision
        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (possiblePlayerX - (iCol * 16) < 16) and (possiblePlayerX - (iCol * 16) > -16) and (
                        possiblePlayerY - (iRow * 16) < 16) and (possiblePlayerY - (iRow * 16) > -16):

                    if self.IsWall(iRow, iCol):
                        numCollisions += 1

        if numCollisions > 0:
            return True
        else:
            return False

    def CheckIfHit(self, playerX, playerY, x, y, cushion):

        if (playerX - x < cushion) and (playerX - x > -cushion) and (playerY - y < cushion) and (
                playerY - y > -cushion):
            return True
        else:
            return False

    def CheckIfHitSomething(self, playerX, playerY, row, col):

        for iRow in range(row - 1, row + 2, 1):
            for iCol in range(col - 1, col + 2, 1):

                if (playerX - (iCol * 16) < 16) and (playerX - (iCol * 16) > -16) and (playerY - (iRow * 16) < 16) and (
                        playerY - (iRow * 16) > -16):
                    # check the offending tile ID
                    result = pacman.thisLevel.GetMapTile(iRow, iCol)

                    if result == tile_ids.tileID['pellet']:
                        # got a pellet
                        pacman.thisLevel.SetMapTile(iRow, iCol, 0)
                        sounds.snd_pellet[pacman.player.pelletSndNum].play()
                        pacman.player.pelletSndNum = 1 - pacman.player.pelletSndNum

                        pacman.thisLevel.pellets -= 1

                        pacman.thisGame.AddToScore(10)

                        if pacman.thisLevel.pellets == 0:
                            # no more pellets left!
                            # WON THE LEVEL
                            pacman.thisGame.SetMode(6)


                    elif result == tile_ids.tileID['pellet-power']:
                        # got a power pellet
                        pacman.thisLevel.SetMapTile(iRow, iCol, 0)
                        sounds.snd_powerpellet.play()

                        pacman.thisGame.AddToScore(100)
                        pacman.thisGame.ghostValue = 200

                        pacman.thisGame.ghostTimer = 360
                        for i in range(0, 4, 1):
                            if pacman.ghosts[i].state == 1:
                                pacman.ghosts[i].state = 2

                    elif result == tile_ids.tileID['door-h']:
                        # ran into a horizontal door
                        for i in range(0, pacman.thisLevel.lvlWidth, 1):
                            if not i == iCol:
                                if pacman.thisLevel.GetMapTile(iRow, i) == tile_ids.tileID['door-h']:
                                    pacman.player.x = i * 16

                                    if pacman.player.velX > 0:
                                        pacman.player.x += 16
                                    else:
                                        pacman.player.x -= 16

                    elif result == tile_ids.tileID['door-v']:
                        # ran into a vertical door
                        for i in range(0, pacman.thisLevel.lvlHeight, 1):
                            if not i == iRow:
                                if pacman.thisLevel.GetMapTile(i, iCol) == tile_ids.tileID['door-v']:
                                    pacman.player.y = i * 16

                                    if pacman.player.velY > 0:
                                        pacman.player.y += 16
                                    else:
                                        pacman.player.y -= 16

    def GetGhostBoxPos(self):

        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile(row, col) == tile_ids.tileID['ghost-door']:
                    return (row, col)

        return False

    def GetPathwayPairPos(self):

        doorArray = []

        for row in range(0, self.lvlHeight, 1):
            for col in range(0, self.lvlWidth, 1):
                if self.GetMapTile(row, col) == tile_ids.tileID['door-h']:
                    # found a horizontal door
                    doorArray.append((row, col))
                elif self.GetMapTile(row, col) == tile_ids.tileID['door-v']:
                    # found a vertical door
                    doorArray.append((row, col))

        if len(doorArray) == 0:
            return False

        chosenDoor = random.randint(0, len(doorArray) - 1)

        if self.GetMapTile(doorArray[chosenDoor][0], doorArray[chosenDoor][1]) == tile_ids.tileID['door-h']:
            # horizontal door was chosen
            # look for the opposite one
            for i in range(0, pacman.thisLevel.lvlWidth, 1):
                if not i == doorArray[chosenDoor][1]:
                    if pacman.thisLevel.GetMapTile(doorArray[chosenDoor][0], i) == tile_ids.tileID['door-h']:
                        return doorArray[chosenDoor], (doorArray[chosenDoor][0], i)
        else:
            # vertical door was chosen
            # look for the opposite one
            for i in range(0, pacman.thisLevel.lvlHeight, 1):
                if not i == doorArray[chosenDoor][0]:
                    if pacman.thisLevel.GetMapTile(i, doorArray[chosenDoor][1]) == tile_ids.tileID['door-v']:
                        return doorArray[chosenDoor], (i, doorArray[chosenDoor][1])

        return False

    def PrintMap(self):

        for row in range(0, self.lvlHeight, 1):
            outputLine = ""
            for col in range(0, self.lvlWidth, 1):
                outputLine += str(self.GetMapTile(row, col)) + ", "

            # print outputLine

    def DrawMap(self):

        self.powerPelletBlinkTimer += 1
        if self.powerPelletBlinkTimer == 60:
            self.powerPelletBlinkTimer = 0

        for row in range(-1, pacman.thisGame.screenTileSize[0] + 1, 1):
            outputLine = ""
            for col in range(-1, pacman.thisGame.screenTileSize[1] + 1, 1):

                # row containing tile that actually goes here
                actualRow = pacman.thisGame.screenNearestTilePos[0] + row
                actualCol = pacman.thisGame.screenNearestTilePos[1] + col

                useTile = self.GetMapTile(actualRow, actualCol)
                if not useTile == 0 and not useTile == tile_ids.tileID['door-h'] and not useTile == tile_ids.tileID['door-v']:
                    # if this isn't a blank tile

                    if useTile == tile_ids.tileID['pellet-power']:
                        if self.powerPelletBlinkTimer < 30:
                            pacman.screen.blit(tile_ids.tileIDImage[useTile], (
                            col * 16 - pacman.thisGame.screenPixelOffset[0], row * 16 - pacman.thisGame.screenPixelOffset[1]))

                    elif useTile == tile_ids.tileID['showlogo']:
                        pacman.screen.blit(pacman.thisGame.imLogo, (
                        col * 16 - pacman.thisGame.screenPixelOffset[0], row * 16 - pacman.thisGame.screenPixelOffset[1]))

                    elif useTile == tile_ids.tileID['hiscores']:
                        pacman.screen.blit(pacman.thisGame.imHiscores, (
                        col * 16 - pacman.thisGame.screenPixelOffset[0], row * 16 - pacman.thisGame.screenPixelOffset[1]))

                    else:
                        pacman.screen.blit(tile_ids.tileIDImage[useTile], (
                        col * 16 - pacman.thisGame.screenPixelOffset[0], row * 16 - pacman.thisGame.screenPixelOffset[1]))

    def LoadLevel(self, levelNum):

        self.map = {}

        self.pellets = 0

        f = open("levels/" + str(levelNum) + ".txt", 'r')
        # ANDY -- edit this
        # fileOutput = f.read()
        # str_splitByLine = fileOutput.split('\n')
        lineNum = -1
        rowNum = 0
        useLine = False
        isReadingLevelData = False

        for line in f:

            lineNum += 1

            # print " ------- Level Line " + str(lineNum) + " -------- "
            while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"): line = line[:-1]
            while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"): line = line[1:]
            str_splitBySpace = line.split(' ')

            j = str_splitBySpace[0]

            if (j == "'" or j == ""):
                # comment / whitespace line
                # print " ignoring comment line.. "
                useLine = False
            elif j == "#":
                # special divider / attribute line
                useLine = False

                firstWord = str_splitBySpace[1]

                if firstWord == "lvlwidth":
                    self.lvlWidth = int(str_splitBySpace[2])
                    # print "Width is " + str( self.lvlWidth )

                elif firstWord == "lvlheight":
                    self.lvlHeight = int(str_splitBySpace[2])
                    # print "Height is " + str( self.lvlHeight )

                elif firstWord == "edgecolor":
                    # edge color keyword for backwards compatibility (single edge color) mazes
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "edgelightcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeLightColor = (red, green, blue, 255)

                elif firstWord == "edgeshadowcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.edgeShadowColor = (red, green, blue, 255)

                elif firstWord == "fillcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.fillColor = (red, green, blue, 255)

                elif firstWord == "pelletcolor":
                    red = int(str_splitBySpace[2])
                    green = int(str_splitBySpace[3])
                    blue = int(str_splitBySpace[4])
                    self.pelletColor = (red, green, blue, 255)

                elif firstWord == "fruittype":
                    pacman.thisFruit.fruitType = int(str_splitBySpace[2])

                elif firstWord == "startleveldata":
                    isReadingLevelData = True
                    # print "Level data has begun"
                    rowNum = 0

                elif firstWord == "endleveldata":
                    isReadingLevelData = False
                    # print "Level data has ended"

            else:
                useLine = True

            # this is a map data line
            if useLine == True:

                if isReadingLevelData == True:

                    # print str( len(str_splitBySpace) ) + " tiles in this column"

                    for k in range(0, self.lvlWidth, 1):
                        self.SetMapTile(rowNum, k, int(str_splitBySpace[k]))

                        thisID = int(str_splitBySpace[k])
                        if thisID == 4:
                            # starting position for pac-man

                            pacman.player.homeX = k * 16
                            pacman.player.homeY = rowNum * 16
                            self.SetMapTile(rowNum, k, 0)

                        elif thisID >= 10 and thisID <= 13:
                            # one of the ghosts

                            pacman.ghosts[thisID - 10].homeX = k * 16
                            pacman.ghosts[thisID - 10].homeY = rowNum * 16
                            self.SetMapTile(rowNum, k, 0)

                        elif thisID == 2:
                            # pellet

                            self.pellets += 1

                    rowNum += 1

        # reload all tiles and set appropriate colors
        tile_ids.GetCrossRef()

        # load map into the pathfinder object
        pacman.path.ResizeMap(self.lvlHeight, self.lvlWidth)

        for row in range(0, pacman.path.size[0], 1):
            for col in range(0, pacman.path.size[1], 1):
                if self.IsWall(row, col):
                    pacman.path.SetType(row, col, 1)
                else:
                    pacman.path.SetType(row, col, 0)

        # do all the level-starting stuff
        self.Restart()

    def Restart(self):

        for i in range(0, 4, 1):
            # move ghosts back to home

            pacman.ghosts[i].x = pacman.ghosts[i].homeX
            pacman.ghosts[i].y = pacman.ghosts[i].homeY
            pacman.ghosts[i].velX = 0
            pacman.ghosts[i].velY = 0
            pacman.ghosts[i].state = 1
            pacman.ghosts[i].speed = 1
            pacman.ghosts[i].Move()

            # give each ghost a path to a random spot (containing a pellet)
            (randRow, randCol) = (0, 0)

            while not self.GetMapTile(randRow, randCol) == tile_ids.tileID['pellet'] or (randRow, randCol) == (0, 0):
                randRow = random.randint(1, self.lvlHeight - 2)
                randCol = random.randint(1, self.lvlWidth - 2)

            # print "Ghost " + str(i) + " headed towards " + str((randRow, randCol))
            pacman.ghosts[i].currentPath = pacman.path.FindPath((pacman.ghosts[i].nearestRow, pacman.ghosts[i].nearestCol), (randRow, randCol))
            pacman.ghosts[i].FollowNextPathWay()

        pacman.thisFruit.active = False

        pacman.thisGame.fruitTimer = 0

        pacman.player.x = pacman.player.homeX
        pacman.player.y = pacman.player.homeY
        pacman.player.velX = 0
        pacman.player.velY = 0

        pacman.player.anim_pacmanCurrent = pacman.player.anim_pacmanS
        pacman.player.animFrame = 3