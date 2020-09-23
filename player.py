import pacman

class player():

    def __init__(self):
        self.x = 0
        self.y = 0
        self.velX = 0
        self.velY = 0
        self.speed = 2

        self.nearestRow = 0
        self.nearestCol = 0

        self.homeX = 0
        self.homeY = 0

        self.anim_pacmanL = {}
        self.anim_pacmanR = {}
        self.anim_pacmanU = {}
        self.anim_pacmanD = {}
        self.anim_pacmanS = {}
        self.anim_pacmanCurrent = {}

        for i in range(1, 9, 1):
            self.anim_pacmanL[i] = pacman.pygame.image.load('sprites/pacman-l' + str(i) + ".gif")
            self.anim_pacmanR[i] = pacman.pygame.image.load('sprites/pacman-r' + str(i) + ".gif")
            self.anim_pacmanU[i] = pacman.pygame.image.load('sprites/pacman-u' + str(i) + ".gif")
            self.anim_pacmanD[i] = pacman.pygame.image.load('sprites/pacman-d' + str(i) + ".gif")
            self.anim_pacmanS[i] = pacman.pygame.image.load('sprites/pacman.gif')

        self.pelletSndNum = 0

    def Move(self):

        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))

        # make sure the current velocity will not cause a collision before moving
        if not pacman.thisLevel.CheckIfHitWall(self.x + self.velX, self.y + self.velY, self.nearestRow, self.nearestCol):
            # it's ok to Move
            self.x += self.velX
            self.y += self.velY

            # check for collisions with other tiles (pellets, etc)
            pacman.thisLevel.CheckIfHitSomething(self.x, self.y, self.nearestRow, self.nearestCol)

            # check for collisions with the ghosts
            for i in range(0, 4, 1):
                if pacman.thisLevel.CheckIfHit(self.x, self.y, pacman.ghosts[i].x, pacman.ghosts[i].y, 8):
                    # hit a ghost

                    if pacman.ghosts[i].state == 1:
                        # ghost is normal
                        pacman.thisGame.SetMode(2)

                    elif pacman.ghosts[i].state == 2:
                        from pacman import snd_eatgh
                        # ghost is vulnerable
                        # give them glasses
                        # make them run
                        pacman.thisGame.AddToScore(pacman.thisGame.ghostValue)
                        pacman.thisGame.ghostValue = pacman.thisGame.ghostValue * 2
                        snd_eatgh.play()

                        pacman.ghosts[i].state = 3
                        pacman.ghosts[i].speed = pacman.ghosts[i].speed * 4
                        # and send them to the ghost box
                        pacman.ghosts[i].x = pacman.ghosts[i].nearestCol * 16
                        pacman.ghosts[i].y = pacman.ghosts[i].nearestRow * 16
                        pacman.ghosts[i].currentPath = pacman.path.FindPath((pacman.ghosts[i].nearestRow, pacman.ghosts[i].nearestCol), (
                        pacman.thisLevel.GetGhostBoxPos()[0] + 1, pacman.thisLevel.GetGhostBoxPos()[1]))
                        pacman.ghosts[i].FollowNextPathWay()

                        # set game mode to brief pause after eating
                        pacman.thisGame.SetMode(5)

            # check for collisions with the fruit
            if pacman.thisFruit.active == True:
                if pacman.thisLevel.CheckIfHit(self.x, self.y, pacman.thisFruit.x, pacman.thisFruit.y, 8):
                    from pacman import snd_eatfruit
                    pacman.thisGame.AddToScore(2500)
                    pacman.thisFruit.active = False
                    pacman.thisGame.fruitTimer = 0
                    pacman.thisGame.fruitScoreTimer = 120
                    snd_eatfruit.play()

        else:
            # we're going to hit a wall -- stop moving
            self.velX = 0
            self.velY = 0

        # deal with power-pellet ghost timer
        if pacman.thisGame.ghostTimer > 0:
            pacman.thisGame.ghostTimer -= 1

            if pacman.thisGame.ghostTimer == 0:
                for i in range(0, 4, 1):
                    if pacman.ghosts[i].state == 2:
                        pacman.ghosts[i].state = 1
                self.ghostValue = 0

        # deal with fruit timer
        pacman.thisGame.fruitTimer += 1
        if pacman.thisGame.fruitTimer == 500:
            pathwayPair = pacman.thisLevel.GetPathwayPairPos()

            if not pathwayPair == False:
                pathwayEntrance = pathwayPair[0]
                pathwayExit = pathwayPair[1]

                pacman.thisFruit.active = True

                pacman.thisFruit.nearestRow = pathwayEntrance[0]
                pacman.thisFruit.nearestCol = pathwayEntrance[1]

                pacman.thisFruit.x = pacman.thisFruit.nearestCol * 16
                pacman.thisFruit.y = pacman.thisFruit.nearestRow * 16

                pacman.thisFruit.currentPath = pacman.path.FindPath((pacman.thisFruit.nearestRow, pacman.thisFruit.nearestCol), pathwayExit)
                pacman.thisFruit.FollowNextPathWay()

        if pacman.thisGame.fruitScoreTimer > 0:
            pacman.thisGame.fruitScoreTimer -= 1

    def Draw(self):

        if pacman.thisGame.mode == 3:
            return False

        # set the current frame array to match the direction pacman is facing
        if self.velX > 0:
            self.anim_pacmanCurrent = self.anim_pacmanR
        elif self.velX < 0:
            self.anim_pacmanCurrent = self.anim_pacmanL
        elif self.velY > 0:
            self.anim_pacmanCurrent = self.anim_pacmanD
        elif self.velY < 0:
            self.anim_pacmanCurrent = self.anim_pacmanU

        pacman.screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x - pacman.thisGame.screenPixelPos[0], self.y - pacman.thisGame.screenPixelPos[1]))

        if pacman.thisGame.mode == 1:
            if not self.velX == 0 or not self.velY == 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1

            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1