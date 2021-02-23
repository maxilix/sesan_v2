import 		time
import 		datetime
import 		os
import 		re
import		subprocess
import 		threading
import 		json
import 		socket

from 		c_console			import 		console

from		constants			import		*


def now():
	return datetime.datetime.now()


def is_hex_string(s):
	for c in s:
		if c not in "0123456789abcdefABCDEF":
			return False
	return True



def next_free_port():
	port = PORT_RANGE_START
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(('', port))
			s.close()
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.bind(('', port))
			s.close()
			break
		except:
			port += 1
			continue
	return port



def check_enode(enodeString):
	if (enodeString[:8] != "enode://"):
		console.error("invalid enode : doesn't start with \"enode://\"")
		return False

	if (enodeString[136] != "@"):
		console.error("invalid enode : 136th char must be '@'")
		return False

	if not is_hex_string(enodeString[8:136]):
		console.error("invalid enode : public key must be 128-length hex string")
		return False

	#if ([int(self.enode.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)] != self.ip):
	#	console.error("invalid enode : ip doesn't match")
	#	return False

	return True



def check_address(addressString):
	if (len(addressString) == 42 and addressString[:2] == "0x"):
		addressString = addressString[2:]
	else:
		console.error("invalid address : 42-length address must be start with \"0x\"")
		return False

	if not (len(addressString) == 40 and is_hex_string(addressString)):
		console.error("invalid address : address must be 40-length hex string")
		return False

	return True

