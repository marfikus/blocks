
from typing import List
from .block import Block
from .coords import Coords


class Rotation:
    def __init__(self):
        self.is_active: bool = False
        self.blocks_count: int = 0
        self.width: int = 0
        self.height: int = 0
        self.figure_map: List[List[Block | None]] = []

        
    def get_blocks_coords(self) -> List[Coords]:
        coords: List[Coords] = []
        
        for y in range(self.height):
            for x in range(self.width):
                if self.figure_map[y][x] != None:
                    coords.append(Coords(x, y))
        
        return coords
    

    def show_map(self):
        print("----------------")
        for str in self.figure_map:
            for obj in str:
                if obj is None:
                    print(0, end=" ")
                else:
                    print(1, end=" ")
            print()
        print("----------------")

