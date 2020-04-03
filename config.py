from threading import Lock, Event
import logging

from myFunc.BlockChainClass import *

# HOST IP & BROADCAST
ip_addr = '192.168.139.1'
broadcast_addr = '192.168.139.255'
# PORT NUMBERS
listen_port_no = 10001
pong_port = 20000
# TIME FORMAT
timeformat = "%d-%m-%Y %H:%M:%S"
# DECLARE SHARED OTHER VARIABLES
masterChain = BlockChain()
chain_len = 0
mutex = Lock()
nodeList = []  # ip_addr, listen_port_no, node_id
exit_event = Event()
logging.basicConfig(format='%(asctime)s\t%(levelname)s : %(message)s -> %(threadName)s', level=logging.DEBUG,
						filename="log/p2p.log", filemode="w")