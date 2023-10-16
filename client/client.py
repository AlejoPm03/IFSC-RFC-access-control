# Operative System
import os
# Network
import socket
# Time
import time
# Utils
import logging
# Message
from message import Message, MessageType
# Arguments
from args import arg_parser, CommandLineArgs


# Flow control
APP_IS_RUNNING = True


#
# Client class
#
class Client():
	#
	# Properties
	#

	# Unique door identifier
	id: int

	# Server ip
	server_ip: str

	# Server port
	server_port: int

	# Response timeout in seconds
	timeout: int

	#
	# Constructor
	#
	def __init__(self, args: CommandLineArgs):
		self.id = args.id
		self.server_ip = args.server_ip
		self.server_port = args.server_port
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


	#
	# String representation
	#
	def __str__(self):
		return f"Client: {self.ip}:{self.port}"


	#
	# Run client
	#
	def run(self):
		logging.info(f"Client started on {self.server_ip}:{self.server_port} with id {self.id}")

		# Starts client loop
		while APP_IS_RUNNING:
			try:
				# Clear screen
				if os.name == "posix":
					os.system("clear")
				else:
					os.system("cls")

				# Login user
				self.login()

				# Delay 2 seconds
				time.sleep(2)
			except KeyboardInterrupt:
					break
			except:
				pass

		# Stop client
		self.stop()


	#
	# Try to login user
	#
	def login(self):
		# Ask action
		action = input("Login or Signup? (L/S): ").lower()

		# Fetch user data
		username = input("Username: ")
		password = input("Password: ")

		# Validate user data
		if not username or not password:
			print("Invalid username or password")
			return

		if action == "l":
			self.open_door(username, password)
		elif action == "s":
			self.register(username, password)


	#
	# Register a new user in the system
	#
	def register(self, username: str, password: str):
		# Ask for user to be registered
		username_to_register = input("Username to register: ")
		password_to_register = input("Password to register: ")

		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
			# Connect to server
			conn.connect((self.server_ip, self.server_port))

			# Send login message
			login_message = Message(self.id,
				MessageType.SIGNUP,
				username = username,
				password = password
			).send_and_receive(conn)

			# Check if authorized
			if not login_message.authorized:
				logging.warning("Unauthorized")
				return

			# Send signup message
			message = Message(self.id,
				MessageType.SIGNUP,
				username = username_to_register,
				password = password_to_register
			).send_and_receive(conn)

			# Handle message
			if message and message.type == MessageType.SIGNUP:
				# Check if authorized
				if message.authorized:
					logging.info("Register successful")
			else:
				logging.warning("Internal Error")


	#
	# Open door
	#
	def open_door(self, username: str, password: str) -> None:
		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
			# Connect to server
			conn.connect((self.server_ip, self.server_port))

			# Send login message
			message = Message(self.id,
				MessageType.LOGIN,
				username = username,
				password = password
			).send_and_receive(conn)

			# Handle message
			if message and message.type == MessageType.LOGIN:
				# Check if authorized
				if message.authorized:
					logging.info("Authorized")
					print("...................OPENING DOOR....................")
				else:
					logging.warning("Unauthorized")
			else:
				logging.warning("Internal Error")


	#
	# Perform action
	#
	def stop(self):
		logging.info("Client stopped")


# Run client
if __name__ == '__main__':
	# Parse command-line arguments
	args = arg_parser()

	# Create client
	client = Client(args)

	# Run client
	client.run()
