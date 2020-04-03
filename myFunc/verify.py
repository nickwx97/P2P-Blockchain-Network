from hashlib import sha256
from time import strptime

from config import *


def compareChain(tempChain):
	# return -1 if tempChain, 0 if equal, 1 if masterChain
	global mutex
	global timeformat
	ptr = masterChain.head
	temp = tempChain.head

	with mutex:
		while ptr and temp:

			mastertime = strptime(ptr.timestamp, timeformat)
			temptime = strptime(temp.timestamp, timeformat)

			if mastertime > temptime:
				return -1
			elif mastertime < temptime:
				return 1

			ptr = ptr.next
			temp = temp.next

	if ptr is None and temp is None:
		return 0
	elif ptr is not None and temp is None:
		return 1
	else:
		return -1


def verifyChain(tempChain):
	ptr = tempChain.head
	length = 0
	while ptr is not None:
		verification = sha256((str(ptr.previousHash) + str(ptr.index) + ptr.data + ptr.timestamp).rstrip().encode()).hexdigest()
		if ptr.currHash != verification:
			return False,
		else:
			length += 1
			ptr = ptr.next
	return True, length
