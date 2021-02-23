import 		threading
import 		web3
import 		json
import 		time

from 		c_console			import 		console

from		constants			import		*




class Spy(threading.Thread,):






	##################################################################################################
	#
	#	Constructor
	#
	def __init__(self, username, contractName, w3):
		threading.Thread.__init__(self, daemon = True)

		self.username 		= username
		self.contractName 	= contractName
		self.status 		= S_INITIAL

		# check if there is already a node instance
		for th in threading.enumerate():
			if "[thread]_{0}-{1}".format(self.username,self.contractName) in th.name :
				console.error("{1} already executed for {0}".format(self.username, self.contractName))
				self.status = S_ERROR
				return

		self.name = "[thread]_{0}-{1}".format(self.username, self.contractName)


		console.info("{0} initialized".format(self.contractName))
		return

	###########s#######################################################################################
	#
	#	run associate thread
	#
	def run(self):
		if (self.status == S_ERROR):
			return






		self.status = S_VALID
		console.info("{0} is runing".format(self.contractName))

		# thread loop
		while ("[exit]" not in self.name):
			time.sleep(WAITING_TIME)
			self.update()

		self.end()

		return

	##################################################################################################
	#
	#	final thread execution
	#
	def end(self):
		self.status = S_EXIT

		#del 

		console.info("{0} closed".format(self.contractName))

	##################################################################################################
	#
	#	update
	#
	def update(self):

		pass

	##################################################################################################
	#
	#	stop
	#
	def stop(self):
		self.status = S_EXIT
		self.name = "[exit]" + self.name

	##################################################################################################
