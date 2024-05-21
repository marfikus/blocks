
class Block:
	def __init__(self, tag: str = "", x: int = 0, y: int = 0):
		self.tag = tag
		self.x = x
		self.y = y

	def __str__(self):
		return f"{self.tag} {self.x} {self.y}"

