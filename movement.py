import pygame, math

pygame.init()

win_back = (225, 225, 225)
win_res = (win_width, win_height) = (500, 480)
win = pygame.display.set_mode(win_res)
win.fill(win_back)
pygame.display.set_caption("Learning Movement")

walkRight = [pygame.image.load('Sprites/R1.png'), pygame.image.load('Sprites/R2.png'), pygame.image.load('Sprites/R3.png'), pygame.image.load('Sprites/R4.png'), pygame.image.load('Sprites/R5.png'), pygame.image.load('Sprites/R6.png'), pygame.image.load('Sprites/R7.png'), pygame.image.load('Sprites/R8.png'), pygame.image.load('Sprites/R9.png')]
walkLeft = [pygame.image.load('Sprites/L1.png'), pygame.image.load('Sprites/L2.png'), pygame.image.load('Sprites/L3.png'), pygame.image.load('Sprites/L4.png'), pygame.image.load('Sprites/L5.png'), pygame.image.load('Sprites/L6.png'), pygame.image.load('Sprites/L7.png'), pygame.image.load('Sprites/L8.png'), pygame.image.load('Sprites/L9.png')]
bg = pygame.image.load('Sprites/bg.jpg')
char = pygame.image.load('Sprites/standing.png')

clock = pygame.time.Clock()

x = 50
y = 400
width = 64
height = 64
vel = 10
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0


def redrawGameWindow():
    global walkCount
    win.blit(bg, (0, 0))
    if walkCount +1 >= 27:
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//3], (x, y))  # int div
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x, y))
        walkCount += 1
    else:
        win.blit(char, (x, y))
    pygame.display.update()


run = True
# main loop
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] and x+width < win_width:
        x += vel
        right = True
        left = False
    elif keys[pygame.K_LEFT] and x > 0:
        x += -vel
        left = True
        right = False
    else:
        left = right = False
        walkCount = 0
    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
            right = left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            jumpDist = pow(jumpCount, 2) * neg / 3
            y -= jumpDist
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    redrawGameWindow()

pygame.quit()
