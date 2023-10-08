import time
import socket
import struct

# Enums
from enum import Enum

# Message type
class MessageType(Enum):
	LOGIN = 0
	SIGNUP = 1

class Message():
	# Type of message
	# 0 - login
	# 1 - signup
	type: MessageType

	# Id
	id: int

	# Timestamp
	timestamp: int

	# Authorized
	authorized: bool

	# Username 50 chars
	username: str

	# Password 4 digits
	password: int

	# Constructor
	def __init__(self, id: int = 0, type: MessageType = MessageType.SIGNUP, authorized: bool = False, username: str = "guest", password: str = "0000", timestamp: int = None):
		
		# Validate type
		if not isinstance(type, MessageType):
			raise ValueError('Type must be MessageType')
		self.type = type
		
		# Validate id
		id = int(id)
		if (id < 0 or id > 15):
			raise ValueError('Id must be 4 bits')
		self.id = id

		# Validate authorized
		if not isinstance(authorized, bool):
			raise ValueError('Authorized must be bool')
		self.authorized = authorized

		# Update timestamp if not provided
		if timestamp == None:
			self.update_timestamp()
		else:
			self.timestamp = timestamp

		# Validate username		
		if len(username) > 50:
			raise ValueError('Username too long')
		self.username = username

		# Validate password
		if (int(password) < 0 or int(password) > 9999):
			raise ValueError('Password must be 4 digits')
		self.password = password

	# Update timestamp
	def update_timestamp(self):
		self.timestamp = int(time.time())
		
	# Serialize message to bytes
	def pack(self) -> bytes:
		# Type: 1bit
		# Id: 4bit
		# Authorized: 1bit
		# timestamp: long long
		# username: char[50]
		# password: char[4]

		# Ensure that type and id have the correct size
		type_bit = self.type.value & 0b1
		id_bits = self.id & 0b1111
		auth_bit = self.authorized & 0b1

		# Combine type and id into a single byte
		combined_byte = (type_bit << 5) | (id_bits << 1) | auth_bit

		# Pack the combined byte, timestamp, username, and password into binary format
		return struct.pack("Bq50s4s",
						combined_byte,
						self.timestamp,
						self.username.encode('utf-8'),
						str(self.password).encode('utf-8'))
	

	# Send message to socket
	def send(self, conn: socket.socket):
		# Send message
		self.update_timestamp()
		conn.send(self.pack())

	# Send message to socket and wait for response
	# Timeout in seconds
	def send_and_receive(self, conn: socket.socket, timeout: int = 10) -> 'Message':
		
		# Set a timeout
		conn.settimeout(timeout)

		# Send message
		self.send(conn)

		# Wait for response
		while True:
			
			# Receive message
			message = conn.recv(1024)

			# Check if message is valid
			if message:
				# Parse message
				message = Message.unpack(message)

				# Check if message is valid
				if message.id == self.id:
					return message
				
	# Receive message from socket with timeout
	# Timeout in seconds
	@staticmethod
	def receive(conn: socket.socket, timeout: int = 10) -> 'Message':
		
		# Set a timeout of 5 seconds
		conn.settimeout(timeout)

		while True:
			# Receive message
			message = conn.recv(1024)

			# Check if message is valid
			if message:
				# Parse message
				message = Message.unpack(message)

				return message

	# Deserialize bytes to message
	@staticmethod
	def unpack(data: bytes) -> 'Message':
		# Unpack the data
		combined_byte, timestamp, username, password = struct.unpack("Bq50s4s", data)

		# Extract type and id from combined byte
		type = MessageType((combined_byte >> 5) & 1)
		auth = bool(combined_byte & 1)
		id = (combined_byte >> 1) & 0b1111

		# Extract username and password from bytes
		username = username.decode('utf-8').rstrip('\x00')
		password = password.decode('utf-8')

		# Create message object
		message = Message(id, type, auth, username, password, timestamp)

		return message
	
	# Message length
	@staticmethod
	def length() -> int:
		return len(Message().pack())

	# String representation
	def __str__(self) -> str:
		return f'Message(type={self.type}, id={self.id}, authorized={self.authorized}, username={self.username}, password={self.password}, timestamp={time.ctime(self.timestamp)})'
