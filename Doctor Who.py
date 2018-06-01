# Imports
import pygame
import os
import sys
import random

# Initialize game engine
pygame.init()


# Window
WIDTH = 1200
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
TITLE = "Doctor Who"
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(TITLE)
screen_walls = pygame.Surface(SIZE)


# Timer
clock = pygame.time.Clock()
refresh_rate = 60

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)

# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font(None, 32)
FONT_LG = pygame.font.Font(None, 64)

                                                                                                                                                                                                                                                                                                                        # Images
ship_img = pygame.image.load('assests/images/tartis.png')
ship_img2 = pygame.image.load('assests/images/tartis1.png')
ship_img3 = pygame.image.load('assests/images/tartis2.png')
ship_img4 = pygame.image.load('assests/images/tartis3.png')
ship_img5 = pygame.image.load('assests/images/tartis4.png')
laser_img = pygame.image.load('assests/images/sonic_s1.png')
mob_img = pygame.image.load('assests/images/darlkus2.png')
mob2_img = pygame.image.load('assests/images/cyber.png')
mob6_img = pygame.image.load('assests/images/cyber2.png')
bomb_img = pygame.image.load('assests/images/laser1.png')
background_img = pygame.image.load('assests/images/spaceyou1.png').convert()
intro_img = pygame.image.load('assests/images/title.png').convert()
end_img = pygame.image.load('assests/images/end_screen.png')
health_image = pygame.image.load('assests/images/Healthbar.png')
health_image2 = pygame.image.load('assests/images/HealthBar2.png')
health_image3 = pygame.image.load('assests/images/HealthBar3.png')
health_image4 = pygame.image.load('assests/images/HealthBar4.png')
health_image5= pygame.image.load('assests/images/HealthBar5.png')

# Sounds
music = pygame.mixer.music.load('assests/music/intro_music.ogg')
EXPLOSION = pygame.mixer.Sound('assests/music/dalekattack.ogg')
shot_sound = pygame.mixer.Sound('assests/music/lasersound.ogg')


# restart
def restart():
    os.execv(sys.executable, ['python'] + sys.argv)


        
        
# Stages
START = 0
PLAYING = 1
END = 2


# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y, image, image2, image3, image4, image5):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image2 = image2
        self.image3 = image3
        self.image4 = image4
        self.image5 = image5

        
        
        
        self.speed = 5
        self.shield = 5

    def move_left(self):
        self.rect.x -= self.speed
        
    def move_right(self):
        self.rect.x += self.speed
                  

    def shoot(self):
        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)

    def update(self, bombs):
        hit_list = pygame.sprite.spritecollide(self, bombs, True)

        for hit in hit_list:
            self.shield -= 1

        hit_list = pygame.sprite.spritecollide(self, mobs, False)
        if len(hit_list) > 0:
            self.shield = 0

        if self.shield <= 0:
            EXPLOSION.play()
            self.kill()

        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.right >= 1200:
            self.rect.right = 1200

        if self.shield == 5:
                pass
        elif self.shield == 4:
                self.image = self.image2
        elif self.shield == 3:
                self.image = self.image3
        elif self.shield == 2:
                self.image = self.image4
        elif self.shield == 1:
                self.image = self.image5
            
            
class Laser(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
    
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            EXPLOSION.play()
            player.score += 1
            self.kill()

class Mob2(pygame.sprite.Sprite):
    def __init__(self, x, y, image, image2):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.shield = 2
        self.image2 = image2

    def drop_bomb(self):
        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.bottom
        bombs.add(bomb)
    
    def update(self, lasers, player):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        for hit in hit_list:
                self.shield -= 1

        if self.shield <= 0:
            EXPLOSION.play()
            player.score += 2
            self.kill()


        if self.shield == 2:
                pass
        elif self.shield == 1:
                self.image = self.image2
                        

class Bomb(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
    
    
class Fleet:

    def __init__(self, mobs):
        self.mobs = mobs
        self.moving_right = True
        self.speed = 3
        self.bomb_rate = 30       

    def move(self):
        reverse = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed
                if m.rect.right >= WIDTH:
                    reverse = True
            else:
                m.rect.x -= self.speed
                if m.rect.left <=0:
                    reverse = True

        if reverse == True:
            self.moving_right = not self.moving_right
            for m in mobs:
                m.rect.y += 32
            

    def choose_bomber(self):
        rand = random.randrange(0, self.bomb_rate)
        all_mobs = mobs.sprites()
        
        if len(all_mobs) > 0 and rand == 0:
            return random.choice(all_mobs)
        else:
            return None
    
    def update(self):
        self.move()

        bomber = self.choose_bomber()
        if bomber != None:
           bomber.drop_bomb()




#time based options
class power_up(pygame.sprite.Sprite):
    
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        
        self.speed = 3

    def update(self):
        self.rect.y += self.speed        




# Make game objects
ship = Ship(384, 650, ship_img, ship_img2, ship_img3, ship_img4, ship_img5)
mob1 = Mob(75, 20, mob_img)
mob2 = Mob(150, 20, mob_img)
mob3 = Mob(225, 20, mob_img)
mob4 = Mob(300, 20, mob_img)
mob5 = Mob(375, 20, mob_img)
mob6 = Mob(450, 20, mob_img)
mob7 = Mob(525, 20, mob_img)
mob8 = Mob(600, 20, mob_img)
mob9 = Mob(675, 20, mob_img)
mob10 = Mob(750, 20, mob_img)
mob11 = Mob(825, 20, mob_img)
mob12 = Mob(900, 20, mob_img)
mob13 = Mob(975, 20, mob_img)
mob14 = Mob(1050, 20, mob_img)
mob15 = Mob(75, 80, mob_img)
mob16 = Mob(150, 80, mob_img)
mob17 = Mob(225, 80, mob_img)
mob18 = Mob(300, 80, mob_img)
mob19 = Mob(375, 80, mob_img)
mob20 = Mob(450, 80, mob_img)
mob21 = Mob(525, 80, mob_img)
mob22 = Mob(600, 80, mob_img)
mob23 = Mob(675, 80, mob_img)
mob24 = Mob(750, 80, mob_img)
mob25 = Mob(825, 80, mob_img)
mob26 = Mob(900, 80, mob_img)
mob27 = Mob(975, 80, mob_img)
mob28 = Mob(1050, 80, mob_img)
mob29 = Mob(75, 140, mob_img)
mob30 = Mob(150, 140, mob_img)
mob31 = Mob(225, 140, mob_img)
mob32 = Mob(300, 140, mob_img)
mob33 = Mob(375, 140, mob_img)
mob34 = Mob(450, 140, mob_img)
mob35 = Mob(525, 140, mob_img)
mob36 = Mob(600, 140, mob_img)
mob37 = Mob(675, 140, mob_img)
mob38 = Mob(750, 140, mob_img)
mob39 = Mob(825, 140, mob_img)
mob40 = Mob(900, 140, mob_img)
mob41 = Mob(975, 140, mob_img)
mob42 = Mob(1050, 140, mob_img)
mob43 = Mob(75, 200, mob_img)
mob44 = Mob(150, 200, mob_img)
mob45 = Mob(225, 200, mob_img)
mob46 = Mob(300, 200, mob_img)
mob47 = Mob(375, 200, mob_img)
mob48 = Mob(450, 200, mob_img)
mob49 = Mob(525, 200, mob_img)
mob50 = Mob(600, 200, mob_img)
mob51 = Mob(675, 200, mob_img)
mob52 = Mob(750, 200, mob_img)
mob53 = Mob(825, 200, mob_img)
mob54 = Mob(900, 200, mob_img)
mob55 = Mob(975, 200, mob_img)
mob56 = Mob(1050, 200, mob_img)
mob57 = Mob2(75, -200, mob2_img,mob6_img)
mob58 = Mob2(150, -200, mob2_img,mob6_img)
mob59 = Mob2(225, -200, mob2_img,mob6_img)
mob60 = Mob2(300, -200, mob2_img,mob6_img)
mob61 = Mob2(375, -200, mob2_img,mob6_img)
mob62 = Mob2(450, -200, mob2_img,mob6_img)
mob63 = Mob2(525, -200, mob2_img,mob6_img)
mob64 = Mob2(600, -200, mob2_img,mob6_img)
mob65 = Mob2(675, -200, mob2_img,mob6_img)
mob66 = Mob2(750, -200, mob2_img,mob6_img)
mob67 = Mob2(825, -200, mob2_img,mob6_img)
mob68 = Mob2(900, -200, mob2_img,mob6_img)
mob69 = Mob2(975, -200, mob2_img,mob6_img)
mob70 = Mob2(1050,-200, mob2_img,mob6_img)


# Make sprite groups
player = pygame.sprite.GroupSingle()
player.add(ship)
player.score = 0

lasers = pygame.sprite.Group()

mobs = pygame.sprite.Group()
mobs.add(mob1, mob2, mob3, mob4, mob5, mob6, mob7, mob8,mob9, mob10, mob11, mob12, mob13, mob14,mob15,mob16,mob17,mob18,mob19,mob20,mob21,mob22,mob23,mob24,mob25,mob26,mob27,mob27,mob28,
         mob29,mob30,mob31,mob32,mob33,mob34,mob35,mob36,mob37,mob38,mob39,mob40,mob41,mob42,mob43,mob44,mob45,mob46,mob47,mob48,mob49,mob50,mob51,mob52,mob53,mob54,mob55,mob56,mob57,mob58,
         mob59,mob60,mob61,mob62,mob63,mob63,mob64,mob65,mob66,mob67,mob68,mob69,mob70)

bombs = pygame.sprite.Group()


fleet = Fleet(mobs)

# set stage
stage = START

# Game helper functions
def show_title_screen():
    title_text = intro_img
    screen.blit(title_text, [0,0])
    


        
    
def show_stats(player):
    score_text = FONT_MD.render(str(player.score), 1, WHITE)
    screen.blit(score_text, [32, 32])


def show_health(ship):
    if ship.shield == 5:
        screen.blit(health_image, [1000,5])
    elif ship.shield == 4:
        screen.blit(health_image2, [1000,5])
    elif ship.shield == 3:
        screen.blit(health_image3, [1000,5])
    elif ship.shield == 2:
        screen.blit(health_image4, [1000,5])
    elif ship.shield == 1:
        screen.blit(health_image5, [1000,5])
     

# Game loop
pygame.mixer.music.play(-1)
done = False

while not done:
    # Event processing (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING
                    music = pygame.mixer.music.load('assests/music/doctor.ogg')
                    pygame.mixer.music.play(-1)
            elif stage == PLAYING: 
                if event.key == pygame.K_SPACE:
                    ship.shoot()
                    shot_sound.play()
            elif stage == END:
                restart()


    if stage == PLAYING:
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()

        if len(mobs) == 0:
            stage = END
        if ship.shield == 0:
            stage = END

                    
            
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update(bombs)
        lasers.update()   
        mobs.update(lasers, player)
        bombs.update()
        fleet.update()

        
        screen.blit(background_img,[0,0])
        show_health(ship)
        lasers.draw(screen)
        player.draw(screen)
        bombs.draw(screen)
        mobs.draw(screen)
        show_stats(player)
    
    



    if stage == START:
        show_title_screen()
    if stage == END:
        screen.blit(end_img, [0,0])
    
    



        

    
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()


    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()


