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
        checked = []
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
        for i in [0,-1,1]:
            for j in [0,1,-1]:
                if (pos[0]+i,pos[1]+j) not in checked and self.grid[pos[0]+i,pos[1]+j] == 1:
                    checked.append((pos[0]+i,pos[1]+j))
                    if pos[1]+j == self.size[1]:
                        return True
                    if self.solve((pos[0]+i,pos[1]+j),checked):
                        return True
        return False


newGrid = grid((100,100),0.75)

print(newGrid.percolate())

newGrid.draw()