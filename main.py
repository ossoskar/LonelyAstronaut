import time

import pygame

import physics
import objects
import maps

pygame.init()
width = 1920
height = 1080
display = pygame.display.set_mode((width, height))
main_font = pygame.font.Font("fonts/EOTGR.otf", 50)
clock = pygame.time.Clock()

physics.init(display)
objects.init(display)
maps.init(display)

background = (51, 51, 51)


def close():
    pygame.quit()


def start_game(map):
    map.create_level()


def tutorial():
    first_line = objects.Label(10, 380, 1920, 100, None, background)
    first_line.add_text("1. PULL THE ASTRONAUT LIKE A SLINGSHOT", 60, "fonts/EOTGR.otf", (236, 240, 241))

    second_line = objects.Label(10, 490, 1920, 100, None, background)
    second_line.add_text('2. PRESS "T" TO TOGGLE BETWEEN DIFFERENT PROJECTION SETTINGS', 60, "fonts/EOTGR.otf", (236, 240, 241))

    third_line = objects.Label(10, 600, 1920, 100, None, background)
    third_line.add_text("3. AIM AND RELEASE TO SLING THE ASTRONAUT BACK TO THE STATION", 60, "fonts/EOTGR.otf", (236, 240, 241))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()

        display.fill(background)

        first_line.draw()
        second_line.draw()
        third_line.draw()

        pygame.display.update()
        clock.tick(120)


def select_level(map):
    level1 = objects.Button(400, 390, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level1.add_text("1", 60, "fonts/EOTGR.otf", background)

    level2 = objects.Button(648, 390, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level2.add_text("2", 60, "fonts/EOTGR.otf", background)

    level3 = objects.Button(896, 390, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level3.add_text("3", 60, "fonts/EOTGR.otf", background)

    level4 = objects.Button(1144, 390, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level4.add_text("4", 60, "fonts/EOTGR.otf", background)

    level5 = objects.Button(1392, 390, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level5.add_text("5", 60, "fonts/EOTGR.otf", background)

    level6 = objects.Button(400, 590, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level6.add_text("6", 60, "fonts/EOTGR.otf", background)

    level7 = objects.Button(648, 590, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level7.add_text("7", 60, "fonts/EOTGR.otf", background)

    level8 = objects.Button(896, 590, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level8.add_text("8", 60, "fonts/EOTGR.otf", background)

    level9 = objects.Button(1144, 590, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level9.add_text("9", 60, "fonts/EOTGR.otf", background)

    level10 = objects.Button(1392, 590, 128, 100, None, (244, 208, 63), (247, 220, 111))
    level10.add_text("10", 60, "fonts/EOTGR.otf", background)

    buttons = [level1, level2, level3, level4, level5, level6, level7, level8, level9, level10]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game()
            if event.type == pygame.MOUSEBUTTONUP:
                if level1.isActive():
                    map.specific_level(1)
                if level2.isActive():
                    map.specific_level(2)
                if level3.isActive():
                    map.specific_level(3)
                if level4.isActive():
                    map.specific_level(4)
                if level5.isActive():
                    map.specific_level(5)
                if level6.isActive():
                    map.specific_level(6)
                if level7.isActive():
                    map.specific_level(7)
                if level8.isActive():
                    map.specific_level(8)
                if level9.isActive():
                    map.specific_level(9)
                if level10.isActive():
                    map.specific_level(10)

        display.fill(background)

        for button in buttons:
            button.draw()

        pygame.display.update()
        clock.tick(120)


def game():
    map = maps.Maps()

    welcome = objects.Label(760, 100, 400, 200, None, background)
    welcome.add_text("STRANDED ASTRONAUT", 80, "fonts/EOTGR.otf", (236, 240, 241))

    start = objects.Button(500, 400, 400, 100, start_game, (72, 61, 139), (105, 73, 166))
    start.add_text("START GAME", 60, "fonts/EOTGR.otf", (236, 240, 241))

    selection = objects.Button(1000, 400, 400, 100, select_level, (72, 61, 139), (105, 73, 166))
    selection.add_text("LEVELS", 60, "fonts/EOTGR.otf", (236, 240, 241))

    tut = objects.Button(500, 600, 400, 100, tutorial, (244, 208, 63), (247, 220, 111))
    tut.add_text("TUTORIAL", 60, "fonts/EOTGR.otf", background)

    exit = objects.Button(1000, 600, 400, 100, close, (241, 148, 138), (245, 183, 177))
    exit.add_text("QUIT", 60, "fonts/EOTGR.otf", background)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close()
                if event.key == pygame.K_KP_ENTER:
                    start_game(map)

            if event.type == pygame.MOUSEBUTTONUP:
                if exit.isActive():
                    exit.action()
                if tut.isActive():
                    tut.action()
                if selection.isActive():
                    selection.action(map)
                if start.isActive():
                    time.sleep(0.2)
                    start_game(map)

        display.fill(background)

        start.draw()
        exit.draw()
        tut.draw()
        welcome.draw()
        selection.draw()

        pygame.display.update()
        clock.tick(120)


game()
