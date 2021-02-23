

import	subprocess
import	re
import	os
import 	json
from 	getpass 		import 	getpass


from	constants 		import	*




#check geth version
print("Check geth installation")
proc = subprocess.Popen('''geth version''', shell = True, stdout = subprocess.PIPE)
out, err = proc.communicate(timeout = 5)
out = out.decode('UTF-8').split('\n')
if ("Geth" not in out[0]):
	raise NameError("geth seems uninstalled")

print("\t{0}".format(out[1]))
print()



print("Check genesis file")
genesisFilename = input("\tfile name [{0}] : ".format(DEFAULT_GENESIS_FILENAME)) or DEFAULT_GENESIS_FILENAME
if not os.path.isfile("{0}/{1}".format(ROOT, genesisFilename)):
	raise NameError("{0} source not found".format(genesisFilename))
print()




# set username
print("Create user account (lowercase lettre only [a-z])")
username = ""
while (username == "" or bool(re.compile(r'[^a-z]').search(username))):
	username = input("\tNew account - username : ")

# create user password file
p1 = "1"
p2 = "2"
while (p1 != p2) :
	p1 = getpass("\tNew account - password : ")
	p2 = getpass("\tNew account -   repeat : ")

passFile = open("{0}/.tmp".format(ROOT),"w")
passFile.write(p1)
passFile.close()

# create user account
proc = subprocess.Popen("""geth --datadir {0}/eth_{1}/ --password {0}/.tmp account new""".format(ROOT, username),shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out,err = proc.communicate(timeout = 5)
founderAddress = out.decode('UTF-8')[60:100].lower()

# delete user passfile
proc = subprocess.Popen("""rm {0}/.tmp""".format(ROOT), shell = True, stdout = subprocess.PIPE)
out, err = proc.communicate(timeout = 5)

print("\tAccount created : {0}-0x{1}".format(username, founderAddress))
print()


print("Geth initialization")
proc = subprocess.Popen('''geth --datadir {0}/eth_{1}/ init {0}/{2}'''.format(ROOT, username, genesisFilename),shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out, err = proc.communicate(timeout = 5)
