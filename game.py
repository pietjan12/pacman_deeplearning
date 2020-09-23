import pacman

class game():

    def defaulthiscorelist(self):
        return [(100000, "Bob"), (80000, "Pieterke")]

    def gethiscores(self):
        """If res/hiscore.txt exists, read it. If not, return the default high scores.
           Output is [ (score,name) , (score,name) , .. ]. Always 6 entries."""
        try:
            f = open("res/hiscore.txt")
            hs = []
            for line in f:
                while len(line) > 0 and (line[0] == "\n" or line[0] == "\r"): line = line[1:]
                while len(line) > 0 and (line[-1] == "\n" or line[-1] == "\r"): line = line[:-1]
                score = int(line.split(" ")[0])
                name = line.partition(" ")[2]
                if score > 99999999: score = 99999999
                if len(name) > 22: name = name[:22]
                hs.append((score, name))
            f.close()
            if len(hs) > 6: hs = hs[:6]
            while len(hs) < 6: hs.append((0, ""))
            return hs
        except IOError:
            return self.defaulthiscorelist()

    def writehiscores(self, hs):
        """Given a new list, write it to the default file."""
        fname = "res/hiscore.txt"
        f = open(fname, "w")
        for line in hs:
            f.write(str(line[0]) + " " + line[1] + "\n")
        f.close()

    def getplayername(self):
        """Ask the player his name, to go on the high-score list."""
        if pacman.NO_WX: return pacman.USER_NAME
        try:
            import wx
        except:
            print("Pacman Error: No module wx. Can not ask the user his name!")
            print("     :(       Download wx from http://www.wxpython.org/")
            print("     :(       To avoid seeing this error again, set NO_WX in file pacman.pyw.")
            return pacman.USER_NAME
        app = wx.App(None)
        dlog = wx.TextEntryDialog(None, "You made the high-score list! Name:")
        dlog.ShowModal()
        name = dlog.GetValue()
        dlog.Destroy()
        app.Destroy()
        return name

    def updatehiscores(self, newscore):
        """Add newscore to the high score list, if appropriate."""
        hs = self.gethiscores()
        for line in hs:
            if newscore >= line[0]:
                hs.insert(hs.index(line), (newscore, self.getplayername()))
                hs.pop(-1)
                break
        self.writehiscores(hs)

    def makehiscorelist(self):
        "Read the High-Score file and convert it to a useable Surface."
        f = pacman.pygame.font.Font("res/VeraMoBd.ttf", 10)
        scoresurf = pacman.pygame.Surface((276, 86), pacman.pygame.SRCALPHA)
        scoresurf.set_alpha(200)
        linesurf = f.render(" " * 18 + "HIGH SCORES", 1, (255, 255, 0))
        scoresurf.blit(linesurf, (0, 0))
        hs = self.gethiscores()
        vpos = 0
        for line in hs:
            vpos += 12
            linesurf = f.render(line[1].rjust(22) + str(line[0]).rjust(9), 1, (255, 255, 255))
            scoresurf.blit(linesurf, (0, vpos))
        return scoresurf

    def drawmidgamehiscores(self):
        """Redraw the high-score list image after pacman dies."""
        self.imHiscores = self.makehiscorelist()

    def __init__(self):
        self.levelNum = 0
        self.score = 0
        self.lives = 3

        # game "mode" variable
        # 1 = normal
        # 2 = hit ghost
        # 3 = game over
        # 4 = wait to start
        # 5 = wait after eating ghost
        # 6 = wait after finishing level
        self.mode = 0
        self.modeTimer = 0
        self.ghostTimer = 0
        self.ghostValue = 0
        self.fruitTimer = 0
        self.fruitScoreTimer = 0
        self.fruitScorePos = (0, 0)

        self.SetMode(3)

        # camera variables
        self.screenPixelPos = (0, 0)  # absolute x,y position of the screen from the upper-left corner of the level
        self.screenNearestTilePos = (0, 0)  # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (0, 0)  # offset in pixels of the screen from its nearest-tile position

        self.screenTileSize = (23, 21)
        self.screenSize = (self.screenTileSize[1] * 16, self.screenTileSize[0] * 16)

        # numerical display digits
        self.digit = {}
        for i in range(0, 10, 1):
            self.digit[i] = pacman.pygame.image.load("text/" + str(i) + ".gif")
        self.imLife = pacman.pygame.image.load("text/life.gif")
        self.imGameOver = pacman.pygame.image.load("text/gameover.gif")
        self.imReady = pacman.pygame.image.load("text/ready.gif")
        self.imLogo = pacman.pygame.image.load("text/logo.gif")
        self.imHiscores = self.makehiscorelist()

    def StartNewGame(self):
        self.levelNum = 1
        self.score = 0
        self.lives = 3

        self.SetMode(4)
        pacman.thisLevel.LoadLevel(pacman.thisGame.GetLevelNum())

    def AddToScore(self, amount):

        extraLifeSet = [25000, 50000, 100000, 150000]

        for specialScore in extraLifeSet:
            if self.score < specialScore and self.score + amount >= specialScore:
                pacman.snd_extralife.play()
                pacman.thisGame.lives += 1

        self.score += amount

    def DrawScore(self):
        self.DrawNumber(self.score, 24 + 16, self.screenSize[1] - 24)

        for i in range(0, self.lives, 1):
            pacman.screen.blit(self.imLife, (24 + i * 10 + 16, self.screenSize[1] - 12))

        pacman.screen.blit(pacman.thisFruit.imFruit[pacman.thisFruit.fruitType], (4 + 16, self.screenSize[1] - 20))

        if self.mode == 3:
            pacman.screen.blit(self.imGameOver, (self.screenSize[0] / 2 - 32, self.screenSize[1] / 2 - 10))
        elif self.mode == 4:
            pacman.screen.blit(self.imReady, (self.screenSize[0] / 2 - 20, self.screenSize[1] / 2 + 12))

        self.DrawNumber(self.levelNum, 0, self.screenSize[1] - 12)

    def DrawNumber(self, number, x, y):
        strNumber = str(int(number))
        for i in range(0, len(strNumber), 1):
            iDigit = int(strNumber[i])
            pacman.screen.blit(self.digit[iDigit], (x + i * 9, y))

    def SmartMoveScreen(self):

        possibleScreenX = pacman.player.x - self.screenTileSize[1] / 2 * 16
        possibleScreenY = pacman.player.y - self.screenTileSize[0] / 2 * 16

        if possibleScreenX < 0:
            possibleScreenX = 0
        elif possibleScreenX > pacman.thisLevel.lvlWidth * 16 - self.screenSize[0]:
            possibleScreenX = pacman.thisLevel.lvlWidth * 16 - self.screenSize[0]

        if possibleScreenY < 0:
            possibleScreenY = 0
        elif possibleScreenY > pacman.thisLevel.lvlHeight * 16 - self.screenSize[1]:
            possibleScreenY = pacman.thisLevel.lvlHeight * 16 - self.screenSize[1]

        pacman.thisGame.MoveScreen(possibleScreenX, possibleScreenY)

    def MoveScreen(self, newX, newY):
        self.screenPixelPos = (newX, newY)
        self.screenNearestTilePos = (
        int(newY / 16), int(newX / 16))  # nearest-tile position of the screen from the UL corner
        self.screenPixelOffset = (newX - self.screenNearestTilePos[1] * 16, newY - self.screenNearestTilePos[0] * 16)

    def GetScreenPos(self):
        return self.screenPixelPos

    def GetLevelNum(self):
        return self.levelNum

    def SetNextLevel(self):
        self.levelNum += 1

        self.SetMode(4)
        pacman.thisLevel.LoadLevel(pacman.thisGame.GetLevelNum())

        pacman.player.velX = 0
        pacman.player.velY = 0
        pacman.player.anim_pacmanCurrent = pacman.player.anim_pacmanS

    def SetMode(self, newMode):
        self.mode = newMode
        self.modeTimer = 0
        # print " ***** GAME MODE IS NOW ***** " + str(newMode)