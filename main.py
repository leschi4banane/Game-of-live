import pygame as pg
import random

def get_neighbors(x,y):
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

        result = 0
        for i in neighbors:
            if i == (0, 0, 0, 255):
                result += 1

        return result

def flip_screen():
    upscaled_screen =  pg.transform.scale(screen, (800, 800))
    display_screen.blit(upscaled_screen,(0,0))
    drawGrid()

    Clock.tick(fps_limit)
    pg.display.flip()

def drawGrid():
    blockSize = round(800/screen_size)
    for x in range(0, 800, blockSize):
        for y in range(0, 800, blockSize):
            rect = pg.Rect(x, y, blockSize, blockSize)
            pg.draw.rect(display_screen, (200,200,200), rect, 1)


pg.init()
Clock = pg.time.Clock()

screen_size = 50
fps_limit = 60

display_screen = pg.display.set_mode((800,800))
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
                pos = pg.mouse.get_pos()
                posx = int((pos[0]/800)*screen_size)
                posy = int((pos[1]/800)*screen_size)

                if screen.get_at((posx,posy)) == (0, 0, 0, 255):
                    screen.set_at((posx,posy), (255,255,255))
                else:
                    screen.set_at((posx,posy), (0,0,0))
            except: pass
            flip_screen()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if play == True: play = False
                else: play = True
            if event.key == pg.K_ESCAPE:
                screen.fill((255,255,255))
            

    if play:
        new_version = pg.Surface((screen_size,screen_size))
        new_version.fill((255,255,255))
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

        screen.blit(new_version, (0,0))
        flip_screen()

    else:
        flip_screen()