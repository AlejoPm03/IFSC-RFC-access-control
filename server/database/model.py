# Database
from .db import Database
# Typing
from typing import Callable, List, Any


#
# Defines operations in a given table
#
class ModelOperator:
	# Database instance
	__db__: Database

	#
	# Constructor
	#
	def __init__(self, db: Database) -> None:
		# Fetches database details
		self.__db__ = db

	#
	# Read the entire database and converts to classes instances
	#
	def read(self) -> List[ Any ]:
		return self.__db__.read()

	#
	# Stores a list of entities in the database, override all data in database
	# file
	#
	def store(self, records: List[ Any ]) -> None:
		self.__db__.store(records)

	#
	# Searches for one record in the database
	#
	def find(self, predicative: Callable[ [ Any ], bool ] = lambda x: True) -> List[ Any ]:
		return self.__db__.find(predicative)

	#
	# Searches for one record in the database
	#
	def find_one(self, predicative: Callable[ [ Any ], bool ]) -> Any:
		return self.__db__.find_one(predicative)

	#
	# Inserts one record in database
	#
	def insert(self, record: Any) -> None:
		self.__db__.insert(record)

	#
	# Update records in database
	#
	def update(self, predicative: Callable[ [ Any ], bool ], record: Any) -> None:
		self.__db__.update(predicative, record)

	#
	# Remove records in database
	#
	def remove(self, predicative: Callable[ [ Any ], bool ]) -> None:
		self.__db__.remove(predicative)


#
# Represents one database model
#
class Model:
	# Primary key
	primary: Callable[ [Any], bool ]

	# Database instance
	__db__: Database

	#
	# Returns the name of the child class
	#
	@classmethod
	def __child_name__(cls) -> str:
		return cls.__name__


	#
	# Returns the parse function of the child class
	#
	@classmethod
	def __get_parse__(cls):
		return cls.parse


	#
	# Returns the serialize function of the child class
	#
	@classmethod
	def __get_serialize__(cls):
		return cls.serialize

	#
	# Get objects operator
	#
	@classmethod
	def objects(cls) -> ModelOperator:
		# Fetches database details
		db = Database(
			cls.__child_name__().lower(),
			cls.__get_parse__(),
			cls.__get_serialize__()
		)
		return ModelOperator(db)

	#
	# Constructor
	#
	def __init__(self, primary: Callable[ [Any], bool ]) -> None:
		# Fetches database details
		self.__db__ = Database(
			self.__child_name__().lower(),
			self.__get_parse__(),
			self.__get_serialize__()
		)

		# Saves primary predicate
		self.primary = primary


	#
	# Inserts this instance in database
	#
	def save(self) -> None:
		instance = self.__db__.find_one(self.primary)

		# If already exists update
		if instance:
			self.__db__.update(self.primary, self.__dict__)
		else:
			self.__db__.insert(self)


	#
	# Delete this object from database
	#
	def delete(self) -> None:
		self.__db__.remove(self.primary)
