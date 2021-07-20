import pygame

pygame.init()

width = 1920
height = 1080
display = None
clock = pygame.time.Clock()


def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size


pygame.display.set_mode()

# load images
PLANET1 = pygame.image.load("images/kuu.png").convert_alpha()
PLANET2 = pygame.image.load("images/mars.png").convert_alpha()
PLANET3 = pygame.image.load("images/pixar.png").convert_alpha()
PLANET4 = pygame.image.load("images/uranus.png").convert_alpha()
ISS = pygame.image.load("images/ISS.png").convert_alpha()
ASTRONAUT = pygame.image.load("images/astronaut.png").convert_alpha()
BG = pygame.transform.scale(pygame.image.load("images/back.jpg"), (width, height))


class Button:
    def __init__(self, x, y, w, h, action=None, color=(189, 195, 199), color_active=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        self.color = color
        self.color_active = color_active

        self.action = action

        self.font = None
        self.text = None
        self.text_pos = None

    def add_text(self, text, size=20, font="fonts/EOTGR.otf", text_color=(0, 0, 0)):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, text_color)
        self.text_pos = self.text.get_rect()

        self.text_pos.center = (self.x + self.w / 2, self.y + self.h / 2)

    def isActive(self):
        pos = pygame.mouse.get_pos()

        if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
            return True
        else:
            return False

    def draw(self):
        if self.isActive():
            if self.color_active is not None:
                pygame.draw.rect(display, self.color_active, (self.x, self.y, self.w, self.h))
        else:
            pygame.draw.rect(display, self.color, (self.x, self.y, self.w, self.h))

        if self.text:
            display.blit(self.text, self.text_pos)


class Label(Button):
    def draw(self):
        if self.text:
            display.blit(self.text, self.text_pos)


class Planet:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.m = r * 10 ** 23
        self.planet_img = pygame.transform.scale(PLANET1, (2 * r, 2 * r))
        self.mask = pygame.mask.from_surface(self.planet_img)

    def draw(self, window):
        window.blit(self.planet_img, (self.x - self.r, self.y - self.r))


class Iss:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.iss_img = pygame.transform.scale(ISS, (self.w, self.h))
        self.mask = pygame.mask.from_surface(self.iss_img)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, window):
        window.blit(self.iss_img, (self.x, self.y))


class Astronaut:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.m = 4500
        self.v_x = 0
        self.v_y = 0
        self.image = pygame.transform.scale(ASTRONAUT, (self.w, self.h))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.isLaunched = False

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
