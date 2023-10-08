class User():

	username: str

	password: str

	authentication_level: int

	def __init__(self, username: str, password: str, authentication_level: int = 0):
		self.username = str(username)
		self.password = str(password)
		self.authentication_level = authentication_level

	def __str__(self):
		return f"User: {self.username} Password: {self.password} Auth Level: {self.authentication_level}"
	
	# Check if user has access to a certain level
	def have_access(self, authentication_level: int):
		return self.authentication_level > authentication_level
	
	# Login user
	def login(self, password: str):
		if str(self.password) == password:
			return True
		return False
	

class Users():

	users: dict  # Users

	database: str

	# Constructor
	def __init__(self, database: str = "users.csv"):
		self.database = database

		# Load users from database
		self.load_users()
	
	# String representation
	def __str__(self):
		return f"Users: {list(self.users.values())}"
	
	# Add user to users
	def add_user(self, user: User):
		# Check if user exists
		if user.username in self.users:
			raise ValueError('User already exists')
		self.users[user.username] = user  # Add user to dictionary with username as key

		# Update database
		self.save_users()
	
	# Get user by username
	def get_user(self, username: str) -> User:
		return self.users.get(username, None)
	
	# Load users from database
	def load_users(self):
		self.users = {}

		# Check if file exists and create it if it doesn't
		try:
			open(self.database, 'r')
		except FileNotFoundError:
			open(self.database, 'w').close()

		# Read users from database
		with open(self.database, 'r') as file:
			for line in file:
				# Split line
				line = line.split(',')

				# Create user
				user = User(line[0], str
				(line[1]), int(line[2]))

				# Add user to users
				self.add_user(user)

	# Save users to database
	def save_users(self):
		with open(self.database, 'w') as file:
			for user in self.users.values():
				file.write(f"{user.username},{user.password},{user.authentication_level}\n")

	def remove_user(self, username: str):
		if username in self.users:
			del self.users[username]
			# Update database
			self.save_users()

	
	def login(self, username: str, password: int):
		user = self.get_user(username)
		if user and user.login(password):
			return user
		return None
	
	def have_access(self, username: str, authentication_level: int):
		user = self.get_user(username)
		if user:
			return user.have_access(authentication_level)
		return False
