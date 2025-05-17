import pygame
import numpy as np

# Parameters
GRID_SIZE = 50
CELL_SIZE = 10
INFECTION_PROB = 0.2
RECOVERY_TIME = 5  # Steps to recover

# Initialize grid: 0=healthy, 1=infected, 2=recovered
grid = np.zeros((GRID_SIZE, GRID_SIZE))
# Add initial infection
grid[25][25] = 1  # Patient Zero

# PyGame setup
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE))
clock = pygame.time.Clock()

running = True
while running:
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a copy of the grid to calculate next state
    new_grid = grid.copy()

    # Update rules for each cell
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            # If cell is infected, spread to neighbors
            if grid[x][y] == 1:
                # Check all 8 neighbors
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= x+dx < GRID_SIZE and 0 <= y+dy < GRID_SIZE:
                            if grid[x+dx][y+dy] == 0 and np.random.rand() < INFECTION_PROB:
                                new_grid[x+dx][y+dy] = 1
                # Track recovery
                if grid[x][y] == 1:
                    new_grid[x][y] = 2  # Recover after 1 step (simplified)

    # Update grid and colors
    grid = new_grid
    screen.fill((255, 255, 255))  # White background

    # Draw cells
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = (0, 255, 0) if grid[x][y] == 0 else \
                    (255, 0, 0) if grid[x][y] == 1 else \
                    (128, 128, 128)
            pygame.draw.rect(screen, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

    pygame.display.flip()
    clock.tick(10)  # Control simulation speed

pygame.quit()