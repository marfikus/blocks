
from angle import Angle
from block import Block
from figure import Figure
from figure_l import FigureL
from map import Map


def start_interactive(map: Map, figure: Figure):
    import pygame


    SIZE = 50
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


    update_map()


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                map.move_figure(figure, figure.x, figure.y - 1)
            if pressed[pygame.K_DOWN]:
                map.move_figure(figure, figure.x, figure.y + 1)
            if pressed[pygame.K_LEFT]:
                map.move_figure(figure, figure.x - 1, figure.y)
            if pressed[pygame.K_RIGHT]:
                map.move_figure(figure, figure.x + 1, figure.y)

        
        update_map()
        clock.tick(FPS)

    pygame.quit()


b1 = Block("b1")
b2 = Block("b2")
b3 = Block("b3")
# print(b1)
# print(b2)

# blocks = []
# for i in range(4):
#     blocks.append(Block(f"b{i}"))
# print(blocks[0])

f1 = Figure("f1")
# print(f1)
# f1.show_map()
f1.add_block(b1, 0, 0)
# print(f1)
# f1.show_map()
f1.add_block(b2, 0, 1)
f1.add_block(b3, 1, 1)
# print(f1)
# f1.show_map()

# f1.make_rotation(Angle.CLOCKWISE_90)
# f1.make_rotation(Angle.CLOCKWISE_90)

map = Map(10, 10)
# map.show()
# map.add_figure(f1, 2, 4)
# map.show()
# map.move_figure(f1, 0, 4)
# map.show()
# map.rotate_figure(f1, Angle.CLOCKWISE_90)
# map.show()
# map.rotate_figure(f1, Angle.COUNTERCLOCKWISE_90)
# map.show()
# map.rotate_figure(f1, Angle.CLOCKWISE_180)
# map.show()

fl_1 = FigureL()
print(fl_1)
fl_1.show_map()

map.add_figure(fl_1, 2, 3)
map.show()

fl_2 = FigureL()
map.add_figure(fl_2, 5, 3)
map.show()

map.rotate_figure(fl_2, Angle.CLOCKWISE_90)
map.show()

# map.move_figure(fl_1, 4, 3)
map.show()

print(fl_2)


start_interactive(map, fl_2)
