
import csv
import os

class Door():

	id: int

	authentication_level: int

	# Constructor
	def __init__(self, id: int, authentication_level: int = 0):
		self.id = id
		self.authentication_level = authentication_level

	# String representation
	def __str__(self):
		return f"Door: {self.id} Auth Level: {self.authentication_level}"
	
	# Check if user has access to a certain level
	def have_access(self, user_authentication_level: int):
		return (self.authentication_level < user_authentication_level)
	
class Doors():

	doors: dict

	database: str

	# Constructor
	def __init__(self, database: str = "doors.csv"):
		self.database = database

		# Load doors from database
		self.load()

	# String representation
	def __str__(self):
		return f"Doors: {list(self.doors.values())}"  # Changed to display values of the dict
	
	# Add door to doors
	def add_door(self, door: Door):
		# Check if door exists
		if door.id in self.doors:
			raise ValueError('Door already exists')
		self.doors[door.id] = door  # Add door to dictionary with id as key

	# Get door by id
	def get_door(self, id: int) -> Door:
		return self.doors.get(id, None)
	
	# Load doors from database
	def load(self):
		self.doors = {}

		# Check if file exists and create it if it doesn't
		if not os.path.exists(self.database):
			with open(self.database, 'w', newline='') as file:
				writer = csv.writer(file)
				writer.writerow(["id", "authentication_level"])
			return

		# Load doors from database
		with open(self.database, 'r') as file:
			reader = csv.reader(file)
			for row in reader:
				self.add_door(Door(int(row[0]), int(row[1])))

	# Save doors to database
	def save(self):
		# Save doors to database
		with open(self.database, 'w', newline='') as file:
			writer = csv.writer(file)
			for door in self.doors.values():
				writer.writerow([door.id, door.authentication_level])

