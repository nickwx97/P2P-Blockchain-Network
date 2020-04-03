import socket

from config import *


def pong():
	local = ("", pong_port)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.bind(local)
	print(f"Pong server up and listening on {local}")
	logging.info(f"Pong thread started on {local}")
	while not exit_event.isSet():
		bytesAddressPair = sock.recvfrom(1024)
		message = bytesAddressPair[0].decode("utf-8").split(",")
		logging.info(f"Recieved ping from {bytesAddressPair[1]}")
		if message[0] == "ping":
			address = bytesAddressPair[1]
			ipPortCheck = [(i[0], i[1]) for i in nodeList]
			if address[0] == ip_addr:
				continue
			elif (address[0], message[1]) not in ipPortCheck:
				nodeList.append((address[0], message[1], len(nodeList)))
			message = str(listen_port_no)
			logging.info(f"Sent pong to {address}")
			sock.sendto(message.encode(), address)


def ping():
	print("Probing for nodes (max reties 5)...")
	logging.info("Ping Thread started")
	dest = (broadcast_addr, pong_port)
	sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	message = "ping," + str(listen_port_no)
	sock.sendto(message.encode(), dest)
	logging.info(f"Ping sent to {dest}")
	sock.settimeout(1)
	tries = 0
	while tries < 5:
		try:
			reply = sock.recvfrom(1024)
			logging.info(f"Reply {tries+1} received: {reply}")
			message = reply[0].decode("utf-8")
			address = reply[1][0]
			nodeList.append((address, message, len(nodeList)))
			tries = 0
		except socket.timeout as e:
			print(e, ": Attempt #", tries + 1, sep="")
			tries += 1
