import node, tile_ids

class path_finder():

    def __init__(self):
        # map is a 1-DIMENSIONAL array.
        # use the Unfold( (row, col) ) function to convert a 2D coordinate pair
        # into a 1D index to use with this array.
        self.map = {}
        self.size = (-1, -1)  # rows by columns

        self.pathChainRev = ""
        self.pathChain = ""

        # starting and ending nodes
        self.start = (-1, -1)
        self.end = (-1, -1)

        # current node (used by algorithm)
        self.current = (-1, -1)

        # open and closed lists of nodes to consider (used by algorithm)
        self.openList = []
        self.closedList = []

        # used in algorithm (adjacent neighbors path finder is allowed to consider)
        self.neighborSet = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def ResizeMap(self, numRows, numCols):
        self.map = {}
        self.size = (numRows, numCols)

        # initialize path_finder map to a 2D array of empty nodes
        for row in range(0, self.size[0], 1):
            for col in range(0, self.size[1], 1):
                self.Set(row, col, node.node())
                self.SetType(row, col, 0)

    def CleanUpTemp(self):

        # this resets variables needed for a search (but preserves the same map / maze)

        self.pathChainRev = ""
        self.pathChain = ""
        self.current = (-1, -1)
        self.openList = []
        self.closedList = []

    def FindPath(self, startPos, endPos):

        self.CleanUpTemp()

        # (row, col) tuples
        self.start = startPos
        self.end = endPos

        # add start node to open list
        self.AddToOpenList(self.start)
        self.SetG(self.start, 0)
        self.SetH(self.start, 0)
        self.SetF(self.start, 0)

        doContinue = True

        while (doContinue == True):

            thisLowestFNode = self.GetLowestFNode()

            if not thisLowestFNode == self.end and not thisLowestFNode == False:
                self.current = thisLowestFNode
                self.RemoveFromOpenList(self.current)
                self.AddToClosedList(self.current)

                for offset in self.neighborSet:
                    thisNeighbor = (self.current[0] + offset[0], self.current[1] + offset[1])

                    if not thisNeighbor[0] < 0 and not thisNeighbor[1] < 0 and not thisNeighbor[0] > self.size[
                        0] - 1 and not thisNeighbor[1] > self.size[1] - 1 and not self.GetType(thisNeighbor) == 1:
                        cost = self.GetG(self.current) + 10

                        if self.IsInOpenList(thisNeighbor) and cost < self.GetG(thisNeighbor):
                            self.RemoveFromOpenList(thisNeighbor)

                        # if self.IsInClosedList( thisNeighbor ) and cost < self.GetG( thisNeighbor ):
                        #   self.RemoveFromClosedList( thisNeighbor )

                        if not self.IsInOpenList(thisNeighbor) and not self.IsInClosedList(thisNeighbor):
                            self.AddToOpenList(thisNeighbor)
                            self.SetG(thisNeighbor, cost)
                            self.CalcH(thisNeighbor)
                            self.CalcF(thisNeighbor)
                            self.SetParent(thisNeighbor, self.current)
            else:
                doContinue = False

        if thisLowestFNode == False:
            return False

        # reconstruct path
        self.current = self.end
        while not self.current == self.start:
            # build a string representation of the path using R, L, D, U
            if self.current[1] > self.GetParent(self.current)[1]:
                self.pathChainRev += 'R'
            elif self.current[1] < self.GetParent(self.current)[1]:
                self.pathChainRev += 'L'
            elif self.current[0] > self.GetParent(self.current)[0]:
                self.pathChainRev += 'D'
            elif self.current[0] < self.GetParent(self.current)[0]:
                self.pathChainRev += 'U'
            self.current = self.GetParent(self.current)
            self.SetType(self.current[0], self.current[1], 4)

        # because pathChainRev was constructed in reverse order, it needs to be reversed!
        for i in range(len(self.pathChainRev) - 1, -1, -1):
            self.pathChain += self.pathChainRev[i]

        # set start and ending positions for future reference
        self.SetType(self.start[0], self.start[1], 2)
        self.SetType(self.end[0], self.start[1], 3)

        return self.pathChain

    def Unfold(self, row, col):
        # this function converts a 2D array coordinate pair (row, col)
        # to a 1D-array index, for the object's 1D map array.
        return (row * self.size[1]) + col

    def Set(self, row, col, newNode):
        # sets the value of a particular map cell (usually refers to a node object)
        self.map[self.Unfold(row, col)] = newNode

    def GetType(self, val):
        row, col = val
        return self.map[self.Unfold(row, col)].type

    def SetType(self, row, col, newValue):
        self.map[self.Unfold(row, col)].type = newValue

    def GetF(self, val):
        row, col = val
        return self.map[self.Unfold(row, col)].f

    def GetG(self, val):
        row, col = val
        return self.map[self.Unfold(row, col)].g

    def GetH(self, val):
        row, col = val
        return self.map[self.Unfold(row, col)].h

    def SetG(self, val, newValue):
        row, col = val
        self.map[self.Unfold(row, col)].g = newValue

    def SetH(self, val, newValue):
        row, col = val
        self.map[self.Unfold(row, col)].h = newValue

    def SetF(self, val, newValue):
        row, col = val
        self.map[self.Unfold(row, col)].f = newValue

    def CalcH(self, val):
        row, col = val
        self.map[self.Unfold(row, col)].h = abs(row - self.end[0]) + abs(col - self.end[0])

    def CalcF(self, val):
        row, col = val
        unfoldIndex = self.Unfold(row, col)
        self.map[unfoldIndex].f = self.map[unfoldIndex].g + self.map[unfoldIndex].h

    def AddToOpenList(self, val):
        row, col = val
        self.openList.append((row, col))

    def RemoveFromOpenList(self, val):
        row, col = val
        self.openList.remove((row, col))

    def IsInOpenList(self, val):
        row, col = val
        if self.openList.count((row, col)) > 0:
            return True
        else:
            return False

    def GetLowestFNode(self):
        lowestValue = 1000  # start arbitrarily high
        lowestPair = (-1, -1)

        for iOrderedPair in self.openList:
            if self.GetF(iOrderedPair) < lowestValue:
                lowestValue = self.GetF(iOrderedPair)
                lowestPair = iOrderedPair

        if not lowestPair == (-1, -1):
            return lowestPair
        else:
            return False

    def AddToClosedList(self, val):
        row, col = val
        self.closedList.append((row, col))

    def IsInClosedList(self, val):
        row, col = val
        if self.closedList.count((row, col)) > 0:
            return True
        else:
            return False

    def SetParent(self, val, val2):
        row, col = val
        parentRow, parentCol = val2
        self.map[self.Unfold(row, col)].parent = (parentRow, parentCol)

    def GetParent(self, val):
        row, col = val
        return self.map[self.Unfold(row, col)].parent

    def draw(self):
        from pacman import screen
        for row in range(0, self.size[0], 1):
            for col in range(0, self.size[1], 1):
                thisTile = self.GetType((row, col))
                screen.blit(tile_ids.tileIDImage[thisTile], (col * 32, row * 32))