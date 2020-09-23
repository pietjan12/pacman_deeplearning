import pygame, tile_ids

NO_WX= 1 # dont ask user for name in highscores.
USER_NAME = "User" #default username.

# initialise sound engine
pygame.mixer.pre_init(22050,16,2,512)
pygame.mixer.init()

#initialise sounds
snd_pellet = {}
snd_pellet[0] = pygame.mixer.Sound('sounds/pellet1.wav')
snd_pellet[1] = pygame.mixer.Sound('sounds/pellet2.wav')
snd_powerpellet = pygame.mixer.Sound('sounds/powerpellet.wav')
snd_eatgh = pygame.mixer.Sound('sounds/eatgh2.wav')
snd_fruitbounce = pygame.mixer.Sound('sounds/fruitbounce.wav')
snd_eatfruit = pygame.mixer.Sound('sounds/eatfruit.wav')
snd_extralife = pygame.mixer.Sound('sounds/extralife.wav')

#initialise clock and pygame
clock = pygame.time.Clock()
pygame.init()

window = pygame.display.set_mode((1, 1))
pygame.display.set_caption("AIMan")

screen = pygame.display.get_surface()

img_Background = pygame.image.load('backgrounds/bg.gif').convert()


#initialize player class inside pacman.py
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
            self.anim_pacmanL[i] = pygame.image.load('sprites/pacman-l ' + str(i) + ".gif")
            self.anim_pacmanR[i] = pygame.image.load('sprites/pacman-r ' + str(i) + ".gif")
            self.anim_pacmanU[i] = pygame.image.load('sprites/pacman-u ' + str(i) + ".gif")
            self.anim_pacmanD[i] = pygame.image.load('sprites/pacman-d ' + str(i) + ".gif")
            self.anim_pacmanS[i] = pygame.image.load('sprites/pacman.gif')

        self.pelletSndNum = 0

    def Move(self):

        self.nearestRow = int(((self.y + 8) / 16))
        self.nearestCol = int(((self.x + 8) / 16))

        # make sure the current velocity will not cause a collision before moving
        if not thisLevel.CheckIfHitWall(self.x + self.velX, self.y + self.velY, self.nearestRow, self.nearestCol):
            # it's ok to Move
            self.x += self.velX
            self.y += self.velY

            # check for collisions with other tiles (pellets, etc)
            thisLevel.CheckIfHitSomething(self.x, self.y, self.nearestRow, self.nearestCol)

            # check for collisions with the ghosts
            for i in range(0, 4, 1):
                if thisLevel.CheckIfHit(self.x, self.y, ghosts[i].x, ghosts[i].y, 8):
                    # hit a ghost

                    if ghosts[i].state == 1:
                        # ghost is normal
                        thisGame.SetMode(2)

                    elif ghosts[i].state == 2:
                        # ghost is vulnerable
                        # give them glasses
                        # make them run
                        thisGame.AddToScore(thisGame.ghostValue)
                        thisGame.ghostValue = thisGame.ghostValue * 2
                        snd_eatgh.play()

                        ghosts[i].state = 3
                        ghosts[i].speed = ghosts[i].speed * 4
                        # and send them to the ghost box
                        ghosts[i].x = ghosts[i].nearestCol * 16
                        ghosts[i].y = ghosts[i].nearestRow * 16
                        ghosts[i].currentPath = path.FindPath((ghosts[i].nearestRow, ghosts[i].nearestCol), (
                        thisLevel.GetGhostBoxPos()[0] + 1, thisLevel.GetGhostBoxPos()[1]))
                        ghosts[i].FollowNextPathWay()

                        # set game mode to brief pause after eating
                        thisGame.SetMode(5)

            # check for collisions with the fruit
            if thisFruit.active == True:
                if thisLevel.CheckIfHit(self.x, self.y, thisFruit.x, thisFruit.y, 8):
                    thisGame.AddToScore(2500)
                    thisFruit.active = False
                    thisGame.fruitTimer = 0
                    thisGame.fruitScoreTimer = 120
                    snd_eatfruit.play()

        else:
            # we're going to hit a wall -- stop moving
            self.velX = 0
            self.velY = 0

        # deal with power-pellet ghost timer
        if thisGame.ghostTimer > 0:
            thisGame.ghostTimer -= 1

            if thisGame.ghostTimer == 0:
                for i in range(0, 4, 1):
                    if ghosts[i].state == 2:
                        ghosts[i].state = 1
                self.ghostValue = 0

        # deal with fruit timer
        thisGame.fruitTimer += 1
        if thisGame.fruitTimer == 500:
            pathwayPair = thisLevel.GetPathwayPairPos()

            if not pathwayPair == False:
                pathwayEntrance = pathwayPair[0]
                pathwayExit = pathwayPair[1]

                thisFruit.active = True

                thisFruit.nearestRow = pathwayEntrance[0]
                thisFruit.nearestCol = pathwayEntrance[1]

                thisFruit.x = thisFruit.nearestCol * 16
                thisFruit.y = thisFruit.nearestRow * 16

                thisFruit.currentPath = path.FindPath((thisFruit.nearestRow, thisFruit.nearestCol), pathwayExit)
                thisFruit.FollowNextPathWay()

        if thisGame.fruitScoreTimer > 0:
            thisGame.fruitScoreTimer -= 1

    def Draw(self):

        if thisGame.mode == 3:
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

        screen.blit(self.anim_pacmanCurrent[self.animFrame],
                    (self.x - thisGame.screenPixelPos[0], self.y - thisGame.screenPixelPos[1]))

        if thisGame.mode == 1:
            if not self.velX == 0 or not self.velY == 0:
                # only Move mouth when pacman is moving
                self.animFrame += 1

            if self.animFrame == 9:
                # wrap to beginning
                self.animFrame = 1


#creating the pacman game from all the classes
# create fruit
ghosts = {}


#create player/pacman
player = player()

#create path finder
import path_finder
path = path_finder.path_finder()

#create ghosts
import ghost
for i in range(0,6,1):
    # remember, ghost[4] is the blue, vulnerable ghost
    ghosts[i] = ghost.ghost(i)

import fruit
thisFruit = fruit.fruit()

# create game and level objects and load first level
import game
thisGame = game.game()
import level
thisLevel = level.level()

thisLevel.LoadLevel(thisGame.GetLevelNum())

window = pygame.display.set_mode( thisGame.screenSize, pygame.DOUBLEBUF | pygame.HWSURFACE)

import gameinput

while True:
    gameinput.CheckIfCloseButton(pygame.event.get())

    if thisGame.mode == 1:
        # normal gameplay mode
        gameinput.CheckInputs(thisGame, player)

        thisGame.modeTimer += 1
        player.Move()
        for i in range(0, 4, 1):
            ghosts[i].Move()
        thisFruit.Move()

    elif thisGame.mode == 2:
        # waiting after getting hit by a ghost
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 90:
            thisLevel.Restart()

            thisGame.lives -= 1
            if thisGame.lives == -1:
                thisGame.updatehiscores(thisGame.score)
                thisGame.SetMode(3)
                thisGame.drawmidgamehiscores()
            else:
                thisGame.SetMode(4)

    elif thisGame.mode == 3:
        # game over
        gameinput.CheckInputs(thisGame, player)

    elif thisGame.mode == 4:
        # waiting to start
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 90:
            thisGame.SetMode(1)
            player.velX = player.speed

    elif thisGame.mode == 5:
        # brief pause after munching a vulnerable ghost
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 30:
            thisGame.SetMode(1)

    elif thisGame.mode == 6:
        # pause after eating all the pellets
        thisGame.modeTimer += 1

        if thisGame.modeTimer == 60:
            thisGame.SetMode(7)
            oldEdgeLightColor = thisLevel.edgeLightColor
            oldEdgeShadowColor = thisLevel.edgeShadowColor
            oldFillColor = thisLevel.fillColor

    elif thisGame.mode == 7:
        # flashing maze after finishing level
        thisGame.modeTimer += 1

        whiteSet = [10, 30, 50, 70]
        normalSet = [20, 40, 60, 80]

        if not whiteSet.count(thisGame.modeTimer) == 0:
            # member of white set
            thisLevel.edgeLightColor = (255, 255, 255, 255)
            thisLevel.edgeShadowColor = (255, 255, 255, 255)
            thisLevel.fillColor = (0, 0, 0, 255)
            tile_ids.GetCrossRef()
        elif not normalSet.count(thisGame.modeTimer) == 0:
            # member of normal set
            thisLevel.edgeLightColor = oldEdgeLightColor
            thisLevel.edgeShadowColor = oldEdgeShadowColor
            thisLevel.fillColor = oldFillColor
            tile_ids.GetCrossRef()
        elif thisGame.modeTimer == 150:
            thisGame.SetMode(8)

    elif thisGame.mode == 8:
        # blank screen before changing levels
        thisGame.modeTimer += 1
        if thisGame.modeTimer == 10:
            thisGame.SetNextLevel()

    thisGame.SmartMoveScreen()

    screen.blit(img_Background, (0, 0))

    if not thisGame.mode == 8:
        thisLevel.DrawMap()

        if thisGame.fruitScoreTimer > 0:
            if thisGame.modeTimer % 2 == 0:
                thisGame.DrawNumber(2500, thisFruit.x - thisGame.screenPixelPos[0] - 16,
                                    thisFruit.y - thisGame.screenPixelPos[1] + 4)

        for i in range(0, 4, 1):
            ghosts[i].Draw()
        thisFruit.Draw()
        player.Draw()

        if thisGame.mode == 3:
            screen.blit(thisGame.imHiscores, (32, 256))

    if thisGame.mode == 5:
        thisGame.DrawNumber(thisGame.ghostValue / 2, player.x - thisGame.screenPixelPos[0] - 4,
                            player.y - thisGame.screenPixelPos[1] + 6)

    thisGame.DrawScore()

    pygame.display.flip()

    clock.tick(60)