import pygame as pg
import random

def get_neighbors(x,y):
        # gets the colors of the neighboring pixels
        # the try is there incase the pixel is on the edge of the screen
        neighbors = []
        try: neighbors.append(screen.get_at((x-1,y)))
        except: pass
        try: neighbors.append(screen.get_at((x+1,y)))
        except: pass
        try: neighbors.append(screen.get_at((x,y-1)))
        except: pass
        try: neighbors.append(screen.get_at((x,y+1)))
        except: pass
        try: neighbors.append(screen.get_at((x-1,y-1)))
        except: pass
        try: neighbors.append(screen.get_at((x+1,y+1)))
        except: pass
        try: neighbors.append(screen.get_at((x-1,y+1)))
        except: pass
        try: neighbors.append(screen.get_at((x+1,y-1)))
        except: pass

        # counts the number of black pixels and returns it
        return neighbors.count((0, 0, 0, 255))

def flip_screen():
    # upscales the pixel-screen und draws it on the display screen
    upscaled_screen =  pg.transform.scale(screen, (800, 800))
    display_screen.blit(upscaled_screen,(0,0))
    # draws the Grid
    drawGrid()
    # adjusts clock speed
    Clock.tick(fps_limit)
    # updates screen
    pg.display.flip()

# draws a grid (the size depends on the ratio of the pixel screen and the display screen)
def drawGrid():
    # draws a rectangle every 800/screen_size blocks
    blockSize = round(800/screen_size)
    for x in range(0, 800, blockSize):
        for y in range(0, 800, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(display_screen, (200,200,200), rect, 1)

# sets up pygame 
pg.init()
Clock = pg.time.Clock()

screen_size = 50
fps_limit = 60

# creates the screen that will be displayed
display_screen = pg.display.set_mode((800,800))
# creates the screen that will hold the pixels
screen = pg.Surface((screen_size,screen_size))
screen.fill((255,255,255))


run = True
play = True
while run:
    # ckecks for quiting
    event_list = pg.event.get()
    for event in event_list:
        if event.type == pg.QUIT:
            run = False
        # if mouse button is clicked set point at the position of the mouse curser
        if event.type == pg.MOUSEBUTTONDOWN:
            try:
                # get mouse position on the display window and converts it to the position om the small canvas
                pos = pg.mouse.get_pos()
                posx = int((pos[0]/800)*screen_size)
                posy = int((pos[1]/800)*screen_size)
                # If white draws a black pixel. If black sets draws a white pixel 
                if screen.get_at((posx,posy)) == (0, 0, 0, 255):
                    screen.set_at((posx,posy), (255,255,255))
                else:
                    screen.set_at((posx,posy), (0,0,0))
            except: pass
            # update screen
            flip_screen()

        if event.type == pg.KEYDOWN:
            # changes the variable that pauses the game
            if event.key == pg.K_SPACE:
                if play == True: play = False
                else: play = True
            # clears the screen
            if event.key == pg.K_ESCAPE:
                screen.fill((255,255,255))
            

    if play:
        # creates a now surface for the new version of the old surface
        new_version = pg.Surface((screen_size,screen_size))
        new_version.fill((255,255,255))
        # loops trough every pixel and applies the rules
        for x in range(screen_size):
            for y in range(screen_size):
                neighbors = get_neighbors(x,y)
                if screen.get_at((x,y)) == (0, 0, 0, 255):
                    if neighbors < 2 or neighbors > 3:
                        new_version.set_at((x,y), (255,255,255))
                    else:
                        new_version.set_at((x,y), (0,0,0))
                elif neighbors == 3:
                    new_version.set_at((x,y), (0,0,0))
        
        # sets the new frame as the default frame
        screen.blit(new_version, (0,0))

    flip_screen()