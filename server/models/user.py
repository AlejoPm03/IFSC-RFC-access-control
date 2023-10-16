# Typing
from typing import Self
# Model
from database.model import Model

#
# User model
#
class User(Model):
	# Username string
	username: str

	# Password string
	password: str

	# Level that the user has access to
	authentication_level: int

	#
	# Constructor
	#
	def __init__(
		self,
		username: str,
		password: str,
		authentication_level: int = 0
	):
		# Inits
		self.username = str(username)
		self.password = str(password)
		self.authentication_level = int(authentication_level)

		# Inits super with primary
		super().__init__(
			lambda user: user.username == self.username
		)


	#
	# Parse one User from str line
	#
	@staticmethod
	def parse(line: str) -> Self:
		# Split line
		data = line.split(',')

		# Create user
		return User(data[0], data[1], data[2])


	#
	# Serializes one User to str
	#
	@staticmethod
	def serialize(user: Self) -> str:
		return f"{user.username},{user.password},{user.authentication_level}"


	#
	# String Representation of this obj
	#
	def __str__(self):
		return f"User: {self.username} Password: {self.password} Auth Level: {self.authentication_level}"


	#
	# Login user
	#
	def login(self, password: str) -> bool:
		return self.password == password
