#initialise tiles
tileIDName = {}
tileID = {}
tileIDImage = {}
# NO_GIF_TILES -- tile numbers which do not correspond to a GIF file
NO_GIF_TILES=[23]

def GetCrossRef():
    from pacman import pygame, thisLevel
    f = open("res/crossref.txt", 'r')
    # ANDY -- edit
    # fileOutput = f.read()
    # str_splitByLine = fileOutput.split('\n')

    lineNum = 0
    useLine = False

    for i in f.readlines():
        # print " ========= Line " + str(lineNum) + " ============ "
        while len(i) > 0 and (i[-1] == '\n' or i[-1] == '\r'): i = i[:-1]
        while len(i) > 0 and (i[0] == '\n' or i[0] == '\r'): i = i[1:]
        str_splitBySpace = i.split(' ')

        j = str_splitBySpace[0]

        if (j == "'" or j == "" or j == "#"):
            # comment / whitespace line
            # print " ignoring comment line.. "
            useLine = False
        else:
            # print str(wordNum) + ". " + j
            useLine = True

        if useLine == True:
            tileIDName[int(str_splitBySpace[0])] = str_splitBySpace[1]
            tileID[str_splitBySpace[1]] = int(str_splitBySpace[0])

            thisID = int(str_splitBySpace[0])
            if not thisID in NO_GIF_TILES:
                tileIDImage[thisID] = pygame.image.load('tiles/' + str_splitBySpace[1] + '.gif')
            else:
                tileIDImage[thisID] = pygame.Surface((16, 16))

            # change colors in tileIDImage to match maze colors
            for y in range(0, 16, 1):
                for x in range(0, 16, 1):

                    if tileIDImage[thisID].get_at((x, y)) == (255, 206, 255, 255):
                        # wall edge
                        tileIDImage[thisID].set_at((x, y), thisLevel.edgeLightColor)

                    elif tileIDImage[thisID].get_at((x, y)) == (132, 0, 132, 255):
                        # wall fill
                        tileIDImage[thisID].set_at((x, y), thisLevel.fillColor)

                    elif tileIDImage[thisID].get_at((x, y)) == (255, 0, 255, 255):
                        # pellet color
                        tileIDImage[thisID].set_at((x, y), thisLevel.edgeShadowColor)

                    elif tileIDImage[thisID].get_at((x, y)) == (128, 0, 128, 255):
                        # pellet color
                        tileIDImage[thisID].set_at((x, y), thisLevel.pelletColor)

                        # print str_splitBySpace[0] + " is married to " + str_splitBySpace[1]
        lineNum += 1