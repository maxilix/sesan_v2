#!/usr/bin/python3

import 		threading
import 		time

from 		c_node 		import 		Node
from 		c_console	import 		console


from 		tools 		import 		*
from 		constants 	import 		*




def nodes():
	r = []
	for var in globals().copy():
		if isinstance(globals()[var], Node):
			r.append(globals()[var])
	return r


def end():
	for node in nodes():
			node.stop()
	for node in nodes():
			node.join()

	global console
	del console

	# fowarding to standard exit function in constants.py
	time.sleep(1)
	exit()



def clear():
	for var in globals():
		if isinstance(globals()[var], Node):
			if (not globals()[var].isAlive()):
				del globals()[var]


def new():
	tmp = Node()
	globals()["{0}Node".format(tmp.user[0])] = tmp
	globals()["{0}Node".format(tmp.user[0])].start()
	time.sleep(1)





print()
print(get_public_ip())
print("Welcome to sesan_v2")
print()
print("- Use help() to see informations")
print("- Use 'tail -f ./{0}' in for log info".format(LOG_FILENAME))
print()


new()
time.sleep(1)



