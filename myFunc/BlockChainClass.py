class Block:
	def __init__(self, index: int, timestamp: str, data: str, currHash: str, previousHash: str):
		self.index = index
		self.timestamp = timestamp
		self.data = str(data)
		self.currHash = currHash
		self.previousHash = previousHash
		self.next = None

	def dump(self):
		return "{\"index\" : " + str(self.index) + ", \"timestamp\": \"" + str(self.timestamp) + \
			   "\", \"data\": \"" + str(self.data) + "\", \"currHash\": \"" + str(
			self.currHash) + "\", \"previousHash\": \"" + str(self.previousHash) + "\"}"


class BlockChain:
	def __init__(self):
		self.head = None

	def dumpAll(self):
		ptr = self.head
		out = "["
		while ptr is not None:
			out += ptr.dump()
			if ptr.next is not None:
				out += ","
			ptr = ptr.next
		out += "]"
		return out
