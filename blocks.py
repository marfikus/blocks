
from angle import Angle
from block import Block
from figure import Figure
from figure_s import FigureS
from figure_back_s import FigureBackS
from figure_t import FigureT
from figure_l import FigureL
from figure_back_l import FigureBackL
from figure_line import FigureLine
from figure_square import FigureSquare
from map import Map

import random
import time


def start_interactive():
    import pygame


    SIZE = 30
    WIDTH = len(map.busy_cells_map[0]) * SIZE
    HEIGHT = len(map.busy_cells_map) * SIZE
    FPS = 60

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My game")
    clock = pygame.time.Clock()
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, 1000)

    def update_map():
        screen.fill(BLACK)

        x = 0
        y = 0

        for string in map.busy_cells_map:
            for cell in string:
                if cell == 1:
                    pygame.draw.rect(screen, RED, pygame.Rect(x, y, SIZE, SIZE))
                x += SIZE
            x = 0
            y += SIZE

        pygame.display.update()


    # todo: сделать нормально, отдельный класс со счетчиком...
    def select_next_figure():
        nonlocal figure_index

        # if len(map.figures) == 0:
        #     print("No figures in map!")
        #     return
        
        if figure_index < len(map.figures) - 1:
            figure_index += 1
        else:
            figure_index = 0

        return map.figures[figure_index]


    figure_index = 0
    # figure = random.choice(figures)
    # map.add_figure(figure, 3, 0)
        # break

    running = True
    is_need_update_map = True
    # figure = map.figures[1]
    rotated = False
    figure_dropped = True
    last = pygame.time.get_ticks()
    game_speed = 1000

    while running:
        # saved = False
        if figure_dropped:
            figure = random.choice(figures)
            if not map.add_figure(figure, 3, 0):
                running = False
                break
            figure_dropped = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == TIMEREVENT:
                moved = map.move_figure(figure, figure.x, figure.y + 1)
                if not moved:
                    map.drop_figure(figure)
                    figure_dropped = True
                    map.remove_filled_lines()
                is_need_update_map = True
                continue
            if event.type == pygame.KEYDOWN:
                is_need_update_map = True

            pressed = pygame.key.get_pressed()
            # if pressed[pygame.K_UP]:
                # map.move_figure(figure, figure.x, figure.y - 1)
            if pressed[pygame.K_DOWN]:
                moved = map.move_figure(figure, figure.x, figure.y + 1)
                if not moved:
                    map.drop_figure(figure)
                    figure_dropped = True
                    map.remove_filled_lines()
            elif pressed[pygame.K_LEFT]:
                map.move_figure(figure, figure.x - 1, figure.y)
            elif pressed[pygame.K_RIGHT]:
                map.move_figure(figure, figure.x + 1, figure.y)
            elif pressed[pygame.K_SPACE]:
                if not rotated:
                    map.rotate_figure(figure, Angle.CLOCKWISE_90)
                    rotated = True
            # elif pressed[pygame.K_TAB]:
                # figure = select_next_figure()
            # elif pressed[pygame.K_F5]:
                # if not saved:
                    # print("save")
                    # saved = True
                    # сохранять текущее состояние карты в файл, чтобы потом продолжить игру
            
            # elif pressed[pygame.K_q]:
                # running = False

        if is_need_update_map:
            update_map()
            is_need_update_map = False
            rotated = False

        clock.tick(FPS)
    pygame.quit()


map = Map(10, 15)

figures = [
    FigureLine(),
    FigureSquare(),
    FigureT(),
    FigureL(),
    FigureBackL(),
    FigureS(),
    FigureBackS(),
]

start_interactive()

# while True:
#     figure = random.choice(figures)
#     if not map.add_figure(figure, 3, 0):
#         break

#     while True:
#         map.remove_filled_lines()
#         map.show()
#         com = input()

#         if com == "t":
#             map.rotate_figure(figure, Angle.CLOCKWISE_90)
#         elif com == "l":
#             map.move_figure(figure, figure.x - 1, figure.y)
#         elif com == "r":
#             map.move_figure(figure, figure.x + 1, figure.y)

#         if not map.move_figure(figure, figure.x, figure.y + 1):
#             break

#     map.drop_figure(figure)






