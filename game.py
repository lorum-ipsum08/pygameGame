import pygame as pg
manX = 100
manY = 100
man = pg.image.load(r"pygameGame/man-standing.png")

pg.display.init()
while not pg.display.get_init:
    continue

screen = pg.display.set_mode(size=(800,500))

def update_screen(screen):
    screen.blit(man,(manX,manY))
    pg.display.flip()

run = True
while run:
    update_screen(screen)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            run = False