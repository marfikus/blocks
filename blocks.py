
from angle import Angle
from block import Block
from figure import Figure
from map import Map


b1 = Block("b1")
b2 = Block("b2")
b3 = Block("b3")
print(b1)
# print(b2)

# blocks = []
# for i in range(4):
#     blocks.append(Block(f"b{i}"))
# print(blocks[0])

f1 = Figure("f1")
print(f1)
f1.show_map()
f1.add_block(b1, 0, 0)
# print(f1)
# f1.show_map()
f1.add_block(b2, 0, 1)
f1.add_block(b3, 1, 1)
print(f1)
f1.show_map()

f1.make_rotation(Angle.CLOCKWISE_90)
# f1.make_rotation(Angle.CLOCKWISE_90)

map = Map(10, 10)
map.show()
map.add_figure(f1, 2, 4)
map.show()

