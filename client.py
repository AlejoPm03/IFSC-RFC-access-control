import socket
import logging
from message import Message, MessageType
from user import User

class Client():

	# Client id
	id: int

	# Server ip
	server_ip: str

	# Server port
	server_port: int

	# Id
	id: int

	# Response timeout in seconds
	timeout: int

	# Logged user
	user: User

	# Constructor
	def __init__(self, server_ip: str, server_port: int, timeout: int = 5):
		self.id = input("Enter door id:")
		self.server_ip = server_ip
		self.server_port = server_port
		self.timeout = timeout
		self.user = User("guest", "0000", -1)


		# Configure the root logger
		logging.basicConfig(
			level=logging.INFO,
			format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
			handlers=[
				logging.StreamHandler(),
				logging.FileHandler('client.log')
			]
		)
		

	# String representation
	def __str__(self):
		return f"Client: {self.ip}:{self.port}"
	
	# Run client
	def run(self):

		logging.info(f"Client started on {self.server_ip}:{self.server_port} with id {self.id}")

		while True:

			print("\n\nLogged as: " + self.user.username)
			print("What would you like to do?")
			print("1. Login")
			print("2. Register")
			print("3. Logout")
			print("4. Access")
			print("5. Exit")
			choice = input("Choice: ")

			try:
				if choice == "1":
					self.login()
				elif choice == "2":
					self.register()
				elif choice == "3":
					self.logout()
				elif choice == "4":
					self.access()
				elif choice == "5":
					exit()
			except Exception as e:
				logging.error(e)

	# Login user
	def login(self):

		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:

			# Connect to server
			conn.connect((self.server_ip, self.server_port))

			# Create user without authorization level
			user = User(input("Username: "), int(input("Password: ")), -1)

			# Send login message
			message = Message(self.id,
				MessageType.LOGIN,
				username = user.username,
				password = user.password
			).send_and_receive(conn)

			# Handle message
			if message and message.type == MessageType.LOGIN:
				# Check if authorized
				if message.authorized:
					logging.info("Login successful")
					self.user = user
				else:
					logging.warn("Login failed, server unauthorized user")
			else:
				logging.warn("Login failed, server sent invalid message")
	
	def register(self):

		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
			# Connect to server
			conn.connect((self.server_ip, self.server_port))

			# Send login message
			login_message = Message(self.id,
				MessageType.SIGNUP,
				username = self.user.username,
				password = self.user.password
			).send_and_receive(conn)

			# Check if authorized
			if not login_message.authorized:
				logging.warn("Signup failed, server unauthorized user")
				return
			
			# Ask the user for new user data
			user = User(input("Username: "), int(input("Password: ")), -1)

			# Send signup message
			message = Message(self.id,
				MessageType.SIGNUP,
				username = user.username,
				password = user.password
			).send_and_receive(conn)

			# Handle message
			if message and message.type == MessageType.SIGNUP:
				# Check if authorized
				if message.authorized:
					logging.info("Signup successful")
			else:
				logging.warn("Signup failed, server unauthorized user")

	# Logout user
	def logout(self):
		self.user = User("guest", "0000", -1)

	def access(self):

		# Create socket
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
			# Connect to server
			conn.connect((self.server_ip, self.server_port))

			# Send login message
			login_message = Message(self.id,
				MessageType.LOGIN,
				username = self.user.username,
				password = self.user.password
			).send_and_receive(conn)

			# Check if authorized
			if not login_message.authorized:
				logging.warn("Access failed, server unauthorized user")
				return
			
			logging.info("Access granted")

# Run client
if __name__ == '__main__':
	# Create client
	client = Client("127.0.0.1", 5429)

	# Run client
	client.run()