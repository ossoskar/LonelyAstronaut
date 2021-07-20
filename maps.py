import time

import pygame
import physics
from numpy import random

import objects

pygame.init()
width = 1920
height = 1080
display = None
main_font = pygame.font.Font("fonts/EOTGR.otf", 50)
clock = pygame.time.Clock()


def init(screen):
    global width, height, display
    display = screen
    (width, height) = display.get_rect().size
    objects.init(display)


def close():
    pygame.quit()


class Maps:
    def __init__(self):
        self.level = 1
        self.max_level = 10
        self.color = {'background': (50, 50, 50)}

    def check_win(self, astronaut, iss, planets):
        if iss.rect.collidepoint(astronaut.x + astronaut.w / 2, astronaut.y + astronaut.h / 2):
            return 1

        for planet in planets:
            if (astronaut.x + astronaut.w / 2 - planet.x) ** 2 + (
                    astronaut.y + astronaut.h / 2 - planet.y) ** 2 < planet.r ** 2:
                return -1

        if astronaut.x + astronaut.w / 2 < 0 or astronaut.x + astronaut.w / 2 > 1920 or astronaut.y + astronaut.h / 2 < 0 or astronaut.y + astronaut.h / 2 > 1080:
            return -2
        else:
            return 0

    def redraw_level(self, astronaut, iss, planets, mouse_clicked, trajectory):
        display.blit(objects.BG, (0, 0))
        # level
        level_label = main_font.render(f"Level: {self.level}", True, (236, 240, 241))
        pause_label = main_font.render("P - PAUSE", True, (236, 240, 241))
        shuffle_label = main_font.render("R - SHUFFLE", True, (236, 240, 241))
        projection_label = main_font.render("T - TOGGLE TRAJECTORY", True, (236, 240, 241))

        display.blit(level_label, (width - level_label.get_width() - 10, 10))
        display.blit(pause_label, (10, height - pause_label.get_height() - 10))
        display.blit(shuffle_label, (width - shuffle_label.get_width() - 10, height - shuffle_label.get_height() - 10))
        display.blit(projection_label,
                     (960 - projection_label.get_width() / 2, height - projection_label.get_height() - 10))

        if self.level == 1:
            tutorial_label = main_font.render("SLING THE ASTRONAUT BACK TO THE STATION", True, (236, 240, 241))
            display.blit(tutorial_label, (960 - tutorial_label.get_width() / 2, 10))

        for planet in planets:
            planet.draw(display)
        astronaut.draw(display)
        iss.draw(display)

        if mouse_clicked:
            coords = physics.projection(astronaut, planets, trajectory)
            pygame.draw.lines(display, (236, 240, 241), False, coords, 1)

        pygame.display.update()

    def create_level(self):
        astronaut_start = (192, 508)
        iss_start = (1600, 476)
        mouse_clicked = False
        run = True
        launch_happened = False
        trajectory = 1
        FPS = 120

        if self.level == 1:
            planets = []
            planet = objects.Planet(random.randint(500, 1400), random.randint(150, 900), random.randint(60, 150))
            planets.append(planet)
            astronaut = objects.Astronaut(astronaut_start[0], astronaut_start[1], 64, 64)
            iss = objects.Iss(iss_start[0], iss_start[1], 128, 128)
        else:
            planets = []
            while len(planets) < self.level:
                planet = objects.Planet(random.randint(400, 1400), random.randint(150, 900),
                                        int(random.randint(60, 150) / (self.level / 2)))
                planet.planet_img = pygame.transform.scale(
                    random.choice([objects.PLANET1, objects.PLANET2, objects.PLANET3, objects.PLANET4]),
                    (2 * planet.r, 2 * planet.r))
                if len(planets) == 0:
                    planets.append(planet)
                else:
                    overlap = False
                    for moon in planets:
                        if (moon.x - planet.x) ** 2 + (moon.y - planet.y) ** 2 < moon.r ** 2 or (
                                moon.x - planet.x) ** 2 + (moon.y - planet.y) ** 2 < planet.r ** 2:
                            overlap = True
                    if overlap is False:
                        planets.append(planet)

            astronaut = objects.Astronaut(192, 508, int(64 / (self.level / 2)),
                                          int(64 / (self.level / 2)))
            iss = objects.Iss(iss_start[0], iss_start[1], int(128 / (self.level / 4)), int(128 / (self.level / 4)))

        while run:
            clock.tick(FPS)
            self.redraw_level(astronaut, iss, planets, mouse_clicked, trajectory)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_clicked = False
                    astronaut.v_x, astronaut.v_y = -physics.launch(astronaut)[0], -physics.launch(astronaut)[1]
                    launch_happened = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        trajectory += 1
                    if event.key == pygame.K_ESCAPE:
                        self.pause()
                    if event.key == pygame.K_p:
                        self.pause()
                    if event.key == pygame.K_r:
                        self.replay_level()

            if launch_happened:
                physics.move(astronaut, planets)

            if self.check_win(astronaut, iss, planets) == 1:
                self.level_completed()

            if self.check_win(astronaut, iss, planets) < 0:
                self.level_failed(self.check_win(astronaut, iss, planets))

    def pause(self):

        replay = objects.Button(350, 500, 300, 100, self.create_level, (244, 208, 63), (247, 220, 111))
        replay.add_text("RESTART", 60, "fonts/EOTGR.otf", self.color['background'])

        exit = objects.Button(1150, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "fonts/EOTGR.otf", self.color['background'])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()
                    if event.key == pygame.K_p:
                        return

                if event.type == pygame.MOUSEBUTTONUP:
                    if replay.isActive():
                        time.sleep(0.2)
                        replay.action()
                    if exit.isActive():
                        exit.action()

            replay.draw()
            exit.draw()

            pygame.display.update()
            clock.tick(120)

    def replay_level(self):
        self.create_level()

    def specific_level(self, level):
        self.level = level
        self.create_level()

    def start_again(self):
        self.level = 1
        self.create_level()

    def level_completed(self):
        self.level += 1

        level_completed_text = objects.Label(760, 100, 400, 200, None, self.color['background'])
        if self.level <= self.max_level:
            level_completed_text.add_text("LEVEL " + str(self.level - 1) + " COMPLETED!", 80, "fonts/EOTGR.otf",
                                          (236, 240, 241))
        else:
            level_completed_text.add_text("ALL LEVELS COMPLETED!", 80, "fonts/EOTGR.otf", (236, 240, 241))

        replay = objects.Button(350, 500, 350, 100, self.replay_level, (244, 208, 63), (247, 220, 111))
        replay.add_text("PLAY AGAIN", 60, "fonts/EOTGR.otf", self.color['background'])

        if self.level <= self.max_level:
            next = objects.Button(750, 500, 350, 100, self.create_level, (88, 214, 141), (171, 235, 198))
            next.add_text("CONTINUE", 60, "fonts/EOTGR.otf", self.color['background'])
        else:
            next = objects.Button(750, 500, 350, 100, self.start_again, (88, 214, 141), (171, 235, 198))
            next.add_text("START AGAIN", 60, "fonts/EOTGR.otf", self.color['background'])

        exit = objects.Button(1150, 500, 350, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "fonts/EOTGR.otf", self.color['background'])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()

                if event.type == pygame.MOUSEBUTTONUP:
                    if replay.isActive():
                        time.sleep(0.2)
                        replay.action()
                    if exit.isActive():
                        exit.action()
                    if next.isActive():
                        time.sleep(0.2)
                        next.action()

            replay.draw()
            next.draw()
            exit.draw()
            level_completed_text.draw()

            pygame.display.update()

            clock.tick(120)

    def level_failed(self, code):
        replay = objects.Button(610, 500, 300, 100, self.replay_level, (244, 208, 63), (247, 220, 111))
        replay.add_text("PLAY AGAIN", 60, "fonts/EOTGR.otf", self.color['background'])

        exit = objects.Button(1010, 500, 300, 100, close, (241, 148, 138), (245, 183, 177))
        exit.add_text("QUIT", 60, "fonts/EOTGR.otf", self.color['background'])

        fail_text = objects.Label(760, 100, 400, 200, None, self.color['background'])
        if code == -1:
            fail_text.add_text("COLLIDED WITH A PLANET", 80, "fonts/EOTGR.otf", (236, 240, 241))
        if code == -2:
            fail_text.add_text("OUT OF BOUNDS", 80, "fonts/EOTGR.otf", (236, 240, 241))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close()

                if event.type == pygame.MOUSEBUTTONUP:
                    if replay.isActive():
                        time.sleep(0.2)
                        replay.action()
                    if exit.isActive():
                        exit.action()

            replay.draw()
            exit.draw()
            fail_text.draw()

            pygame.display.update()
            clock.tick(120)
