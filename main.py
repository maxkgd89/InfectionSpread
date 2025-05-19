import pygame
import numpy as np

# Simulation Parameters
GRID_SIZE = 50          # Grid dimensions (50x50)
CELL_SIZE = 10          # Pixel size of each cell
INFECTION_PROB = 0.35    # Base chance of infection spread
WALL_DENSITY = 0.2      # 10% chance of wall per cell

# Cell States
HEALTHY = 0
INFECTED = 1
RECOVERED = 2
WALL = 3

# Colors
COLORS = {
    HEALTHY: (0, 255, 0),    # Green
    INFECTED: (255, 0, 0),    # Red
    RECOVERED: (128, 128, 128), # Gray
    WALL: (0, 0, 0),          # Black
    "PLAYER": (0, 0, 255)     # Blue
}

# Initialize Grid
grid = np.zeros((GRID_SIZE, GRID_SIZE))

# Add Walls
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if np.random.rand() < WALL_DENSITY:
            grid[x][y] = WALL

# Initialize Player
player_x, player_y = 0, 0
while grid[player_x][player_y] == WALL:
    player_x, player_y = np.random.randint(0, GRID_SIZE, size=2)

# Add Initial Infection
grid[25][25] = INFECTED

# PyGame Setup
pygame.init()
screen = pygame.display.set_mode((GRID_SIZE*CELL_SIZE, GRID_SIZE*CELL_SIZE))
clock = pygame.time.Clock()
running = True
player_moved = False  # Turn-based simulation flag

# Main Loop
while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            new_x, new_y = player_x, player_y
            if event.key == pygame.K_UP: new_y -= 1
            elif event.key == pygame.K_DOWN: new_y += 1
            elif event.key == pygame.K_LEFT: new_x -= 1
            elif event.key == pygame.K_RIGHT: new_x += 1

            # Validate Movement
            if (0 <= new_x < GRID_SIZE and 
                0 <= new_y < GRID_SIZE and 
                grid[new_x][new_y] != WALL):
                player_x, player_y = new_x, new_y
                player_moved = True

    # Simulation Update (When Player Moves)
    if player_moved:
        new_grid = grid.copy()
        # Infection Spread
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if grid[x][y] == INFECTED:
                    # Infect Neighbors
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0: continue
                            nx, ny = x+dx, y+dy
                            if (0 <= nx < GRID_SIZE and 
                                0 <= ny < GRID_SIZE and 
                                grid[nx][ny] == HEALTHY):
                                if np.random.rand() < INFECTION_PROB:
                                    new_grid[nx][ny] = INFECTED
                    # Recover
                    new_grid[x][y] = RECOVERED
        grid = new_grid.copy()
        player_moved = False

    # Rendering
    screen.fill((255, 255, 255))  # White background
    # Draw Grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = COLORS[grid[x][y]]
            pygame.draw.rect(screen, color, 
                           (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))
    # Draw Player
    pygame.draw.rect(screen, COLORS["PLAYER"], 
                   (player_x*CELL_SIZE, player_y*CELL_SIZE, CELL_SIZE-1, CELL_SIZE-1))

    pygame.display.flip()
    clock.tick(10)

pygame.quit()