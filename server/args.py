# Data classes
from dataclasses import dataclass
# Command line arguments
import argparse


#
# Represents command-line arguments for the server.
#
@dataclass
class CommandLineArgs:
	# IP address to use when opening the server.
	ip: str

	# Port to use when opening the server. Default is 25432.
	port: int = 25432

	# Timeout used to keep connections alive. Default is 10 seconds.
	timeout: int = 10

	# Password for the root user. Default is "root".
	root_username: str = "root"

	# Password for the root user. Default is "root".
	root_password: str = "0000"

	# Server log file to use. Default is "./server.log".
	log: str = "./server.log"


#
# Command line parser
#
def arg_parser() -> CommandLineArgs:
	parser = argparse.ArgumentParser(
		description = "Simple door auth server"
	)
	
	# Define command-line arguments
	parser.add_argument(
		"--ip",
		type = str,
		default = "127.0.0.1",
		help = "IP address to use when opening the server"
	)
	parser.add_argument(
		"--port",
		type = int,
		default = 25432,
		help = "Port to use when opening the server"
	)
	parser.add_argument(
		"--timeout",
		type = int,
		default = 10,
		help = "Timeout used to keep connections alive"
	)
	parser.add_argument(
		"--log",
		type = str,
		default = "./logs/server.log",
		help = "Server log file to use"
	)
	parser.add_argument(
		"--root-username",
		type = str,
		default = "root",
		help = "Username for the root user"
	)
	parser.add_argument(
		"--root-password",
		type = str,
		default = "0000",
		help = "Password for the root user"
	)

	# Fetch raw args
	args = parser.parse_args()

	# Creates server command line instance
	server_args = CommandLineArgs(
		ip = args.ip,
		port = args.port,
		timeout = args.timeout,
		log = args.log,
		root_username = args.root_username,
		root_password = args.root_password,
	)

	return server_args
