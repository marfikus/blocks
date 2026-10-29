
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
import base.colors as colors

import random
import time
import pickle
import os


def start_interactive():
    import pygame

    global map

    BLOCK_SIZE = 30
    MAP_WIDTH = len(map.busy_cells_map[0]) * BLOCK_SIZE
    MAP_HEIGHT = len(map.busy_cells_map) * BLOCK_SIZE

    SEPARATOR_WIDTH = 3
    SIDEBAR_WIDTH = 200

    NEXT_FIGURE_PREVIEW_SIZE = BLOCK_SIZE * 4

    SCREEN_WIDTH = MAP_WIDTH + SEPARATOR_WIDTH + SIDEBAR_WIDTH
    SCREEN_HEIGHT = MAP_HEIGHT

    TEXT_POS_X = MAP_WIDTH + SEPARATOR_WIDTH + 10

    FPS = 60

    GAME_STATE_FILENAME = "game_state"

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris game")
    clock = pygame.time.Clock()
    TIMEREVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMEREVENT, 1000)

    screen.fill(colors.BG)
    pygame.draw.rect(screen, colors.SEPARATOR, (MAP_WIDTH, 0, SEPARATOR_WIDTH, MAP_HEIGHT))
    font = pygame.font.SysFont(None, 24)
    score_label = font.render("Score:", True, colors.TEXT)
    screen.blit(score_label, (TEXT_POS_X, 10))
    score_val_rect = None
    next_figure_label = font.render("Next:", True, colors.TEXT)
    screen.blit(next_figure_label, (TEXT_POS_X, 70))
    screen_map = pygame.Surface((MAP_WIDTH, MAP_HEIGHT))
    screen_map_rect = screen_map.get_rect(topleft=(0, 0))
    next_figure_preview = pygame.Surface((NEXT_FIGURE_PREVIEW_SIZE, NEXT_FIGURE_PREVIEW_SIZE))
    next_figure_preview_rect = next_figure_preview.get_rect(topleft=(TEXT_POS_X + 30, 95))


    def update_map():
        screen_map.fill(colors.BG)
        x = 0
        y = 0

        for string in map.busy_cells_map:
            for cell in string:
                if cell is not None:
                    pygame.draw.rect(screen_map, cell, (x, y, BLOCK_SIZE, BLOCK_SIZE))
                x += BLOCK_SIZE
            x = 0
            y += BLOCK_SIZE

        screen.blit(screen_map, screen_map_rect)


    def update_score():
        nonlocal score_val_rect

        if score_val_rect is not None:
            screen.fill(colors.BG, rect=score_val_rect)

        score_val = font.render(str(total_removed_lines), True, colors.TEXT)
        score_val_rect = score_val.get_rect(topleft=(TEXT_POS_X, 30))
        screen.blit(score_val, score_val_rect)


    def update_next_figure_preview(next_figure):
        next_figure_preview.fill(colors.BG)

        x_pad = 0
        y_pad = 0
        next_figure_width = next_figure.width * BLOCK_SIZE
        if next_figure_width < NEXT_FIGURE_PREVIEW_SIZE:
            x_pad = (NEXT_FIGURE_PREVIEW_SIZE - next_figure_width) / 2

        next_figure_height = next_figure.height * BLOCK_SIZE
        if next_figure_height < NEXT_FIGURE_PREVIEW_SIZE:
            y_pad = (NEXT_FIGURE_PREVIEW_SIZE - next_figure_height) / 2

        x = x_pad
        y = y_pad
        for string in next_figure.figure_map:
            for cell in string:
                if cell is not None:
                    pygame.draw.rect(next_figure_preview, next_figure.color, (x, y, BLOCK_SIZE, BLOCK_SIZE))
                x += BLOCK_SIZE
            x = x_pad
            y += BLOCK_SIZE

        screen.blit(next_figure_preview, next_figure_preview_rect)


    def save_state():
        with open(GAME_STATE_FILENAME, "wb") as f:
            state = {
                "map": map,
                "running": running,
                "is_need_update_map": is_need_update_map,
                "figure": figure,
                "next_figure": next_figure,
                "rotated": rotated,
                "figure_dropped": figure_dropped,
                "game_speed": game_speed,
                "total_removed_lines": total_removed_lines
            }
            pickle.dump(state, f)


    def load_state():
        if not os.path.exists(GAME_STATE_FILENAME):
            print("Saved game state not found!")
            return

        global map
        nonlocal running, is_need_update_map, figure, next_figure, rotated, figure_dropped, game_speed, total_removed_lines

        with open(GAME_STATE_FILENAME, "rb") as f:
            state = pickle.load(f)
            map = state["map"]
            running = state["running"]
            is_need_update_map = state["is_need_update_map"]
            figure = map.figures[0]
            next_figure = state["next_figure"]
            rotated = state["rotated"]
            figure_dropped = state["figure_dropped"]
            game_speed = state["game_speed"]
            total_removed_lines = state["total_removed_lines"]

        update_score()
        update_next_figure_preview(next_figure)


    running = True
    is_need_update_map = True
    figure = None
    next_figure = None
    rotated = False
    figure_dropped = True
    last = pygame.time.get_ticks()
    game_speed = 1000
    total_removed_lines = 0

    update_score()

    while running:
        # todo: вероятно можно избавиться от многих лишних флагов, где-то делать continue..
        saved = False
        loaded = False
        if figure_dropped:
            if next_figure is None:
                figure = eval(random.choice(figure_names) + "()")
            else:
                figure = next_figure
            next_figure = eval(random.choice(figure_names) + "()")
            # print("next_figure:", next_figure)
            # next_figure.show_map()
            update_next_figure_preview(next_figure)

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
                    removed_lines = map.remove_filled_lines()
                    if removed_lines > 0:
                        total_removed_lines += removed_lines
                        print(f"removed_lines: {removed_lines}, total: {total_removed_lines}")
                        update_score()
                is_need_update_map = True
                continue
            if event.type == pygame.KEYDOWN:
                # может стоит сделать обработку клавиш как в примере test_update?
                is_need_update_map = True

                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_DOWN]:
                    moved = map.move_figure(figure, figure.x, figure.y + 1)
                    if not moved:
                        map.drop_figure(figure)
                        figure_dropped = True
                        removed_lines = map.remove_filled_lines()
                        if removed_lines > 0:
                            total_removed_lines += removed_lines
                            print(f"removed_lines: {removed_lines}, total: {total_removed_lines}")
                            update_score()
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

        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()


map = Map(10, 15)

figure_names = [
    "FigureLine",
    "FigureSquare",
    "FigureT",
    "FigureL",
    "FigureBackL",
    "FigureS",
    "FigureBackS",
]

start_interactive()

