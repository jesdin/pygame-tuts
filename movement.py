import pygame

pygame.init()

win_back = (225, 225, 225)
win_res = (win_width, win_height) = (500, 480)
win = pygame.display.set_mode(win_res)
win.fill(win_back)
pygame.display.set_caption("First Game")

# loading sprites

bg = pygame.image.load('Sprites/bg.jpg')

clock = pygame.time.Clock()


class Player(object):
    walkRight = [pygame.image.load('Sprites/R1.png'), pygame.image.load('Sprites/R2.png'),
                 pygame.image.load('Sprites/R3.png'), pygame.image.load('Sprites/R4.png'),
                 pygame.image.load('Sprites/R5.png'), pygame.image.load('Sprites/R6.png'),
                 pygame.image.load('Sprites/R7.png'), pygame.image.load('Sprites/R8.png'),
                 pygame.image.load('Sprites/R9.png')]
    walkLeft = [pygame.image.load('Sprites/L1.png'), pygame.image.load('Sprites/L2.png'),
                pygame.image.load('Sprites/L3.png'), pygame.image.load('Sprites/L4.png'),
                pygame.image.load('Sprites/L5.png'), pygame.image.load('Sprites/L6.png'),
                pygame.image.load('Sprites/L7.png'), pygame.image.load('Sprites/L8.png'),
                pygame.image.load('Sprites/L9.png')]
    char = pygame.image.load('Sprites/standing.png')

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJump = False
        self.left = False
        self.right = True
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True

    def draw(self, screen):
        if self.walkCount + 1 >= 27:
            man.walkCount = 0
        if not self.standing:
            if self.left:
                screen.blit(Player.walkLeft[self.walkCount // 3], (self.x, self.y))  # int div
                if not self.isJump:
                    self.walkCount += 1
            elif self.right:
                screen.blit(Player.walkRight[self.walkCount // 3], (self.x, self.y))
                if not self.isJump:
                    self.walkCount += 1
        else:
            if self.right:
                screen.blit(Player.walkRight[0], (self.x, self.y))
            elif self.left:
                screen.blit(Player.walkLeft[0], (self.x, self.y))


class Projectile(object):
    def __init__(self, x, y, radius , color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.velocity = 8 * facing

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Enemy(object):
    walkRight = [pygame.image.load('Sprites/R1E.png'), pygame.image.load('Sprites/R2E.png'),
                 pygame.image.load('Sprites/R3E.png'), pygame.image.load('Sprites/R4E.png'),
                 pygame.image.load('Sprites/R5E.png'), pygame.image.load('Sprites/R6E.png'),
                 pygame.image.load('Sprites/R7E.png'), pygame.image.load('Sprites/R8E.png'),
                 pygame.image.load('Sprites/R9E.png'),
                 pygame.image.load('Sprites/R10E.png'), pygame.image.load('Sprites/R11E.png')]
    walkLeft = [pygame.image.load('Sprites/L1E.png'), pygame.image.load('Sprites/L2E.png'),
                pygame.image.load('Sprites/L3E.png'), pygame.image.load('Sprites/L4E.png'),
                pygame.image.load('Sprites/L5E.png'), pygame.image.load('Sprites/L6E.png'),
                pygame.image.load('Sprites/L7E.png'), pygame.image.load('Sprites/L8E.png'),
                pygame.image.load('Sprites/L9E.png'), pygame.image.load('Sprites/L10E.png'),
                pygame.image.load('Sprites/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3

    def draw(self, screen):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0
        if self.vel > 0:
            screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        pass

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = -self.vel
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = -self.vel
        pass


def redrawGameWindow():
    win.blit(bg, (0, 0))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()


# main loop
run = True
man = Player(300, 410, 64, 64)
goblin = Enemy(100, 410, 64, 64, 450)
bullets = []
while run:
    clock.tick(27)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if 500 > bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        elif man.right:
            facing = 1
        if len(bullets) < 5:
            bullets.append(Projectile(round(man.x + man.width //2), round(man.y + man.height // 2), 6, (0, 0, 0), facing))
    if keys[pygame.K_RIGHT] and man.x+man.width < win_width:
        man.x += man.velocity
        man.right = True
        man.left = False
        man.standing = False
    elif keys[pygame.K_LEFT] and man.x > 0:
        man.x += -man.velocity
        man.left = True
        man.right = False
        man.standing = False
    else:
        man.walkCount = 0
        man.standing = True
    if not man.isJump:
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            jumpDist = pow(man.jumpCount, 2) * neg / 3
            man.y -= jumpDist
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()

pygame.quit()
