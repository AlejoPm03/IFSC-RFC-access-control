# Operating system
import os
# Typing
from typing import Callable, List, Any, Dict

#
# Default data directory
#
DEFAULT_DATA_DIRECTORY = "./data"

#
# Represents one database instance for one given table
#
class Database:
	# Data directory
	data_dir: str = DEFAULT_DATA_DIRECTORY

	# Current table name
	table: str

	# Read parser
	parse: Callable[ [ str ], Any ]

	# Store parser
	serialize: Callable[ [ str ], Any ]

	#
	# Constructor
	#
	def __init__(
		self,
		table: str,
		parse: Callable[ [ str ], Any ],
		serialize: Callable[ [ str ], Any ]
	) -> None:
		# Init local copies
		self.table = table
		self.parse = parse
		self.serialize = serialize

		# Checks if the file exists
		if not os.path.exists(self.data_dir + "/" + self.table + ".csv"):
			# Creates the file
			with open(self.data_dir + "/" + self.table + ".csv", 'w+') as file:
				file.write("")


	#
	# Read the entire database and converts to classes instances
	#
	def read(self) -> List[ Any ]:
		# Records buffer
		buffer: List[ Any ] = []
		# Open Database file and converts data
		with open(self.data_dir + "/" + self.table + ".csv", 'r') as file:
			# Iterate all lines
			for line in file:
				buffer.append(self.parse(line))

		return buffer


	#
	# Stores a list of entities in the database, override all data in database
	# file
	#
	def store(self, records: List[ Any ]) -> None:
		# Open Database file and saves data
		with open(self.data_dir + "/" + self.table + ".csv", 'w+') as file:
			for record in records:
				file.write(self.serialize(record) + "\n")


	#
	# Searches for one record in the database
	#
	def find(self, predicative: Callable[ [ Any ], bool ] = lambda x: True) -> List[ Any ]:
		# Fetches all records
		records = self.read()

		# Result buffer
		buffer: List[ Any ] = []

		# Linear search
		for record in records:
			if predicative(record):
				buffer.append(record)

		return buffer


	#
	# Searches for one record in the database
	#
	def find_one(self, predicative: Callable[ [ Any ], bool ]) -> Any:
		# Fetches all records
		records = self.read()

		# Linear search with stop
		for record in records:
			if predicative(record):
				return record

		return None


	#
	# Inserts one record in database
	#
	def insert(self, record: Any) -> None:
		# Open Database file and saves data
		with open(self.data_dir + "/" + self.table + ".csv", 'a+') as file:
			file.write(self.serialize(record) + "\n")


	#
	# Update records in database
	#
	def update(
		self, predicative: Callable[ [ Any ], bool ], data: Dict, n: int = 1
	) -> int:
		# Updated counter
		updated = 0

		# Generates copy
		records = self.read()

		# Iterate all lines
		for record in records:
			# If should update
			if predicative(record):
				# Update all keys
				for i in data.items():
					setattr(record, i[0], i[1])
				updated += 1

			# Stops when reach update limit
			if updated >= n:
				break

		# Saves copy
		self.store(records)

		return updated


	#
	# Remove records in database
	#
	def remove(
		self, predicative: Callable[ [ Any ], bool ], n: int = 1
	) -> int:
		# Updated counter
		removed = 0

		# Save buffer
		save_buffer: List[ Any ] = []
		# Generates copy
		records = self.read()

		# Iterate all lines
		for record in records:
			# If should update
			if predicative(record) and removed < n:
				removed += 1
			else:
				save_buffer.append(record)

		# Saves copy
		self.store(save_buffer)

		return removed
