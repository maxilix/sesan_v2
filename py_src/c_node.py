import 		getpass
import 		os
import		threading
import		socket
import		time
import		json
from 		getpass 			import 		getpass


from 		c_geth				import 		Geth
#from		c_client 			import		Client
#from		c_tracker 			import		Tracker
#from		c_config 			import		Config
from		c_guest 			import		Guest
from 		c_console			import 		console

import 		tools
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

		self.udpGuestSoc 	= None
		self.guests 		= []
		self.trackers 		= []


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

		"""
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


		# Create an UDP based socket
		self.udpGuestSoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		self.udpGuestSoc.settimeout(UPDATE_WAITING_TIME)
		port = tools.next_free_port()
		self.udpGuestSoc.bind(('', port));

		console.info("udp socket openned, listenning on {0}".format(port))


		if os.path.isfile("{0}/{1}".format(ROOT, TRACKERS_LIST_FILENAME)):
			with open("{0}/{1}".format(ROOT, TRACKERS_LIST_FILENAME), 'r') as fd:
				trackers = json.load(fd)
			console.info("{0} tracker address loaded".format(len(trackers)))




		self.status = S_VALID
		console.info("node is runing")

		# thread loop
		while (self.status == S_VALID):
			self.update_udp()


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

		if (self.udpGuestSoc):
			self.udpGuestSoc.close()
			console.info("udp socket closed")

		"""
		if (self.tracker):
			self.tracker.stop()
			self.tracker.join()
		if (self.client):
			self.client.stop()
			self.tracker.join()
		"""
		console.info("node closed")

	##################################################################################################
	#
	#	update
	#
	def update_udp(self):
		try:
			(frame, contact) = self.udpGuestSoc.recvfrom(FRAME_LENGHT)

			# split frame byte to byte
			frame = list(frame)

			n, frame = self.__check_identity_frame(frame, contact)
			if   (n == -1):
				return
			elif (frame == []):
				console.warn("no command", who = self.guests[n].who)
				return
			else:
				self.__check_command_frame(self.guests[n], frame)

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
			if (self.guests[n].enodeB[:64] == newGuest.enodeB[:64]):
				return n
		return -1 


	def __check_identity_frame(self, frame, contact):


		valid = False
		newGuest = Guest(self.user[0])
		newGuest.udpContact = contact
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
					elif (frame[index] == BC_RECEIVED_ENODE):
						index += 1
						newGuest.enodeB = frame[index:index+70]
						if (contact[0] != newGuest.ip()):
							console.warn("guest's ip doesn't match", who = newGuest.who)
							valid = False
							return -1, []
						index += 70
						valid = True
					elif (frame[index] == BC_RECEIVED_ADDRESS):
						index += 1
						newGuest.addressB = frame[index:index+20]
						index += 20
					else:
						valid = False
						console.warn("invalid balise in identity frame", who = newGuest.who)
						return -1, []
				
				console.bc(frame[index], who = newGuest.who)
				index += 1


				if (valid and newGuest.update()):
					n = self.__guest_exist(newGuest)
					if (n == -1):
						self.guests.append(newGuest)
						n = len(self.guests) - 1
					else:
						self.guests[n] = newGuest
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


	def __check_command_frame(self, guest, frame):
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



	def __received_frame(self, frame, contact):
		valid 	= False
		who 	= "{0}-newGuest".format(self.user[0])
		console.print("new connexion from {0}:{1}".format(contact[0],contact[1]), who = who)

		try:
			if (frame[0] == BC_BEGIN_IDENTITY):
				console.bc(frame[0], who = who)
				index = 1
				while (frame[index] != BC_END_IDENTITY):
					console.bc(frame[index], who = who)

					if   (frame[index] == BC_ERROR):
						console.warn("identity frame aborted", who = who)
						valid = False
						return
					elif (frame[index] == BC_RECEIVED_ENODE):
						index += 1
						newGuest.enodeB = frame[index:index+70]
						if (contact[0] != newGuest.ip()):
							console.warn("guest's ip doesn't match", who = who)
							valid = False
							return
						index += 70
						#
						#
						#
						valid = True
					else:
						valid = False
						console.warn("invalid balise in identity frame", who = who)
						return
				
				console.bc(frame[index], who = who)
				index += 1


				if (valid):
					#
					#
					#
					console.print("identity completed", who = who)
					return
				else:
					console.warn("incomplete identity", who = who)
					return


			else:
				raise IndexError

		except IndexError:
			console.warn("bad frame construction from {0}:{1}".format(contact[0],contact[1]), who = who)
			return


	def __send_frame(self, contact, commands = []):

		enodeS = self.geth.get_enodeS()

		frame += [BC_BEGIN_IDENTITY]
		frame += [BC_RECEIVED_ENODE]
		frame += self.geth.get_enodeB()
		frame += [BC_END_IDENTITY]

		if commands != []:
			frame += [BC_BEGIN_COMMAND]
			frame += commands
			frame += [BC_END_COMMAND]



