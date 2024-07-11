
from figure import Figure
from block import Block
from typing import List


class FigureL(Figure):
    n = 0
    
    def __init__(self):
        # width = 2
        # height = 3
        super().__init__(f"L_{FigureL.n}")
        FigureL.n += 1
        
        blocks: List[Block] = []
        for i in range(4):
            blocks.append(Block())
        
        self.add_block(blocks[0], 0, 0)
        self.add_block(blocks[1], 0, 1)
        self.add_block(blocks[2], 0, 2)
        self.add_block(blocks[3], 1, 2)
        
