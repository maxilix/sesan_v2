def final_exit():
	exit()


#################################   DEBUG   #####################
DEFAULT_NODE_NAME					= "marie"					#
DEFAULT_NODE_PASSWORD 				= "marie"					#
CONTRACT_STORAGE_FILENAME			= "strorage.sol"			#
#################################################################



#################################   GENESIS   ###################
DEFAULT_GENESIS_FILENAME 			= "sesan_v2_genesis.json" 	#
DEFAULT_CHAIN_ID 					= 1222
DEFAULT_CHAIN_PERIOD 				= 30

#################################################################



#################################   SYSTEM   ####################
ROOT 								= "."						#
CONTRACT_SOURCES_FOLDER				= "sol_src" 				#
PYTHON_SOURCES_FOLDER				= "py_src" 					#
																#
CONFIGURATION_FILENAME				= ".conf.json"				#
LOG_FILENAME 						= ".node.log"				#
																#
																#
VERBOSITY							= 5							#
																#
LOG_FLAG_ERROR						= 0 						# only Error
LOG_FLAG_WARN						= 1 						# Warn and Error
LOG_FLAG_INFO						= 2 						# Warn, Error and Info
LOG_FLAG_NOFLAG						= 3 						# Warn, Error, Info and NoFlag
LOG_FLAG_BC							= 4 						# Warn, Error, Info, NoFlag and BaliseComunication
																#
																#
UPDATE_WAITING_TIME					= 0.1						#
#################################################################



#################################   GETH   #####################
PORT_RANGE_START 					= 30303
GETH_PORT							= 30303
GETH_NETWORK_ID 					= 1789
GETH_LOG_FILENAME 					= ".geth.log"
GETH_FLAGS 							= ["--nousb"]#, "--nodiscover"]

GETH_MAX_PEER_ENODE_SENT			= 20
GETH_PERCENT_PEER_ENODE_SENT		= 10

GETH_EIGENTRUST_NAME 				= "eigentrust"				# configuration file : .name.json
GETH_EIGENTRUST_SPY 				= True
GETH_DEALER_NAME 					= "dealer"
GETH_DEALER_SPY 					= True
################################################################



#################################   SERVER/CLINET   ############
NODE_TYPE 							= "other"
#NODE_TYPE 							= "tracker"
#NODE_TYPE 							= "client"

FRAME_LENGHT 						= 1024						# prefer power of 2

TRACKER_PORT						= 30302

CLIENT_TIMEOUT						= 10

TRACKERS_LIST_FILENAME 				= ".tracker.json"
################################################################


#################################   STATUS   ###################
S_VALID								= 0
S_INITIAL 							= 1
S_ERROR								= 2
S_EXIT 								= 3
################################################################


#################################   BALISE COMMUNICATION   #####

def __BC__auto__():
	if not hasattr(__BC__auto__, "i"):
		__BC__auto__.i = 0
	else:
		__BC__auto__.i += 1
	if (__BC__auto__.i > 255):
		raise "Too much BC code"
	return __BC__auto__.i

# SYSTEM							  00 - FF
BC_ERROR 							= __BC__auto__() 			# 0x00

BC_BEGIN_IDENTITY					= __BC__auto__()			# 
BC_END_IDENTITY						= __BC__auto__()			# 

BC_BEGIN_COMMAND					= __BC__auto__()			# 
BC_END_COMMAND						= __BC__auto__()			# 


# RECEIVED
BC_RECEIVED_ENODE					= __BC__auto__()			# followed by 70 bytes for enode
BC_RECEIVED_PEERS_ENODE				= __BC__auto__()			# followed by 1 bytes for size and size*70 bytes for enodes
BC_RECEIVED_ADDRESS					= __BC__auto__()			# followed by 20 bytes for address
BC_RECEIVED_IM_ADDRESS				= __BC__auto__()			# followed by 20 bytes for address
BC_RECEIVED_EIGENTRUST_ADDRESS		= __BC__auto__()			# followed by 20 bytes for address

# REQUESTED
BC_REQUESTED_PEERS_ENODE			= __BC__auto__()			# 
BC_REQUESTED_IM_ADDRESS				= __BC__auto__()			# 
BC_REQUESTED_EIGENTRUST_ADDRESS		= __BC__auto__()			# 
BC_REQUESTED_ETHER					= __BC__auto__()			# 


BC = dict()
for var in locals().copy():
	if var[:3] == "BC_":
		BC[locals()[var]] = var


################################################################
