import json
from time import sleep
from threading import Thread

from myFunc.pingpong import *
from myFunc.verify import *


def listen():
	# Create a TCP/IP socket to listen on
	listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# Bind the socket to the port
	listener_addr = (ip_addr, listen_port_no)
	print("Listener starting up on {} port {}".format(*listener_addr))
	logging.info(f"Listener thread started on {listener_addr}")
	listener.bind(listener_addr)
	# Listen for incoming connections
	listener.listen(5)

	while not exit_event.isSet():
		# Wait for a connection
		connection, client_address = listener.accept()
		logging.info(f"Connected to client {client_address}")
		t = Thread(target=listenerChild, args=(connection, client_address), name="ListenerChildThread")
		t.start()

def listenerChild(connection, client_address):
	global mutex
	global masterChain
	global chain_len
	try:
		with mutex:
			data = ""
			while True:
				instream = connection.recv(1024)
				if instream:
					data += instream.decode("utf-8")
				else:
					loaded_json = json.loads(data)
					tempChain = BlockChain()
					for b in loaded_json:
						new_block = Block(b["index"], b["timestamp"], b["data"], b["currHash"],
										  b["previousHash"])
						if tempChain.head is None:
							tempChain.head = new_block
						else:
							ptr = tempChain.head
							while ptr.next is not None:
								ptr = ptr.next
							ptr.next = new_block
					break
		v = verifyChain(tempChain)
		if v[0]:
			c = compareChain(tempChain)
			if c == -1:
				masterChain.head = tempChain.head
				logging.info(f"Master Chain updated. Previous length:{chain_len} New length:{v[1]}")
				chain_len = v[1]
	except socket.error:
		logging.exception("Exception occurred")
	finally:
		connection.close()

def heartbeat():
	global mutex
	global masterChain
	while not exit_event.isSet():
		sleep(5)
		logging.info("Sending heartbeat")
		i = 0
		nodeHold = -1
		failcounter = 0
		while i < len(nodeList):
			ip, port, node = nodeList[i]
			if node != nodeHold:
				nodeHold = node
				failcounter = 0
			with mutex:
				dest = (ip, int(port))
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				try:
					sock.connect(dest)
					logging.info(f"Sending heartbeat to {ip}:{port}")
					message = "["
					ptr = masterChain.head
					while ptr is not None:
						message += ptr.dump()
						if ptr.next is not None:
							message += ", "
						ptr = ptr.next
					message += "]"
					sock.sendall(message.encode())
					i += 1
				except (ConnectionRefusedError, TimeoutError) as e:
					logging.error(f"{e}")
					logging.info(f"Retry connection to {(ip, port)}. {failcounter} time(s)")
					failcounter += 1
					if failcounter == 3:
						failcounter = 0
						logging.info(f"Removing {nodeList[i]} from node list")
						del nodeList[i]
						continue
				finally:
					logging.info(f"Closing socket to {ip}:{port}")
					sock.close()
