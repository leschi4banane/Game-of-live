import pygame as pg
from pygame import gfxdraw
import numpy as np

 
def update():
        new_cells = np.zeros((simulation_size,simulation_size), int)
        # loops trough every pixel and applies the rules
        for x in range(simulation_size):
            for y in range(simulation_size):
                neighbors = get_neighbors(x,y)
                if cells[x,y] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_cells[x,y] = 0
                    if neighbors == 2 or neighbors == 3:
                        new_cells[x,y] = 1
                elif neighbors == 3:
                    new_cells[x,y] = 1
        
        return new_cells

def get_neighbors(x,y):
    return cells[(x-1)%simulation_size, y] + cells[(x+1)%simulation_size, y] + cells[x, (y-1)%simulation_size] + cells[x, (y+1)%simulation_size] + cells[(x-1)%simulation_size, (y-1)%simulation_size] + cells[(x+1)%simulation_size, (y+1)%simulation_size] +  cells[(x-1)%simulation_size, (y+1)%simulation_size] + cells[(x+1)%simulation_size,(y-1)%simulation_size]

def draw_cells(grid, color):
    for x in range(simulation_size):
        for y in range(simulation_size):
            if grid[x,y] == 1:
                if circles:
                    gfxdraw.aacircle(display, int(x*block_size + block_size/2), int(y*block_size + block_size/2), int(block_size/2), color)
                    gfxdraw.filled_circle(display, int(x*block_size + block_size/2), int(y*block_size + block_size/2), int(block_size/2), color)
                else:
                    pg.draw.rect(display, color, pg.Rect(x*block_size,y*block_size,block_size,block_size))

# draws a grid (the size depends on the ratio of the pixel screen and the display screen)
def draw_grid():
    # draws a rectangle every display_size/screen_size blocks
    for x in range(0, display_size, block_size):
        for y in range(0, display_size, block_size):
            rect = pg.Rect(x, y, block_size, block_size)
            pg.draw.rect(display, color_grid, rect, 1)

def update_display():
    # clears screen
    display.fill(color_background)
    # draws trails
    if trails:
        draw_cells(cells_1, color_cell_trail.lerp(color_cell, 0.8))
        draw_cells(cells_2, color_cell_trail.lerp(color_cell, 0.6))
        draw_cells(cells_3, color_cell_trail.lerp(color_cell, 0.4))
        draw_cells(cells_4, color_cell_trail.lerp(color_cell, 0.2))
        draw_cells(cells_5, color_cell_trail)
    # draws cells
    draw_cells(cells, color_cell)
    # draws grid if its enabled 
    if grid:
        draw_grid()
    # waits for frame limit
    Clock.tick(fps_limit) 
    # updates display
    pg.display.update()

simulation_size = 50
display_size = 800
fps_limit = 10

color_background = pg.Color(0,0,0)
color_cell = pg.Color(153,0,204)
color_cell_trail = pg.Color(52, 35, 59)
color_grid = pg.Color(59,59,59)

# sets up pygame 
pg.init()
Clock = pg.time.Clock()
display = pg.display.set_mode((display_size,display_size))
pg.display.set_caption("The game of live")

# creates the 2d arrays
try:
    cells = np.loadtxt('save.txt', dtype=np.array)
    print("loaded")
except:
    cells = np.zeros((simulation_size,simulation_size), int)
    
cells_1 = np.zeros((simulation_size,simulation_size), int)
cells_2 = np.zeros((simulation_size,simulation_size), int)
cells_3 = np.zeros((simulation_size,simulation_size), int)
cells_4 = np.zeros((simulation_size,simulation_size), int)
cells_5 = np.zeros((simulation_size,simulation_size), int)

# calculates the block size depending on the simulation size and die screen size
block_size = round(display_size/simulation_size)


pause = True
trails = True
circles = True
grid = False

while True:
    # ckecks for quiting
    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            pg.quit()
        # if mouse button is clicked set point at the position of the mouse curser
        if event.type == pg.MOUSEBUTTONDOWN:
            # get mouse position on the display window and converts it to the position on the 2d array
            mouse = pg.mouse.get_pos()
            mouse_x = int((mouse[0]/display_size)*simulation_size)
            mouse_y = int((mouse[1]/display_size)*simulation_size)
            # If white draws a black pixel. If black sets draws a white pixel 
            if cells[mouse_x,mouse_y] == 0: cells[mouse_x,mouse_y] = 1
            else: cells[mouse_x,mouse_y] = 0

        if event.type == pg.KEYDOWN:
            # toggles pause
            if event.key == pg.K_SPACE:
                if pause == True: pause = False
                else: pause = True
            # clears arrays
            if event.key == pg.K_ESCAPE:
                cells = cells_1 = cells_2 = cells_3 = cells_4 = cells_5 = np.zeros((simulation_size,simulation_size), int)
            # toggles draw trails
            if event.key == pg.K_t:
                if trails == True:
                    trails = False
                    cells_1 = cells_2 = cells_3 = cells_4 = cells_5 = np.zeros((simulation_size,simulation_size), int)
                else: trails = True
            # toggles draw circles
            if event.key == pg.K_c:
                if circles == True: circles = False
                else: circles = True
            # toggles draw grid
            if event.key == pg.K_g:
                if grid == True: grid = False
                else: grid = True

            

    if pause == False:
        if trails:
            cells_5 = cells_4
            cells_4 = cells_3
            cells_3 = cells_2
            cells_2 = cells_1
            cells_1 = cells
        cells = np.copy(update())

    update_display()