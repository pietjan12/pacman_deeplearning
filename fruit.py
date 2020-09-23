import pacman

class fruit():
    def __init__(self):
        # when fruit is not in use, it's in the (-1, -1) position off-screen.
        self.slowTimer = 0
        self.x = -16
        self.y = -16
        self.velX = 0
        self.velY = 0
        self.speed = 1
        self.active = False

        self.bouncei = 0
        self.bounceY = 0

        self.nearestRow = (-1, -1)
        self.nearestCol = (-1, -1)

        self.imFruit = {}
        for i in range(0, 5, 1):
            self.imFruit[i] = pacman.pygame.image.load('sprites/fruit ' + str(i) + '.gif')

        self.currentPath = ""
        self.fruitType = 1

    def Draw(self):

        if pacman.thisGame.mode == 3 or self.active == False:
            return False

        pacman.screen.blit(self.imFruit[self.fruitType],
                    (self.x - pacman.thisGame.screenPixelPos[0], self.y - pacman.thisGame.screenPixelPos[1] - self.bounceY))

    def Move(self):

        if self.active == False:
            return False

        self.bouncei += 1
        if self.bouncei == 1:
            self.bounceY = 2
        elif self.bouncei == 2:
            self.bounceY = 4
        elif self.bouncei == 3:
            self.bounceY = 5
        elif self.bouncei == 4:
            self.bounceY = 5
        elif self.bouncei == 5:
            self.bounceY = 6
        elif self.bouncei == 6:
            self.bounceY = 6
        elif self.bouncei == 9:
            self.bounceY = 6
        elif self.bouncei == 10:
            self.bounceY = 5
        elif self.bouncei == 11:
            self.bounceY = 5
        elif self.bouncei == 12:
            self.bounceY = 4
        elif self.bouncei == 13:
            self.bounceY = 3
        elif self.bouncei == 14:
            self.bounceY = 2
        elif self.bouncei == 15:
            self.bounceY = 1
        elif self.bouncei == 16:
            self.bounceY = 0
            self.bouncei = 0
            pacman.snd_fruitbounce.play()

        self.slowTimer += 1
        if self.slowTimer == 2:
            self.slowTimer = 0

            self.x += self.velX
            self.y += self.velY

            self.nearestRow = int(((self.y + 8) / 16))
            self.nearestCol = int(((self.x + 8) / 16))

            if (self.x % 16) == 0 and (self.y % 16) == 0:
                # if the fruit is lined up with the grid again
                # meaning, it's time to go to the next path item

                if len(self.currentPath) > 0:
                    self.currentPath = self.currentPath[1:]
                    self.FollowNextPathWay()

                else:
                    self.x = self.nearestCol * 16
                    self.y = self.nearestRow * 16

                    self.active = False
                    pacman.thisGame.fruitTimer = 0

    def FollowNextPathWay(self):

        # only follow this pathway if there is a possible path found!
        if not self.currentPath == False:

            if len(self.currentPath) > 0:
                if self.currentPath[0] == "L":
                    (self.velX, self.velY) = (-self.speed, 0)
                elif self.currentPath[0] == "R":
                    (self.velX, self.velY) = (self.speed, 0)
                elif self.currentPath[0] == "U":
                    (self.velX, self.velY) = (0, -self.speed)
                elif self.currentPath[0] == "D":
                    (self.velX, self.velY) = (0, self.speed)