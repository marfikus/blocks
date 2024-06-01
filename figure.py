
from typing import List
from block import Block


class Figure:
    def __init__(self, title: str = ""):
        self.title = title
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.blocks: List[Block] = []
        self.figure_map: List[List[Block | None]] = []


    def __str__(self):
        return (f"Figure '{self.title}': " 
                  f"x:{self.x}, "
                  f"y:{self.y}, "
                  f"width:{self.width}, "
                  f"height:{self.height}"
                # f"figure map:\n\t{self.show_map()}"
        )


    def add_block(self, new_block: Block, x: int, y: int):
        for block in self.blocks:
            if block.x == x and block.y == y:
                print(f"{self.title}: busy cell!")
                return
            
        new_block.x = x
        new_block.y = y
        self.blocks.append(new_block)
        self._update_figure_size()
        self._update_figure_map()
        # self.figure_map[x][y] = new_block


    def _update_figure_size(self):
        max_x: int = 0
        max_y: int = 0

        for block in self.blocks:
            if block.x > max_x: max_x = block.x
            if block.y > max_y: max_y = block.y

        self.width = max_x + 1
        self.height = max_y + 1


    def _update_figure_map(self):
        new_figure_map: List[List[Block | None]] = self._create_map(self.height, self.width)
                
        for block in self.blocks:
            new_figure_map[block.y][block.x] = block

        self.figure_map = new_figure_map

    
    def _create_map(self, h: int, w: int, value=None):
        map: List[List[Block | None]] = []

        for y in range(h):
            map.append([])
            for x in range(w):
                map[y].append(value)

        return map


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


