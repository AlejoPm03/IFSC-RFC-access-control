# Threads
import threading
# Network
import socket
# Utils
import logging
# Message
from message import Message, MessageType
# Arguments
from args import arg_parser, CommandLineArgs
# Models
from models.user import User
from models.door import Door


# Flow control
APP_IS_RUNNING = True

#
# Server class
#
class Server():
	#
	# Properties
	#

	# IP address
	ip: str

	# Port
	port: int

	# Timeout
	timeout: int

	#
	# Constructor
	#
	def __init__(self, args: CommandLineArgs):
		self.ip = args.ip
		self.port = args.port
		self.timeout = args.timeout

		# Configure the root logger
		logging.basicConfig(
			level = logging.INFO,
			format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			handlers = [
				logging.StreamHandler(),
				logging.FileHandler(args.log)
			]
		)

		# Inits root user or update it
		root_user = User(args.root_username, args.root_password, 10000000)
		root_user.save()


	#
	# String representation
	#
	def __str__(self):
		return f"Server: {self.ip}:{self.port}"


	#
	# Main server loop
	#
	def run(self):
		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			# Bind socket
			s.bind((self.ip, self.port))

			# Listen for connections
			s.listen()
			
			logging.info(f"Server started on {self.ip}:{self.port}")

			# Accept connections
			while APP_IS_RUNNING:
				try:
					conn, addr = s.accept()

					# Set timeout
					conn.settimeout(self.timeout)

					logging.info(f"Connected to {addr}")

					# Create thread for connection
					threading.Thread(
						target = self.handle_connection,
						args = (conn, addr)
					).start()
				except KeyboardInterrupt:
					break
				except:
					pass

			# Shutdown socket
			s.shutdown(socket.SHUT_RDWR)

			# Stop server
			self.stop()


	#
	# Handle connection
	#
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


	#
	# Login a user in the system
	#
	def login(self, conn: socket.socket, message: Message):
		# Searches for user
		user: User = User.objects().find_one(
			lambda user: user.username == message.username and user.login(message.password)
		)

		# Search for door
		door: Door = Door.objects().find_one(
			lambda door: door.id == message.id
		)

		# Login user
		if not user:
			logging.warning(f"Login failed user {message.username} not found, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, False, message.username, message.password).send(conn)
			return False

		# Check if door exists
		if not door:
			logging.warning(f"Login failed door {message.id} not found, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, False, message.username, message.password).send(conn)
			return False

		# Check if user can access door
		if door.have_access(user.authentication_level):
			# Send authorized message
			logging.info(f"Login successful user {user.username}, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, True, user.username, user.password).send(conn)
			return True
		else:
			# Send unauthorized message
			logging.warning(f"Login failed user {user.username} does not have access to door {door}, message id :{message.id}")
			Message(message.id, MessageType.LOGIN, False, user.username, user.password).send(conn)
			return False


	#
	# Login a user in the system
	#
	def signup(self, conn: socket.socket, message: Message):
		# First message is always login message
		# Check if user have permission to register users
		if not self.login(conn, message):
			logging.warning("Login failed")
			return

		# Receive signup message
		message = Message.receive(conn)

		# Tries to find user to be created
		new_user: User = User.objects().find_one(
			lambda user: user.username == message.username
		)

		# Check if user exists
		if new_user != None:
			logging.info(f"User already exists: {new_user}")
			Message(message.id, MessageType.SIGNUP, False, message.username, message.password).send(conn)
			return

		# Tries to find door
		door: Door = Door.objects().find_one(
			lambda door: door.id == message.id
		)

		if not door:
			logging.warning(f"Door {message.id} not found for registering user {message.username}")
			Message(message.id, MessageType.SIGNUP, False, message.username, message.password).send(conn)
			return

		# Create user
		new_user = User(
			message.username, message.password, door.authentication_level
		)
		new_user.save()

		logging.info(f"Created user: {new_user}")

		# Send authorized message
		Message(message.id, MessageType.SIGNUP, True, new_user.username, new_user.password).send(conn)

	#
	# Stop server
	#
	def stop(self):
		logging.info("Stopping server")


# Run server
if __name__ == '__main__':
	# Parse command-line arguments
	args = arg_parser()

	# Create server
	server = Server(args)

	# Run server
	server.run()
