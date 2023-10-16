# Typing
from typing import Self
# Model
from database.model import Model

#
# Door model
#
class Door(Model):
	# Unique Identifier of this door
	id: int

	# Authentication level required by this door
	authentication_level: int

	#
	# Constructor
	#
	def __init__(self, id: int, authentication_level: int = 0):
		# Inits
		self.id = int(id)
		self.authentication_level = int(authentication_level)

		# Inits super with primary
		super().__init__(
			lambda door: door.id == self.id
		)


	#
	# Parse one Door from str line
	#
	@staticmethod
	def parse(line: str) -> Self:
		# Split line
		data = line.split(',')

		# Create user
		return Door(data[0], data[1])


	#
	# Serializes one Door to str
	#
	@staticmethod
	def serialize(door: Self) -> str:
		return f"{door.id},{door.authentication_level}"


	#
	# String Representation of this obj
	#
	def __str__(self):
		return f"Door: {self.id} Auth Level: {self.authentication_level}"


	#
	# Check if user has access to a certain level
	#
	def have_access(self, user_authentication_level: int):
		return (self.authentication_level <= user_authentication_level)
