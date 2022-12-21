import pygame as pg
from random import randint as rng
pg.init()
screensize = (1200, 500)
score = 0
vel = 10
width = 1200
height = 500
isJump = False
run = True
jumpCount = 10
upPressed = False
obstXY = (100, 100)
man = pg.image.load(r"man-standing.png")
all_sprites_list = pg.sprite.Group()
floorPos = pg.Rect(0, screensize[1] - 25, screensize[0], 25)
background = pg.image.load(r"background.png")
speeds = [(5,1),(10,2),(15,3),(20,5)]


font = pg.font.Font('freesansbold.ttf', 32)
smallfont = pg.font.Font('freesansbold.ttf', 16)
text = font.render(str(score), True, 'black')
text_rect = text.get_rect()
text_rect[0] = screensize[0] - text_rect[2]


screen = pg.display.set_mode(size=screensize)


text = font.render('Press E To Start!', True, 'black')
modeText = smallfont.render('Press 1, 2, 3, or 4 for Easy, Mid, Hard, or Hyper', True, 'black')
text_rect = text.get_rect(center=(screensize[0]/2, 60))
mode_Rect = modeText.get_rect()
mode_Rect[0] = 5
mode_Rect[1] = 5
screen.blit(background, (0, 0))
screen.blit(modeText, mode_Rect)
screen.blit(text, text_rect)
text_rect[0] = screensize[0] - text_rect[2]
pg.display.flip()

loading = True
while loading:
    mode_Rect = modeText.get_rect()
    mode_Rect[0] = 5
    mode_Rect[1] = 5
    text_rect[0] = screensize[0]/2 - text_rect[2]/2
    screen.blit(background, (0, 0))
    screen.blit(modeText, mode_Rect)
    screen.blit(text, text_rect)
    for i in pg.event.get():
        if i.type == pg.QUIT:
            pg.quit()
    keys = pg.key.get_pressed()
    if keys[pg.K_e]:
        loading = False
    if keys[pg.K_1]:
        modeText = font.render('Easy', True, 'black')
        mode = 0
    elif keys[pg.K_2]:
        modeText = font.render('Mid', True, 'black')
        mode = 1
    elif keys[pg.K_3]:
        modeText = font.render('Hard', True, 'black')
        mode = 2
    elif keys[pg.K_4]:
        modeText = font.render('Hyper', True, 'black')
        mode = 3
    pg.display.flip()


def generate_obstacle():
    num = rng(1, 6)
    if num == 1:
        obst = pg.image.load(r"tablesawblade.png")
    elif num == 2:
        obst = pg.image.load(r"loan.png")
    elif num == 3:
        obst = pg.image.load(r"present-red.png")
    elif num == 4:
        obst = pg.image.load(r"present-blue.png")
    elif num == 5:
        obst = pg.image.load(r"textureNotFound.png")
    elif num == 6:
        obst = pg.image.load(r"cactus.png")
    else:
        return -1
    return obst


def generate_flying_obstacle():
    num = rng(1, 5)
    if num == 1:
        obst = pg.image.load(r"flyingloan.png")
    elif num == 2:
        obst = pg.image.load(r"arrow.png")
    elif num == 3:
        obst = pg.image.load(r"flyingcactus.png")
    elif num == 4:
        obst = pg.image.load(r"bullet.png")
    elif num == 5:
        obst = pg.image.load(r"brick.png")
    else:
        return -1
    return obst

    
def update_screen(scrn, spritelist):
    screen.fill(0x87CEEB)
    screen.blit(background, (0, 0))
    spritelist.draw(scrn)
    pg.draw.rect(scrn, 0x7CFC00, floorPos)
    text = font.render(str(score), True, 'black', 0x87CEEB)
    text_rect = text.get_rect()
    text_rect[0] = screensize[0] - text_rect[2]
    screen.blit(text, text_rect)
    pg.display.flip()
    

def switch_image(obj, new_image):
    obj.image.fill('brown')
    obj.image.set_colorkey('brown')
    obj.image.blit(new_image, (0, 0))


def damage(lives):
    dead_heart = pg.image.load(r"heart-empty.png")
    live1 = lives[0]
    live2 = lives[1]
    live3 = lives[2]
    if not live1.dead:
        live1.dead = True
        switch_image(live1, dead_heart)
        return False
    elif not live2.dead:
        live2.dead = True
        switch_image(live2, dead_heart)
        return False
    elif not live3.dead:
        live3.dead = True
        switch_image(live3, dead_heart)
        return False
    else:
        return True


def respawn_obstacle(obj):
    obj.rect.x = screensize[0]
    model = generate_obstacle()
    switch_image(obj, model)


def respawn_flying_obstacle(obj):
    obj.rect.x = screensize[0]
    model = generate_flying_obstacle()
    switch_image(obj, model)


def detect_collision(obj, obj2, flying):
    collision = pg.sprite.collide_rect(obj, obj2)
    if collision and not flying:
        respawn_obstacle(obj2)
        return 1
    if collision and flying and not player.ducking:
        respawn_flying_obstacle(obj2)
        return 1
    elif not collision:
        return -1


class Obstacle(pg.sprite.Sprite):
    def __init__(self, model):
        super().__init__()

        self.image = pg.Surface([80, 80])
        self.image.fill('aqua')
        self.image.set_colorkey('aqua')
        self.image.blit(model, (0, 0))
        self.rect = self.image.get_rect()


class FlyingObstacle(pg.sprite.Sprite):
    def __init__(self, model):
        super().__init__()

        self.image = pg.Surface([80, 40])
        self.image.fill('aqua')
        self.image.set_colorkey('aqua')
        self.image.blit(model, (0, 0))
        self.rect = self.image.get_rect()


class Life(pg.sprite.Sprite):
    def __init__(self, model):
        super().__init__()

        self.image = pg.Surface([43, 35])
        self.image.fill('white')
        self.image.set_colorkey('white')
        self.image.blit(model, (0, 0))
        self.rect = self.image.get_rect()
        self.dead = False


class Player(pg.sprite.Sprite):
    def __init__(self, model):
        super().__init__()

        self.image = pg.Surface([120, 160])
        self.image.fill('white')
        self.image.set_colorkey('white')
        self.image.blit(model, (0, 0))
        self.rect = self.image.get_rect()
        self.ducking = False


life1 = Life(pg.image.load(r"heart.png"))
life1.rect.x = 5
life1.rect.y = 5
all_sprites_list.add(life1)

life2 = Life(pg.image.load(r"heart.png"))
life2.rect.x = 55
life2.rect.y = 5
all_sprites_list.add(life2)

life3 = Life(pg.image.load(r"heart.png"))
life3.rect.x = 105
life3.rect.y = 5
all_sprites_list.add(life3)

Fobs = generate_flying_obstacle()
Flying_Obstacle = FlyingObstacle(Fobs)
Flying_Obstacle.rect.x, Flying_Obstacle.rect.y = 0, screensize[1] - 40 - 25 - 120
all_sprites_list.add(Flying_Obstacle)

obs = generate_obstacle()
obstacle = Obstacle(obs)
obstacle.rect.x, obstacle.rect.y = 0, screensize[1] - 80 - 25
all_sprites_list.add(obstacle)

player = Player(man)
player.rect.x, player.rect.y = 100, screensize[1] - 160 - 20
all_sprites_list.add(player)

while run:
    
    print((keys[pg.K_DOWN] or keys[pg.K_s]))
    
    pg.time.delay(17)
    score += speeds[mode][1]
    
    Flying_Obstacle.rect.x -= speeds[mode][0]
    obstacle.rect.x -= speeds[mode][0]
    
    if detect_collision(player, obstacle, False) == 1:
        dead = damage((life1, life2, life3))
        if dead:
            run = False

    if detect_collision(player, Flying_Obstacle, True) == 1:
        dead = damage((life1, life2, life3))
        if dead:
            run = False

    if obstacle.rect.x <= 0 and Flying_Obstacle.rect.x <= 0:
        choice = rng(1, 2)
        if choice == 1:
            respawn_obstacle(obstacle)
        else:
            respawn_flying_obstacle(Flying_Obstacle)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    keys = pg.key.get_pressed()

    if (keys[pg.K_LEFT] or keys[pg.K_a]) and player.rect.x > 0:
        player.rect.x -= vel

    if (keys[pg.K_RIGHT] or keys[pg.K_d]) and player.rect.x < screensize[0] - 120:
        player.rect.x += vel
        
    if (keys[pg.K_UP] or keys[pg.K_w]) and not isJump:
        upPressed = True
        
    if (keys[pg.K_DOWN] or keys[pg.K_s]) and not isJump:
        man = pg.image.load(r"man-ducking.png")
        switch_image(player, man)
        player.ducking = True
        
    if (not keys[pg.K_DOWN] and not keys[pg.K_s]) and not isJump:
        man = pg.image.load(r"man-standing.png")
        switch_image(player, man)
        player.ducking = False
        
    if not isJump and upPressed:
        
        if jumpCount >= -10:
            man = pg.image.load(r"man-jumping.png")
            switch_image(player, man)
            player.rect.y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 0.5
            
        elif jumpCount == -11:
            player.rect.y += 5
            man = pg.image.load(r"man-standing.png")
            switch_image(player, man)
            jumpCount = 10
            isJump = False
            upPressed = False
            
        else:
            man = pg.image.load(r"man-standing.png")
            switch_image(player, man)
            jumpCount = 10
            isJump = False
            upPressed = False

    all_sprites_list.update()
    update_screen(screen, all_sprites_list)




text = font.render(f'GAME OVER | You survived {score} updates', True, 'black')
text_rect = text.get_rect(center=(screensize[0]/2, screensize[1]/2))
while True:
    
    screen.fill('white')
    screen.blit(text, text_rect)
    pg.display.flip()
    for event in pg.event.get():
    
        if event.type == pg.QUIT:
            pg.quit()
            quit()

        pg.display.update()