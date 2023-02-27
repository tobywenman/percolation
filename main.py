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

        checkStack = []

        for i in range(1,self.size[0]+1):
            if self.grid[i,1] == 1:
                checkStack.append((i,1))
                self.grid[i,1] = 2
        
        while len(checkStack) > 0:
            pos = checkStack[0]
            for i in [0,-1,1]:
                for j in [0,1,-1]:
                    if self.grid[pos[0]+i,pos[1]+j] == 1:
                        checkStack.insert(0,(pos[0]+i,pos[1]+j))
                        self.grid[pos[0]+i,pos[1]+j] = 2
                        if pos[1]+j == self.size[1]:
                            return True
                        break
                else:
                    continue
                break
            else:
                checkStack.pop(0)
        return False

    
    
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
