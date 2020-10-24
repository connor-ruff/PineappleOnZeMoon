import math
import sys

class Base:
    def __init__(self):
        self.chamDict = {}
        self.radsPlaced = 0
    
    def getTotalBasePineapples(self):
        
        pineapples = 0
        for ID in self.chamDict.keys():
            heat = self.chamDict[ID].getHeat(self.chamDict)
            #print(f'Heat at {ID}: {heat}')
            if (heat > 3 and heat < 7):
                 pineapples += self.chamDict[ID].numGrown
            #if (heat > 11):
                

        return pineapples



    def checkStruc11(self):
        for ID in self.chamDict.keys():
            heat = self.chamDict[ID].getHeat(self.chamDict)
            #print(f'Heat at {ID}: {heat}')
            if (heat > 7):
                return False

        return True 
        
            

        

class Chamber:

    def __init__(self, IDin, NorthIn, SouthIn, EastIn, WestIn, grownIn):
        self.ID = IDin
        self.North = NorthIn
        self.South = SouthIn
        self.East = EastIn
        self.West = WestIn
        self.numGrown = int(grownIn)
        self.hasRad = False 


    def getHeat(self, base):
        
        
        score = 0
        if (self.North is not None):
            northNode = base[self.North]
            if (northNode.North is not None and base[northNode.North].hasRad):
                score +=1
            if (northNode.East is not None and base[northNode.East].hasRad):
                score +=1
            if (northNode.West is not None and base[northNode.West].hasRad):
                score +=1
            if northNode.hasRad:
                score +=3
        if (self.South is not None):
            southNode = base[self.South]
            if (southNode.South is not None and base[southNode.South].hasRad):
                score +=1
            if (southNode.East is not None and base[southNode.East].hasRad):
                score +=1
            if (southNode.West is not None and base[southNode.West].hasRad):
                score +=1
            if southNode.hasRad:
                score +=3   
        if (self.East is not None):
            eastNode = base[self.East]
            if (eastNode.North is not None and base[eastNode.North].hasRad):
                score +=1
            if (eastNode.South is not None and base[eastNode.South].hasRad):
                score +=1
            if (eastNode.East is not None and base[eastNode.East].hasRad):
                score +=1
            if eastNode.hasRad:
                score +=3 
        if (self.West is not None):
            westNode = base[self.West]
            if (westNode.North is not None and base[westNode.North].hasRad):
                score +=1
            if (westNode.South is not None and base[westNode.South].hasRad):
                score +=1
            if (westNode.West is not None and base[westNode.West].hasRad):
                score +=1
            if westNode.hasRad:
                score +=3      
        if (self.hasRad):
            score +=5
        

        return score   
         
            
              
visited = {}

def main():
    
    if len(sys.argv) == 1:
        toOpen = 'SampleMaps.txt'
    else:
        toOpen = sys.argv[1]
    
    f = open(toOpen)
    allLines = f.readlines()
    i = 0
    j = 0
    while i < len(allLines) - 1:
        j+=1
        numRad = int(allLines[i+1].rstrip().split()[1])
        i = newBase(allLines, numRad, i+2)
        visited.clear()
        print('')

    #print(f'Total Bases: {j}')
    f.close()
    

def newBase(allLines, numRad, i):
    base = Base()
    
    chamList = []
    #print('\nnew base!')
    #print(f'lines: {len(allLines)}')
    while (i < len(allLines) and allLines[i].rstrip() != "Pineapple Moon Base"):
        # Get Chamber ID and Num Pinepaples To Grow
        chamID = allLines[i].rstrip().split()[1]
        i+=1
        numGrown = allLines[i].rstrip().split()[0]
        i+=1
        # Get Directions
        northIn = None
        southIn = None
        eastIn = None
        westIn = None
        while (i < len(allLines) and not allLines[i].rstrip().startswith('Chamber') and not allLines[i].rstrip().startswith('Pineapple Moon Base') ):
            
            if allLines[i].rstrip().startswith('North'):
                northIn = allLines[i].rstrip().split()[1]
            elif allLines[i].rstrip().startswith('West'):
                westIn = allLines[i].rstrip().split()[1]
            elif allLines[i].rstrip().startswith('East'):
                eastIn = allLines[i].rstrip().split()[1]
            elif allLines[i].rstrip().startswith('South'):
                southIn = allLines[i].rstrip().split()[1]
            i+=1
        
        
        tempCham = Chamber(chamID, northIn, southIn, eastIn, westIn, numGrown)
        base.chamDict[chamID] = tempCham
        chamList.append(tempCham)

    evaluateBase(base, numRad)

    
    return i

def evaluateBase(base, numRad):

    #print(f'Chambers: {len(base.chamDict)}  Radiators: {numRad}')

    rootID = list(base.chamDict.keys())[0]
    placeNodes(base, numRad, rootID)

    #print(f'\nTotal: {base.getTotalBasePineapples()}')
    #print(f'Placed: {base.radsPlaced}')
    #print(f'Final Check: {base.checkStruc11()}')
    

def placeNodes(base, numRad, rootID):

    if (base.radsPlaced == numRad):
        return

    if rootID in visited.keys():
        return
    
    visited[rootID] = True
    
    # Get it's current heat
    tempDict = base.chamDict
    currHeat = base.chamDict[rootID].getHeat(tempDict)
    # Cannot add if already has heat > 5
    if (currHeat > 5):
        return
    
    neighbors = []
    neighbors.append(base.chamDict[rootID].North)
    neighbors.append(base.chamDict[rootID].West)
    neighbors.append(base.chamDict[rootID].South)
    neighbors.append(base.chamDict[rootID].East)
    numNeighs = 0
    for direct in neighbors:
        if direct is not None:
            numNeighs +=1

    ratio = base.radsPlaced / numRad   # describes progress of placing the rads
    progress = len(visited)/len(base.chamDict) # describes progress of visited nodes


    if (progress > ratio):
        base.chamDict[rootID].hasRad = True

        isAcceptable = base.checkStruc11()

        if not (isAcceptable):
            base.chamDict[rootID].hasRad = False
            #print(f'Did not place rad at {rootID}')
        else:
            print(f'{rootID}', end=', ')
            base.radsPlaced +=1


    if neighbors[0] is not None:
        placeNodes(base, numRad, neighbors[0])

    if neighbors[1] is not None:
        placeNodes(base, numRad, neighbors[1])
        
    if neighbors[2] is not None:
        placeNodes(base, numRad, neighbors[2])

    if neighbors[3] is not None:
        placeNodes(base, numRad, neighbors[3])

    
    
if __name__== "__main__":
    main()
