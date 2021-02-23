 #from 	hashlib		import 	sha256
from 		datetime 	import 	datetime
#import 	threading
#import 	re

import 		tools

from		constants			import		*
#from 	constants 	import *


class Guest():

	def __init__(self, username):
		self.who 			= "{0}-newGuest".format(username)	# "username-nodekey" for console
		self.timestamp 		= tools.now() 						# timestamp from datetinme
		self.enodeB 		= b'' 								# enode in bytes : 64 nodekey + 4 ip + 2 port  (bytesorder = 'big')
		self.enodeS 		= "" 								# enode in string : "enode://973d81a284a7579d27164a7c2e..."
		self.addressB 		= b'' 								# address in bytes : 20 bytes
		self.addressS 		= "" 								# address in string : "0xea45041a6f49d1b4551861c9379fd7c475d22909"
		self.udpContact 	= ("",0) 							# tuple (str,int) : ("127.0.0.1", 1234)
		self.tpcContact 	= ("",0) 							# tuple (str,int) : ("127.0.0.1", 1234)

	def __del__(self):
		pass

	def update(self):

		self.enodeS = "enode://" + "".join("{0:02x}".format(x) for x in self.enodeB[:64]) + "@" + "".join("{0:d}.".format(x) for x in self.enodeB[64:68])[:-1] + ":" + str(int.from_bytes(self.enodeB[68:70], byteorder='big'))

		self.who = self.who.split('-')[0] + "-" + "".join("{0:02x}".format(x) for x in self.enodeB[:64])

		if (self.addressB != b''):
			self.addressS = "0x" + "".join("{0:02x}".format(x) for x in self.addressB)

		self.timestamp = tools.now()
		
		return True


	def ip(self):
		return "".join("{0:d}.".format(x) for x in self.enodeB[64:68])[:-1]

	def port(self,which):
		if   (which == "geth"):
			return int.from_bytes(self.enodeB[68:70], byteorder='big')
		elif (which == "udp"):
			return udpContact[1]
		elif (which == "tcp"):
			return tcpContact[1]
		else:
			console.error("wrong port specification")







	"""
	def process(contact, frame):
		self.timestamp = datetime.now()

		if (not self.enode)
			self.enode = frame[0:64]
			self.who = "{0}-{1:x}".format(self.username, int.from_bytes(self.enode, byteorder='big'))	
		else:
			if (self.enode != frame[0:64]):
				console.error("guest exist but enode doesn't match")
				return False

		self.ip = frame[64:68]
		if (bytes([int(contact[0].split('.')[x]) for x in range(4)]) != self.ip):
			console.error("guest's ip doesn't match")
			return False

		self.gethPort = frame[68:70]







	def check_enode(self):

		if (self.enode[:8] != "enode://"):
			console.warn("invalid enode : doesn't start with \"enode://\"")
			return False

		if (self.enode[136] != "@"):
			console.warn("invalid enode : 136th char must be '@'")
			return False

		if bool(re.compile(r'[^0-9a-f]').search(self.enode[8:136])):
			console.warn("invalid enode : public key must be 128-length hex string")
			return False

		if ([int(self.enode.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)] != self.ip):
			console.warn("invalid enode : ip doesn't match")
			return False

		# change thread name
		threading.currentThread().name = threading.currentThread().name.split('_')[0] + "_" + self.enode[8:136]
		return True


	def check_address(self):

		if (len(self.address) == 42 and self.address[:2] == "0x"):
			self.address = self.address[2:]
		else:
			console.warn("invalid address : 42-length address must be start with \"0x\"")
			return False

		if bool(re.compile(r'[^0-9a-f]').search(self.address)):
			console.warn("invalid address : address must be 40-length hex string")
			return False

		return True





	def recieve(self):
		cmd = self.connexion.recv(1)
		console.cc(str(cmd) + " opCode recieved")
		return cmd


	def init_connexion(self):
		self.connexion.settimeout(CC_TIMEOUT)
		try:
			# CC__START ################
			if (self.connexion.recv(1) != CC__START):
				console.warn("no CC__START opCode")
				self.close_connexion()
				return False
			console.cc("CC__START opCode OK")
			############################

			# CC__RECIEVE_ENODE ########
			if (self.connexion.recv(1) != CC__RECIEVE_ENODE):
				console.warn("no CC__RECIEVE_ENODE opCode")
				self.close_connexion()
				return False

			size = int.from_bytes(self.connexion.recv(CC_LEN_OF_SIZE), byteorder='big')
			if (size == 0):
				console.warn("enode's size must be nonzero")
				self.close_connexion()
				return False
			self.enode = self.connexion.recv(size).decode('UTF-8')
			if (self.check_enode() == False):
				self.close_connexion()
				return False
			console.cc("CC__RECIEVE_ENODE opCode OK")
			############################

			# CC__RECIEVE_ADDRESS ########
			if (self.connexion.recv(1) != CC__RECIEVE_ADDRESS):
				console.warn("no CC__RECIEVE_ADDRESS opCode")
				self.close_connexion()
				return False
			size = int.from_bytes(self.connexion.recv(CC_LEN_OF_SIZE), byteorder='big')
			if (size != 40 and size != 42):
				console.warn("size of address must be 40 or 42 (not a joke :D)")
				self.close_connexion()
				return False
			self.address = self.connexion.recv(size).decode('UTF-8')
			if (self.check_address() == False):
				self.close_connexion()
				return False
			console.cc("CC__RECIEVE_ADDRESS opCode OK")
			############################

			return True

		except socket.timeout:
			console.warn("connexion timeout")
			self.close_connexion()


	def close_connexion(self):
		self.connexion.close()
		console.info("connexion closed")
		threading.currentThread().name = "[exit]" + threading.currentThread().name
	"""