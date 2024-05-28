
from typing import List
from block import Block


class Figure:
	def __init__(self, title: str = "", x: int = 0, y: int = 0):
		self.title = title
		self.x = x
		self.y = y
		self.width = 0
		self.height = 0
		self.blocks: List[Block] = []
		self.figure_map: List[List[Block]] = [[]]


	def __str__(self):
		return f"Figure '{self.title}', x:{self.x}, y:{self.y}, width:{self.width}, height:{self.height}"


	def add_block(self, new_block: Block, x: int, y: int):
		for block in self.blocks:
			if block.x == x and block.y == y:
				print(f"{self.title}: busy cell!")
				return
			
		new_block.x = x
		new_block.y = y
		self.blocks.append(new_block)
		self._update_figure_size()
		self.update_figure_map()
		self.figure_map[x][y] = new_block


	def _update_figure_size(self):
		max_x: int = 0
		max_y: int = 0

		for block in self.blocks:
			if block.x > max_x: max_x = block.x
			if block.y > max_y: max_y = block.y

		self.width = max_x + 1
		self.height = max_y + 1


	def _update_figure_map(self):
		pass


