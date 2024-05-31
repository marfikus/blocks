
class Block:
	def __init__(self, tag: str = ""):
		self.tag = tag
		self.x = 0
		self.y = 0

	def __str__(self):
		return f"Block '{self.tag}', x:{self.x}, y:{self.y}"

