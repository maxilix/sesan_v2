import 		getpass
import 		os
import		threading
import		socket
import		time
import		json
from 		getpass 			import 		getpass


from 		c_geth				import 		Geth
#from		c_client 			import		Client
from		c_tracker 			import		Tracker
from		c_config 			import		Config

from 		c_console			import 		console

from		constants 			import *


class Node(threading.Thread):


	##################################################################################################
	#
	#	Constructor
	#
	def __init__(self):
		threading.Thread.__init__(self, daemon = True)

		self.status 		= S_INITIAL
		self.user 			= ( input("Username : " ) or DEFAULT_NODE_NAME, getpass("Password : ") or DEFAULT_NODE_PASSWORD)
		self.geth 			= None
		self.tracker 		= None


		# check if there is already a node instance
		for th in threading.enumerate():
			if "[thread]_{0}-node".format(self.user[0]) in th.name :
				console.error("node instance already executed for {0}".format(self.user[0]))
				self.status = S_ERROR
				return

		self.name = "[thread]_{0}-node".format(self.user[0])

		console.info("node initialized")
		return

	##################################################################################################
	#
	#	run associate thread
	#
	def run(self):
		if (self.status == S_ERROR):
			return

		self.geth = Geth(self.user)
		self.geth.start()
		while (self.geth.status == S_INITIAL):
			time.sleep(UPDATE_WAITING_TIME)
		if (self.geth.status != S_VALID):
			self.geth.stop()
			self.geth.join()
			self.geth = None
			console.error("node instance aborted")
			self.status == S_ERROR
			self.end()
			return


		#if   (NODE_TYPE == "tracker"):
		self.tracker = Tracker(self.user[0], self.geth.enodeS, self.geth.addressS, self.geth.eigentrust, self.geth.dealer)
		self.tracker.start()
		while (self.tracker.status == S_INITIAL):
			time.sleep(UPDATE_WAITING_TIME)
		if (self.tracker.status != S_VALID):
			self.tracker.stop()
			self.tracker.join()
			self.tracker = None
			console.warn("only geth is running")
		"""
		elif (NODE_TYPE == "client"):
			self.client = Client(self.user[0], self.geth.enodeString, self.geth.addressString)
			self.client.start()
			while (self.client.status == S_INITIAL):
				time.sleep(UPDATE_WAITING_TIME)
			if (self.client.status != S_VALID):
				self.client.stop()
				self.client.join()
				self.client = None
				console.error("node instance aborted")
				self.status == S_ERROR
				self.end()
				return

		else:
			console.warn("no NODE_TYPE specified")
			console.warn("only geth is running")
		"""

		self.status = S_VALID
		console.info("node is runing")

		# thread loop
		while (self.status == S_VALID):
			self.update()


		self.status = S_EXIT
		self.end()

		return

	##################################################################################################
	#
	#	final thread execution
	#
	def end(self):
		if (self.geth):
			self.geth.stop()
			self.geth.join()
		if (self.tracker):
			self.tracker.stop()
			self.tracker.join()
		"""
		if (self.client):
			self.client.stop()
			self.tracker.join()
		"""
		console.info("node closed")

	##################################################################################################
	#
	#	update
	#
	def update(self):
		time.sleep(UPDATE_WAITING_TIME)

		

		pass

	##################################################################################################
	#
	#	stop
	#
	def stop(self):
		self.status = S_EXIT

	##################################################################################################
