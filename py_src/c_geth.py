import 		time
import 		datetime
import 		os
import		subprocess
import 		threading
import 		psutil
import 		json
from		web3				import		Web3, IPCProvider
from		web3.middleware		import		geth_poa_middleware



from 		c_console			import 		console
import 		tools

from		constants			import		*



"""
def enode_to_bytes(enodeString):
	bEnode = int(enodeString.split('@')[0][8:],16).to_bytes(64, byteorder='big')
	bIp = bytes([int(enodeString.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)])
	bPort = int(enodeString.split('@')[1].split(':')[1]).to_bytes(2, byteorder='big')
	return (bEnode, bIp, bPort)


def bytes_to_enode(bEnode, bIp, bPort):
	r = "enode://"
	r+= "{0:x}".format(int.from_bytes(bEnode, byteorder='big'))
	r+= "@"
	for i in bIp:
		r+= str(i)
		r+= "."
	r = r[:-1] + ":"
	r+= str(int.from_bytes(bPort, byteorder='big'))
	return r
"""


class Geth(threading.Thread):


	##################################################################################################
	#
	#	Constructor
	#
	def __init__(self, user):
		threading.Thread.__init__(self, daemon = True)

		self.status 			= S_INITIAL
		self.pid 				= 0
		self.user 				= user
		self.log 				= None
		self.proc 				= None

		self.enodeS 			= ""
		self.addressS 			= ""

		self.guestEnodeS 		= []

		self.eigentrust			= None
		self.eigentrustEvents 	= None
		self.dealer				= None
		self.dealerEvents 		= None


		# check if there is already a node instance
		for th in threading.enumerate():
			if "[thread]_{0}-geth".format(self.user[0]) in th.name :
				console.error("geth instance already executed for {0}".format(self.user[0]))
				self.status = S_ERROR
				return

		self.name = "[thread]_{0}-geth".format(self.user[0])

		console.info("geth initialized")
		return

	##################################################################################################
	#
	#	run associate thread
	#
	def run(self):
		if (self.status == S_ERROR):
			self.end()
			return

		# check if the eth_username folder is initialized
		if not os.path.exists("{0}/eth_{1}".format(ROOT, self.user[0])):
			console.error("eth_{0} folder not initialized".format(self.user[0]))
			self.status = S_ERROR
			self.end()
			return			

		# run geth subprocess
		if not self.__run_geth_subprocess():
			self.status = S_ERROR
			self.end()
			return
		# connect to geth client with IPC file
		if not self.__IPC_connection():
			self.status = S_ERROR
			self.end()
			return

		# check valid coinbase and user/password and set defaultAccount
		if not self.__check_coinbase():
			self.status = S_ERROR
			self.end()
			return
		self.enodeS 	= self.w3.geth.admin.node_info()["enode"]
		self.addressS 	= self.w3.eth.defaultAccount

		# load eigentrust contract
		self.__load_eigentrust()

		# load dealer contract
		self.__load_dealer()




		self.status = S_VALID
		console.info("geth is running")

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

		if (self.proc):
			if (self.proc.poll() == None):
				self.proc.terminate()
				self.proc.wait()
				console.info("geth subprocess terminated")
			else:
				console.warn("geth subprocess already terminate with return code {0}".format(self.proc.poll()))

		console.info("geth closed")

	##################################################################################################
	#
	#	update
	#
	def update(self):
		time.sleep(UPDATE_WAITING_TIME)


		if self.guestEnodeS != []:
			pass






		who = "{0}-eigenTrust".format(self.user[0])
		# NewUser event
		news = self.eigentrustEvents["NewUser"].get_new_entries()
		for e in news:
			console.print("{0} : {1} added".format(e["args"]["index"],e["args"]["user"]) , who = who)

		# Vote event
		news = self.eigentrustEvents["Vote"].get_new_entries()
		for e in news:
			if (e["args"]["vote"]):
				console.print("{0} vote for {1}".format(e["args"]["from"],e["args"]["to"]) , who = who)
			else:
				console.print("{0} vote against {1}".format(e["args"]["from"],e["args"]["to"]) , who = who)

	##################################################################################################
	#
	#	stop
	#
	def stop(self):
		self.status = S_EXIT

	##################################################################################################




	def __run_geth_subprocess(self):
		

		port = tools.next_free_port()
		cmdlist = ["geth", "--datadir", "{0}/eth_{1}/".format(ROOT, self.user[0]), "--networkid", str(GETH_NETWORK_ID), "--port", str(port)] + GETH_FLAGS
		

		with open("{0}/eth_{1}/{2}".format(ROOT, self.user[0], GETH_LOG_FILENAME),'w') as self.log:
			self.proc = subprocess.Popen(cmdlist, stdin = None, stdout = None, stderr = self.log, shell = False)


		time.sleep(UPDATE_WAITING_TIME)


		if (self.proc.poll() != None):
			console.error("failed to run geth subprocess, return code {0}".format(self.proc.poll()))
			return 

		console.info("geth subprocess is renning on {0}".format(port))
		return True

	def __IPC_connection(self):
		console.info("waiting IPC connection ...")
		while not os.path.exists("./eth_{0}/geth.ipc".format(self.user[0])):
			time.sleep(UPDATE_WAITING_TIME)

		# need set provider in local variable to use clique methode
		provider = Web3.IPCProvider("./eth_{0}/geth.ipc".format(self.user[0]))
		self.w3 = Web3(provider)
		self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
		if (self.w3.isConnected()):
			console.info("IPC connection successful to {0} geth subprocess".format(self.user[0]))
			return True
		else:
			console.error("IPC connection failed")
			return False

	def __check_coinbase(self):
		try:
			self.w3.eth.defaultAccount = self.w3.eth.coinbase
		except ValueError:
			console.error("coinbase not initialized")
			return False

		console.info("{0} setted to default account".format(self.w3.eth.coinbase))

		try:
			self.unlock_coinbase(1)
		except ValueError:
			console.error("wrong password")
			return False

		self.lock_coinbase()
		return True

	def __load_eigentrust(self):
		try:
			with open("{0}/.{1}.json".format(ROOT,GETH_EIGENTRUST_NAME),'r') as fd:
				cfg = json.load(fd)

			self.eigentrust = self.w3.eth.contract(address = cfg["address"], abi = cfg["abi"])

			self.eigentrustEvents = dict()
			self.eigentrustEvents["NewUser"] = self.eigentrust.events.NewUser.createFilter(fromBlock=0)
			self.eigentrustEvents["Vote"] = self.eigentrust.events.Vote.createFilter(fromBlock=0)

			console.info("eigentrust contract loaded")
			return True
		except:
			console.warn("failed to load eigentrust contract")
			return False

	def __load_dealer(self):
		try:
			with open("{0}/.{1}.json".format(ROOT,GETH_DEALER_NAME),'r') as fd:
				cfg = json.load(fd)

			self.dealer = self.w3.eth.contract(address = cfg["address"], abi = cfg["abi"])
			console.info("dealer contract loaded")
			return True
		except:
			console.warn("failed to load dealer contract")
			return False


	##################################################################################################
	#
	#	lock and unlock account fonction
	#
	def unlock_coinbase(self, secondes):
		self.w3.geth.personal.unlock_account(self.w3.eth.defaultAccount,self.user[1],secondes)
		console.info("coinbase account unlocked")

	def lock_coinbase(self):
		self.w3.geth.personal.lock_account(self.w3.eth.defaultAccount)
		console.info("coinbase account locked")
	##################################################################################################

	##################################################################################################
	#
	#	peer connexion
	#
	def add_peer(self, enodeS):
		try:
			self.w3.geth.admin.add_peer(enodeS)

		except:
			pass

	def lock_coinbase(self):
		self.w3.geth.personal.lock_account(self.w3.eth.defaultAccount)
		console.info("coinbase account locked")
	##################################################################################################


	"""
	##################################################################################################
	# clique engine methodes
	#
	def clique_get_period():
		try:
			return clique_get_period.period
		except:
			genesidFile = open("./" + GENESIS_FILENAME , 'r')
			genesisDict = json.load(genesidFile)
			clique_get_period.period = genesisDict["config"]["clique"]["period"]
			genesidFile.close()
			return clique_get_period.period

	def clique_get_signers():
		response = provider.make_request(method = "clique_getSigners", params = [])
		if ("error" in response.keys()):
			print(response)
			raise NameError("Bad RPC request")
		return response["result"]

	def clique_get_proposals():
		response = provider.make_request(method = "clique_proposals", params = [])
		if ("error" in response.keys()):
			print(response)
			raise NameError("Bad RPC request")
		return response["result"]

	def clique_propose(address,vote):
		if (address[:2] != "0x" or not tools.w3.isAddress(address)):
			console(LOG_FLAG_WARN, "clique engine need valid address, propose not set")
			return False
		if (type(vote)!=bool):
			console(LOG_FLAG_WARN, "clique engine need boolean vote, propose not set")
			return False

		response = provider.make_request(method = "clique_propose", params = [address,vote])
		if ("error" in response.keys()):
			print(response)
			raise NameError("Bad RPC request")
		return (response["result"] == None and clique_get_proposals()[address] == vote)

	def clique_discard(address):
		if (address[:2] != "0x" or not tools.w3.isAddress(address)):
			console(LOG_FLAG_WARN, "clique engine need valid address, discard not set")
			return False

		response = provider.make_request(method = "clique_discard", params = [address])
		if ("error" in response.keys()):
			print(response)
			raise NameError("Bad RPC request")
		return (response["result"] == None and address not in clique_get_proposals())

	##################################################################################################
	"""
