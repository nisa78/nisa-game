import pygame
import sys  # sys and os is for making an executable
import os
from pygame.locals import *
pygame.init()

# Just for making an executable

def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Background, Music, Sounds, and Other Images
asset_url = [resource_path('pics/defaultR1.png'), resource_path('pics/defaultR2.png'),
             resource_path('pics/defaultR3.png'), resource_path('pics/defaultR4.png'),
             resource_path('pics/defaultR5.png'), resource_path('pics/defaultR6.png'),
             resource_path('pics/defaultR7.png'), resource_path('pics/defaultR8.png'),
             resource_path('pics/defaultR9.png'), resource_path('pics/defaultR10.png'),
             resource_path('pics/defaultR11.png'), resource_path('pics/defaultR12.png'),
             resource_path('pics/whitebg2.jpg'), resource_path('music/pew.wav'),
             resource_path('music/Curtains.mp3')]

rotationR = [pygame.image.load(asset_url[0]), pygame.image.load(asset_url[1]),
             pygame.image.load(asset_url[2]), pygame.image.load(asset_url[3]),
             pygame.image.load(asset_url[4]), pygame.image.load(asset_url[5]),
             pygame.image.load(asset_url[6]), pygame.image.load(asset_url[7]),
             pygame.image.load(asset_url[8]), pygame.image.load(asset_url[9]),
             pygame.image.load(asset_url[10]), pygame.image.load(asset_url[11])]
rotationL = [pygame.image.load(asset_url[11]), pygame.image.load(asset_url[10]),
             pygame.image.load(asset_url[9]), pygame.image.load(asset_url[8]),
             pygame.image.load(asset_url[7]), pygame.image.load(asset_url[6]),
             pygame.image.load(asset_url[5]), pygame.image.load(asset_url[4]),
             pygame.image.load(asset_url[3]), pygame.image.load(asset_url[2]),
             pygame.image.load(asset_url[1]), pygame.image.load(asset_url[0])]
bg = pygame.image.load(asset_url[12])

bulletSound = pygame.mixer.Sound(asset_url[13])
bulletSound.set_volume(0.25)

music = pygame.mixer.music.load(asset_url[14])
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Creating the Window (Screen)
winWidth = 1550 #612 #748
winHeight = 800 #376 #421
win = pygame.display.set_mode((winWidth, winHeight))
BackR = 0
BackG = 0
BackB = 0
win.fill((BackR, BackG, BackB))
pygame.display.set_caption("Co-Op")

''' Before Executable
# Background, Music, Sounds, and Other Images
rotationR = [pygame.image.load('pics/defaultR1.png'), pygame.image.load('pics/defaultR2.png'),
             pygame.image.load('pics/defaultR3.png'), pygame.image.load('pics/defaultR4.png'),
             pygame.image.load('pics/defaultR5.png'), pygame.image.load('pics/defaultR6.png'),
             pygame.image.load('pics/defaultR7.png'), pygame.image.load('pics/defaultR8.png'),
             pygame.image.load('pics/defaultR9.png'), pygame.image.load('pics/defaultR10.png'),
             pygame.image.load('pics/defaultR11.png'), pygame.image.load('pics/defaultR12.png')]
rotationL = [pygame.image.load('pics/defaultR12.png'), pygame.image.load('pics/defaultR11.png'),
             pygame.image.load('pics/defaultR10.png'), pygame.image.load('pics/defaultR9.png'),
             pygame.image.load('pics/defaultR8.png'), pygame.image.load('pics/defaultR7.png'),
             pygame.image.load('pics/defaultR6.png'), pygame.image.load('pics/defaultR5.png'),
             pygame.image.load('pics/defaultR4.png'), pygame.image.load('pics/defaultR3.png'),
             pygame.image.load('pics/defaultR2.png'), pygame.image.load('pics/defaultR1.png')]
bg = pygame.image.load('pics/whitebg2.jpg')

bulletSound = pygame.mixer.Sound('music/pew.wav')
bulletSound.set_volume(0.25)

music = pygame.mixer.music.load('music/Curtains.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
'''

# Setting Clock & Score
clock = pygame.time.Clock()
score = 0


class Player(object):  # Don't need to type object
    def __init__(self, x, y, width, height):  # Initialization Function
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.moving = False
        self.right = False
        self.left = False
        self.rotationCount = 0
        self.standing = True
        self.hitbox = (self.x + 18, self.y + 13, 25, 50)  # x,y,width,height - rectangle!

    def draw(self, win):
        if self.rotationCount + 1 >= 36:
            # This is for index error, 12 sprites displayed for 3 frames = 36... 36 frames per second
            self.rotationCount = 0

        if not(self.standing):
            if self.right:
                win.blit(rotationR[self.rotationCount // 3], (self.x, self.y))
                # This is integer division - 1/3 = 0, 4/3 = 1... Displays for 3 frames
                self.rotationCount += 1
            elif self.left:
                win.blit(rotationL[self.rotationCount // 3], (self.x, self.y))
                self.rotationCount += 1
        else:
            if self.right:
                win.blit(rotationR[self.rotationCount // 3], (self.x, self.y))
            elif self.left:
                win.blit(rotationL[self.rotationCount // 3], (self.x, self.y))
            else:
                win.blit(rotationR[self.rotationCount // 3], (self.x, self.y))
        #self.hitbox = (self.x + 18, self.y + 13, 25, 50)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)  # Drawing a hit box around character


class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing  # Either 1 or -1 to say left or rightdw
        self.vel = 8 * facing  # * facing so the projectile knows to face left or right

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius, 1)  # No 1 = filled in


def redrawGameWindow():
    win.blit(bg, (0, 0))
    main.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

# MAIN LOOP

# Begin game (Main Loop)
main = Player(15, 335, 64, 64)
bullets = []
shootLoop = 0
run = True
while run:
    clock.tick(36)  # Sets FPS to 36

    # Setting a timer
    if shootLoop > 0:
        # After shooting a bullet (see # Shooting section) - shootLoop is set to 1...
        # The while loop will run and add 1 until shootLoop > 3, setting shootLoop to 0 and allowing the user to shoot
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for bullet in bullets:
        if bullet.x < winWidth and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)

    # Quitting
    for event in pygame.event.get():
        # Quits if x button is clicked
        if event.type == pygame.QUIT:
            run = False
        # Quits when escape key is pressed
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                run = False

    # Main Character Controls
    keys = pygame.key.get_pressed()
    # Shooting
    if keys[pygame.K_SPACE] and shootLoop == 0:
        if main.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(main.x + main.width //2), round(main.y + main.height // 2),
                                      6, (0, 0, 0), facing))
            bulletSound.play()
        shootLoop = 1

    if keys[pygame.K_a] and main.x > main.vel:
        main.x -= main.vel
        main.moving = True
        main.right = False
        main.left = True
        main.standing = False  # This is part of the standing still not facing straight forward code
    elif keys[pygame.K_d] and main.x < winWidth - main.width - main.vel:
        main.x += main.vel
        main.moving = True
        main.right = True
        main.left = False
        main.standing = False
    else:
        #  main.right = False  These were for standing still = straight forward
        #  main.left = False
        main.standing = True
        main.walkCount = 0

    if keys[pygame.K_w] and main.y > main.vel:
        main.y -= main.vel
    if keys[pygame.K_s] and main.y < winHeight - main.height - main.vel:
        main.y += main.vel

    redrawGameWindow()

pygame.quit()
# End game (End Loop)