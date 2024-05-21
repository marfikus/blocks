
class Figure:
	def __init__(self, title: str = "", x: int = 0, y: int = 0):
		self.title = title
		self.x = x
		self.y = y
		self.width = 0
		self.height = 0
		self.blocks = []
		self.figure_map = [[]]

	def __str__(self):
		return f"Figure '{self.title}', x:{self.x}, y:{self.y}, width:{self.width}, height:{self.height}"

