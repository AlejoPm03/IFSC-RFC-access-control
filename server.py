import socket
import threading
import logging
from message import Message, MessageType
from user import User, Users
from door import Door, Doors


class Server():

	ip: str

	port: int

	users: Users

	doors: Doors

	# Constructor
	def __init__(self, ip: str, port: int, users_database: str = None, doors_database: str = None, enable_log: bool = True):
		self.users = Users(users_database)
		self.doors = Doors(doors_database)
		self.ip = ip
		self.port = port

		# Configure the root logger
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			handlers=[
				logging.StreamHandler(),
				logging.FileHandler('server.log')
			]
		)

	# String representation
	def __str__(self):
		return f"Server: {self.ip}:{self.port}"

	# Run server
	def run(self):
		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			# Bind socket
			s.bind((self.ip, self.port))

			# Listen for connections
			s.listen()
			
			logging.info(f"Server started on {self.ip}:{self.port}")

			# Accept connections
			while True:
				conn, addr = s.accept()

				# Set timeout
				conn.settimeout(60)

				logging.info(f"Connected to {addr}")

				# Create thread for connection
				threading.Thread(target=self.handle_connection, args=(conn, addr)).start()

	# Handle connection
	def handle_connection(self, conn: socket.socket, addr: tuple):
		
		message = Message.receive(conn)

		logging.info(f"Received message from {addr}: {message}")

		# Handle message
		if message.type == MessageType.LOGIN:
			self.login(conn, message)
			
		elif message.type == MessageType.SIGNUP:
			self.signup(conn, message)

		# Close connection
		conn.close()

	# Login
	def login(self, conn: socket.socket, message: Message):
		user = self.users.login(message.username, message.password)

		# Login user
		if not user:
			logging.warn(f"Login failed user {message.username} not found, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, False, message.username, message.password).send(conn)
			return False

		if self.doors.get_door(message.id).have_access(user.authentication_level):
			# Send authorized message
			logging.info(f"Login successful user {message.username}, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, True, message.username, message.password).send(conn)
			return True
		else:
			# Send unauthorized message
			logging.warn(f"Login failed user {message.username} does not have access to door {self.doors.get_door(message.id)}, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, False, message.username, message.password).send(conn)
			return False

	# Signup
	def signup(self, conn: socket.socket, message: Message):
		# First message is always login message
		# Check if user have permission to register users
		if not self.login(conn, message):
			logging.warn("Login failed")
			return
		
		# Receive signup message
		message = Message.receive(conn)
		
		# Check if user exists
		if self.users.get_user(message.username) != None:
			Message(message.id, MessageType.SIGNUP, False, message.username, message.password).send(conn)
			return

		# Create user
		user = User(message.username, message.password, self.doors.get_door(message.id).authentication_level)

		logging.info(f"Created user: {user}")

		# Add user to users
		self.users.add_user(user)

		# Send authorized message
		Message(message.id, MessageType.SIGNUP, True, message.username, message.password).send(conn)

	# Stop server
	def stop(self):
		pass

# Run server
if __name__ == "__main__":
	server = Server("127.0.0.1", 5429, "users.csv", "doors.csv")

	# Run server
	server.run()