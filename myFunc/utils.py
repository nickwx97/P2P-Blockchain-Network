from hashlib import sha256
from time import localtime, strftime

from config import *


def produce(data):
	global mutex
	global masterChain
	global chain_len
	with mutex:
		logging.info("Producer Thread started")
		t = localtime()
		current_time = strftime(timeformat, t)
		if masterChain.head is not None:
			ptr = masterChain.head
			while ptr.next is not None:
				ptr = ptr.next
			new_block = Block(ptr.index + 1, current_time, data, hashchain(ptr.currHash, ptr.index + 1, data, current_time),
							  ptr.currHash)
			ptr.next = new_block
			chain_len = new_block.index + 1
		else:
			new_block = Block(0, current_time, data, hashchain(0, 0, data, current_time), str(0))
			masterChain.head = new_block
			chain_len = 1
		logging.info(f"Added new block to chain. New length:{chain_len}")
	updateFile()


def hashchain(previousHash, index, data, time):
	return sha256((str(previousHash) + str(index) + data + str(time)).rstrip().encode()).hexdigest()

def updateFile():
	with mutex:
		with open("webserver/chain.json", "w+") as f:
			f.write(masterChain.dumpAll())
			f.close()