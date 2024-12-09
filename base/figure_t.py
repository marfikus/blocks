
from .figure import Figure
from .block import Block
from typing import List


class FigureT(Figure):
    n = 0
    
    def __init__(self):
        # width = 3
        # height = 2
        super().__init__(f"T_{FigureT.n}")
        FigureT.n += 1
        
        blocks: List[Block] = []
        for i in range(4):
            blocks.append(Block())
        
        self.add_block(blocks[0], 1, 0)
        self.add_block(blocks[1], 0, 1)
        self.add_block(blocks[2], 1, 1)
        self.add_block(blocks[3], 2, 1)
        
