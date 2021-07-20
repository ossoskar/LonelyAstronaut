import pygame

pygame.init()
width = None
height = None
display = None
clock = pygame.time.Clock()
dt = 0.0001


def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


def resultant(vectors):
    x = 0
    y = 0
    for vector in vectors:
        x += vector.x
        y += vector.y

    new_vector = Vector(x, y)
    return new_vector


def distance(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return dx, dy


def launch(astronaut):
    mouse_position = pygame.mouse.get_pos()
    dx, dy = distance((astronaut.x + astronaut.w / 2, astronaut.y + astronaut.h / 2), mouse_position)

    v0_x = dx * 5000
    v0_y = dy * 5000

    return v0_x, v0_y


def projection(astronaut, planets, n_clicked):
    if n_clicked % 3 == 1:
        iterations = 50
    elif n_clicked % 3 == 2:
        iterations = 75
    elif n_clicked % 3 == 0:
        iterations = 25
    x = astronaut.x + astronaut.w / 2
    y = astronaut.y + astronaut.h / 2
    coordinates = [(x, y)]
    astronaut.v_x, astronaut.v_y = -launch(astronaut)[0], -launch(astronaut)[1]
    for i in range(iterations):
        collision = False
        forces = []
        for planet in planets:
            dist_pixels = distance((x, y), (planet.x, planet.y))
            dx = dist_pixels[0] * 7
            dy = dist_pixels[1] * 7
            d = (dx ** 2 + dy ** 2) ** 0.5
            if dx > 0:
                F_x = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dx / (d ** 3)
            else:
                F_x = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dx / (d ** 3)
            if dy > 0:
                F_y = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dy / (d ** 3)
            else:
                F_y = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dy / (d ** 3)
            force = Vector(F_x, F_y)
            forces.append(force)

        F_R = resultant(forces)
        a_x = F_R.x / astronaut.m
        a_y = F_R.y / astronaut.m

        astronaut.v_x += a_x * dt
        astronaut.v_y += a_y * dt

        x += (astronaut.v_x * dt) / 7
        y += (astronaut.v_y * dt) / 7
        for planet in planets:
            if (x - planet.x) ** 2 + (y - planet.y) ** 2 < planet.r ** 2:
                collision = True
        if collision:
            break
        coordinates.append((x, y))
    return coordinates


def move(astronaut, planets):
    forces = []
    for planet in planets:
        dist_pixels = distance((astronaut.x + astronaut.w / 2, astronaut.y + astronaut.h / 2), (planet.x, planet.y))
        dx = dist_pixels[0] * 7
        dy = dist_pixels[1] * 7
        d = (dx ** 2 + dy ** 2) ** 0.5
        if dx > 0:
            F_x = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dx / (d ** 3)
        else:
            F_x = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dx / (d ** 3)
        if dy > 0:
            F_y = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dy / (d ** 3)
        else:
            F_y = 6.67408 * 10 ** (-11) * planet.m * astronaut.m * dy / (d ** 3)
        force = Vector(F_x, F_y)
        forces.append(force)

    F_R = resultant(forces)
    a_x = F_R.x / astronaut.m
    a_y = F_R.y / astronaut.m

    astronaut.v_x += a_x * dt
    astronaut.v_y += a_y * dt

    astronaut.x += (astronaut.v_x * dt) / 7
    astronaut.y += (astronaut.v_y * dt) / 7
    return astronaut.x, astronaut.y
