

import	subprocess
import	re
import	os
import 	json
from 	getpass 		import 	getpass


from	constants 		import	*

def create_genesis_file(founderAddress, chainId, chainPeriod, genesisFilename): # founderAddress on 40 char without "0x"
	genesis 							= dict()
	genesis["config"]						= dict()
	genesis["config"]["chainId"]				= int(chainId)
	genesis["config"]["homesteadBlock"]			= 0
	genesis["config"]["eip150Block"]			= 0
	genesis["config"]["eip150Hash"]				= "0x0000000000000000000000000000000000000000000000000000000000000000"
	genesis["config"]["eip155Block"]			= 0
	genesis["config"]["eip158Block"]			= 0
	genesis["config"]["byzantiumBlock"]			= 0
	genesis["config"]["constantinopleBlock"]	= 0
	genesis["config"]["petersburgBlock"]		= 0
	genesis["config"]["istanbulBlock"]			= 0
	genesis["config"]["clique"]					= dict()
	genesis["config"]["clique"]["period"]			= int(chainPeriod)
	genesis["config"]["clique"]["epoch"]			= 30000
	genesis["nonce"]							= "0x0"
	genesis["timestamp"]						= "0x00000000"
	genesis["extraData"]						= "0x0000000000000000000000000000000000000000000000000000000000000000" + founderAddress + "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
	genesis["gasLimit"]							= "0xffffff"
	genesis["difficulty"]						= "0x1"
	genesis["mixHash"]							= "0x0000000000000000000000000000000000000000000000000000000000000000"
	genesis["coinbase"]							= "0x" + founderAddress
	genesis["alloc"]							= dict()
	genesis["alloc"][founderAddress]					= dict()
	genesis["alloc"][founderAddress]["balance"]			= "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"
	genesis["number"]							= "0x0"
	genesis["gasUsed"]							= "0x0"
	genesis["parentHash"]						= "0x0000000000000000000000000000000000000000000000000000000000000000"

	genesisFile = open("{0}/{1}".format(ROOT, genesisFilename), "w")
	json.dump(genesis, genesisFile, sort_keys = True, indent = 2)
	genesisFile.close()




#check geth version
print("Check geth installation")
proc = subprocess.Popen('''geth version''', shell = True, stdout = subprocess.PIPE)
out, err = proc.communicate(timeout = 5)
out = out.decode('UTF-8').split('\n')
if ("Geth" not in out[0]):
	raise NameError("geth seems uninstalled")

print("\t{0}".format(out[1]))
print()



print("Check contract sources")
#check contract sources
if not os.path.isfile("{0}/{1}/{2}.sol".format(ROOT, CONTRACT_SOURCES_FOLDER, GETH_EIGENTRUST_NAME)):
	raise NameError("{0} source not found".format(GETH_EIGENTRUST_NAME))
print("\tEigenTrust contract   OK")
if not os.path.isfile("{0}/{1}/{2}.sol".format(ROOT, CONTRACT_SOURCES_FOLDER, GETH_DEALER_NAME)):
	raise NameError("{0} source not found".format(GETH_DEALER_NAME))
print("\tDealer contract       OK")
print()




# set username
print("Create founder account (lowercase lettre only [a-z])")
username = ""
while (username == "" or bool(re.compile(r'[^a-z]').search(username))):
	username = input("\tNew account - username : ")

# create founder password file
p1 = "1"
p2 = "2"
while (p1 != p2) :
	p1 = getpass("\tNew account - password : ")
	p2 = getpass("\tNew account -   repeat : ")

passFile = open("{0}/.tmp".format(ROOT),"w")
passFile.write(p1)
passFile.close()

# create founder account
proc = subprocess.Popen("""geth --datadir {0}/eth_{1}/ --password {0}/.tmp account new""".format(ROOT, username),shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out,err = proc.communicate(timeout = 5)
founderAddress = out.decode('UTF-8')[60:100].lower()

# delete founder passfile
proc = subprocess.Popen("""rm {0}/.tmp""".format(ROOT), shell = True, stdout = subprocess.PIPE)
out, err = proc.communicate(timeout = 5)

print("\tAccount created : {0}-0x{1}".format(username, founderAddress))
print()


# create genesis file
print("Create genesis file")
chainId 		= int(input("\tidentifier [{0}] : ".format(DEFAULT_CHAIN_ID)) or DEFAULT_CHAIN_ID)
chainPeriod 	= int(input("\tperiod [{0}s] : ".format(DEFAULT_CHAIN_PERIOD)) or DEFAULT_CHAIN_PERIOD)
genesisFilename = input("\tfile name [{0}] : ".format(DEFAULT_GENESIS_FILENAME)) or DEFAULT_GENESIS_FILENAME

create_genesis_file(founderAddress, chainId, chainPeriod, genesisFilename)
print("\tGenesis file completed")
print()


print("Geth initialization")
proc = subprocess.Popen('''geth --datadir {0}/eth_{1}/ init {0}/{2}'''.format(ROOT, username, genesisFilename),shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out, err = proc.communicate(timeout = 5)
