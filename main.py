import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import random

class grid():
    """class containing the particle grid and its methods"""

    def __init__(self,size,particles):
        #initialise grid
        self.grid = np.zeros(size)
        self.size = size

        #calculate number of particles
        numParticles = int(size[0]*size[1]*particles)

        #distribute particles in grid
        for i in range(numParticles):
            x = random.randint(0,size[0]-1)
            y = random.randint(0,size[1]-1)
            while self.grid[x,y] != 0:
                x = random.randint(0,size[0]-1)
                y = random.randint(0,size[1]-1)
            self.grid[x,y] = 1
        
        #pad grid
        self.grid = np.pad(self.grid,1)
    
    def draw(self):
        cmap = colors.ListedColormap(['red', 'blue','green'])
        bounds = [0,1,2,3]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig, ax = plt.subplots()
        ax.imshow(self.grid, cmap=cmap, norm=norm)

        plt.show()

    def percolate(self):
        """helper function for solve which starts the algorithm by checking all of the first row"""
        checked = []
        found = False
        for i in range(1,self.size[0]+1):
            if self.grid[i,1] == 1 and (i,1) not in checked:
                checked.append((i,1))
                found = self.solve((i,1),checked)
                if found:
                    break

        for i in checked:
            self.grid[i[0],i[1]] = 2
        return found

    def solve(self,pos,checked):
        """function which recursively checks all squares around """
        for i in [0,-1,1]:
            for j in [0,1,-1]:
                if (pos[0]+i,pos[1]+j) not in checked and self.grid[pos[0]+i,pos[1]+j] == 1:
                    checked.append((pos[0]+i,pos[1]+j))
                    if pos[1]+j == self.size[1]:
                        return True
                    if self.solve((pos[0]+i,pos[1]+j),checked):
                        return True
        return False
    
    def iterativePercolate(self):

        #stores coordinates that need checking
        checkStack = []

        #appends all of the first collumn for checking
        for i in range(1,self.size[0]+1):
            if self.grid[i,1] == 1:
                checkStack.append((i,1))
                self.grid[i,1] = 2
        
        #loops while there is coordinates left to check
        while len(checkStack) > 0:
            #current coords being checked
            pos = checkStack[0]

            #loop through adjacent squares
            for i in [0,-1,1]:
                for j in [0,1,-1]:
                    if self.grid[pos[0]+i,pos[1]+j] == 1: #checks if square has a particle and hasn't been checked
                        checkStack.insert(0,(pos[0]+i,pos[1]+j)) #pushes the newly found particle to check stack
                        self.grid[pos[0]+i,pos[1]+j] = 2 #updates grid so that the next particle has been checked
                        if pos[1]+j == self.size[1]: # returns if the other side has been reached
                            return True
                        break #breaks when a particle has been found so that the next particle can be checked
                else:
                    continue #used to break out of i loop if j loop breaks
                break
            else:
                checkStack.pop(0) #removes the current pos from the stack if all possible squares have been checked and no particles are found

        return False #return false if all loops finish and no path is found

    
    
def simulateMany(iters,tests,size):
        probs = np.zeros((len(tests),2))
        test = 0
        for i in tests:
            print(int(100*test/len(tests)))
            passes = 0
            for j in range(iters):
                newGrid = grid(size,i)
                if newGrid.percolate():
                    passes += 1
            probs[test,0] = i
            probs[test,1] = passes/iters
            test += 1
        
        return probs

# tests = np.linspace(0.1,0.9,50)

# result = simulateMany(500,tests,(50,50))

# plt.plot(result[:,0],result[:,1])

newGrid = grid((100,100),0.4)
print(newGrid.iterativePercolate())

newGrid.draw()
