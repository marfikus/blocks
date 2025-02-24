
from base.angle import Angle
from base.block import Block
from base.figure import Figure
from base.figure_s import FigureS
from base.figure_back_s import FigureBackS
from base.figure_t import FigureT
from base.figure_l import FigureL
from base.figure_back_l import FigureBackL
from base.figure_line import FigureLine
from base.figure_square import FigureSquare
from base.map import Map

import random
import time
import pickle
import os


def start_interactive():
    import pygame

    global map

    SIZE = 30
    WIDTH = len(map.busy_cells_map[0]) * SIZE
    HEIGHT = len(map.busy_cells_map) * SIZE
    FPS = 60

    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    GAME_STATE_FILENAME = "game_state"

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


    def save_state():
        with open(GAME_STATE_FILENAME, "wb") as f:
            state = {
                "map": map,
                "running": running,
                "is_need_update_map": is_need_update_map,
                "figure": figure,
                "rotated": rotated,
                "figure_dropped": figure_dropped,
                "game_speed": game_speed,
            }
            pickle.dump(state, f)


    def load_state():
        if not os.path.exists(GAME_STATE_FILENAME):
            print("Saved game state not found!")
            return

        global map
        nonlocal running, is_need_update_map, figure, rotated, figure_dropped, game_speed

        with open(GAME_STATE_FILENAME, "rb") as f:
            state = pickle.load(f)
            map = state["map"]
            running = state["running"]
            is_need_update_map = state["is_need_update_map"]
            figure = map.figures[0]
            rotated = state["rotated"]
            figure_dropped = state["figure_dropped"]
            game_speed = state["game_speed"]


    running = True
    is_need_update_map = True
    figure = None
    rotated = False
    figure_dropped = True
    last = pygame.time.get_ticks()
    game_speed = 1000

    while running:
        # todo: вероятно можно избавиться от многих лишних флагов, где-то делать continue..
        saved = False
        loaded = False
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
            elif pressed[pygame.K_F5]:
                if not saved:
                    print("save state")
                    save_state()
                    saved = True
            elif pressed[pygame.K_F6]:
                if not loaded:
                    print("load state")
                    load_state()
                    loaded = True
            elif pressed[pygame.K_q]:
                running = False

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

