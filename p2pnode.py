from threading import Thread

from myFunc.conn import *
from myFunc.utils import *

from webserver.server import *


def main():
	genesis = Thread(target=produce, args=(str("genesis block"),), name="GenesisThread")
	genesis.start()
	genesis.join()
	serve_pong = Thread(target=pong, daemon=True, name="PongThread")
	serve_pong.start()
	listener = Thread(target=listen, daemon=True, name="ListenerThread")
	listener.start()
	pinger = Thread(target=ping, name="PingThread")
	pinger.start()
	pinger.join()
	heart = Thread(target=heartbeat, daemon=True, name="HeartbeatThread")
	heart.start()

	web = Thread(target=webServerRun, daemon=True, name="WebServerThread")
	web.start()

	print("Setup complete!")

	while not exit_event.isSet():
		data = input("Type nodes to see nodes & exit to quit:")
		if data == "exit":
			exit_event.set()
		elif data == "nodes":
			print(nodeList)
		elif data == "dump":
			print(masterChain.dumpAll())
		else:
			producer = Thread(target=produce, args=(str(data),), name="ProducerThread")
			producer.start()


if __name__ == '__main__':
	logging.info('Main thread started')
	main()
