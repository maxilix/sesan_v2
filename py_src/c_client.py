import		threading
import		socket
import		time
#import		json
import 		re
import 		tools


from		c_guest 	import		Guest

from 		c_console	import 		console

from		constants 	import 		*



class Cient(threading.Thread):




	##################################################################################################
	#
	#	Constructor
	#
	def __init__(self, username, enodeString, addressString):
		threading.Thread.__init__(self, daemon = True)

		self.status 		= S_INITIAL
		self.username  		= username
		self.enodeString 	= enodeString
		self.addressString 	= addressString
		self.nodekey 		= None
		self.ip 			= None
		self.gethPort 		= None
		self.address 		= None
		self.udpSoc 		= None
		self.trackersList 	= None


		self.peersString	= []
		self.peersConnexion	= False
		#self.tcpSoc 	= None

		# check if there is already a client instance
		for th in threading.enumerate():
			if "[thread]_{0}-client".format(self.username) in th.name :
				console.error("client instance already executed for {0}".format(self.username))
				self.status = S_ERROR
				return
		self.name = "[thread]_{0}-client".format(self.username)



		console.info("client initialized")
		return

	##################################################################################################
	#
	#	run associate thread
	#
	def run(self):
		if (self.status == S_ERROR):
			return

		# check valid enode string
		if tools.check_enode(self.enodeString):
			# extract byte informations
			self.nodekey = int(self.enodeString.split('@')[0][8:],16).to_bytes(64, byteorder='big')
			self.ip = bytes([int(self.enodeString.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)])
			self.gethPort = GETH_PORT.to_bytes(2, byteorder='big')
		else:
			self.status = S_ERROR
			self.end()
			return


		# check valid address string
		if tools.check_address(self.addressString):
			# extract byte informations
			if (self.addressString[:2] == "0x"):
				self.addressString = self.addressString[2:]
			self.address = int(self.addressString,16).to_bytes(20, byteorder='big')
		else:
			self.status = S_ERROR
			self.end()
			return


		# load trackers list
		with open("{0}/{1}".format(ROOT,TRACKERS_LIST_FILENAME),'r') as fd:
			self.trackersList = json.load(fd)







		# Create an UDP based client socket
		self.udpSoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		self.udpSoc.settimeout(UPDATE_WAITING_TIME)
		self.udpSoc.bind(('', CLIENT_PORT));

		self.status = S_VALID
		console.info("client is running")

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
		if (self.udpGuestSoc):
			self.udpGuestSoc.close()

		# Guest managment

		console.info("tracker closed")

	##################################################################################################
	#
	#	update
	#
	def update(self):
		try:
			(frame, contact) = self.udpGuestSoc.recvfrom(FRAME_LENGHT)

			# split frame byte to byte
			frame = list(frame)

			n, frame = self.__identity(frame, contact)
			if   (n == -1):
				return
			elif (frame == []):
				console.warn("no command", who = self.guests[n].who)
				return
			else:
				self.__command(self.guests[n], frame)

		except socket.timeout:
			return
	
	##################################################################################################
	#
	#	stop
	#
	def stop(self):
		self.status = S_EXIT

	##################################################################################################








	def __guest_exist(self, newGuest):
		for n in range(len(self.guests)):
			if (self.guests[n].enode[:64] == newGuest.enode[:64]):
				return n
		return -1 



	def __identity(self, frame, contact):


		valid = False
		newGuest = Guest(self.username)
		console.print("new connexion from {0}:{1}".format(contact[0],contact[1]), who = newGuest.who)


		try:
			if (frame[0] == BC_BEGIN_IDENTITY):
				console.bc(frame[0], who = newGuest.who)
				index = 1
				while (frame[index] != BC_END_IDENTITY):
					console.bc(frame[index], who = newGuest.who)

					if   (frame[index] == BC_ERROR):
						console.warn("identity frame aborted", who = newGuest.who)
						valid = False
						return -1, []
					elif (frame[index] == BC_IDENTITY_USER):
						index += 1
						newGuest.guestType = "user"
						newGuest.enode = frame[index:index+70]
						if ([int(contact[0].split('.')[x]) for x in range(4)] != newGuest.enode[64:68]):
							console.warn("guest's ip doesn't match", who = newGuest.who)
							valid = False
							return -1, []
						index += 70
						valid = True
					elif (frame[index] == BC_IDENTITY_TRACKER):
						index += 1
						newGuest.guestType = "tracker"
						#
						#	code
						#
						valid = True
						console.error("not implemented")
						return -1, []
					else:
						valid = False
						console.warn("invalid balise in identity frame", who = newGuest.who)
						return -1, []
				
				console.bc(frame[index], who = newGuest.who)
				index += 1


				if valid:
					newGuest.udpPyPort = list(contact[1].to_bytes(2, byteorder = 'big'))
					newGuest.update()
					n = self.__guest_exist(newGuest)
					if (n == -1):
						self.guests.append(newGuest)
						n = len(self.guests) - 1
					console.print("identity completed", who = newGuest.who)
					return n, frame[index:]
				else:
					console.warn("incomplete identity", who = newGuest.who)
					return -1, []


			else:
				raise IndexError

		except IndexError:
			console.warn("bad frame construction from {0}:{1}".format(contact[0],contact[1]), who = newGuest.who)
			return -1, []


	def __command(self, guest, frame):
		contact = ("".join(["{0}.".format(guest.ip[x])])[:-1], 255*udpPyPort[0] + udpPyPort[1])

		try:
			if (frame[0] == BC_BEGIN_COMMAND):
				console.bc(frame[0], who = guest.who)
				index = 1
				while (frame[index] != BC_END_COMMAND):
					console.bc(frame[index], who = guest.who)

					if   (frame[index] == BC_ERROR):
						console.warn("command frame aborted", who = guest.who)
						return

					#elif (frame[index] == BC.):

					else:
						console.warn("invalid balise in command frame", who = who)
						return


				console.bc(frame[index], who = guest.who)
				return
			else:
				raise IndexError

		except IndexError:
			console.warn("bad frame construction from {0}:{1}".format(contact[0],contact[1]), who = who)
			return
