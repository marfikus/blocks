
class Block:
	def __init__(self, tag: str, posX: int = 0, posY: int = 0):
		self.tag = tag
		self.posX = posX
		self.posY = posY

	def __str__(self):
		return f"{self.tag} {self.posX} {self.posY}"

