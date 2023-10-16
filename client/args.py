# Data classes
from dataclasses import dataclass
# Command line arguments
import argparse


#
# Represents command-line arguments for the client.
#
@dataclass
class CommandLineArgs:
	# ID of this port
	id: int

	# IP of the server to connect
	server_ip: str

	# IP of the server to connect
	server_port: int = 25432

	# Timeout in seconds when trying to communicate with the server
	timeout: int = 10

	# Client log file to use
	log: str = "./logs/client.log"


#
# Command line parser
#
def arg_parser() -> CommandLineArgs:
	parser = argparse.ArgumentParser(
		description = "Simple door auth client"
	)
	
	# Define command-line arguments
	parser.add_argument(
		"--id",
		type = int,
		required = True,
		help = "ID of this port"
	)
	parser.add_argument(
		"--server-ip",
		type = str,
		default = "127.0.0.1",
		help = "IP of the server to connect"
	)
	parser.add_argument(
		"--server-port",
		type = int,
		default = 25432,
		help = "IP of the server to connect"
	)
	parser.add_argument(
		"--timeout",
		type = int,
		default = 10,
		help = "Timeout in seconds when trying to communicate with the server"
	)
	parser.add_argument(
		"--log",
		type = str,
		default = "./logs/client.log",
		help = "Client log file to use"
	)

	# Fetch raw args
	args = parser.parse_args()

	# Creates client command line instance
	client_args = CommandLineArgs(
		id = args.id,
		server_ip = args.server_ip,
		server_port = args.server_port,
		timeout = args.timeout,
		log = args.log
	)

	return client_args
