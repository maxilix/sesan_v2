import 		threading

from 		constants 	import 		*



class Console():


	def __init__(self, logAbsoluteFileName, verbosity):
		self.logFile = open(logAbsoluteFileName,'w')
		self.verbosity = verbosity
		self.__write(LOG_FLAG_NOFLAG, "log file opened")


	def __del__(self):
		self.__write(LOG_FLAG_NOFLAG, "log file is closing")
		self.logFile.close()




	def error(self, message, who = None):
		if (self.verbosity >= LOG_FLAG_ERROR):
			self.__write(LOG_FLAG_ERROR, message, who = who)
			return

	def warn(self, message, who = None):
		if (self.verbosity >= LOG_FLAG_WARN):
			self.__write(LOG_FLAG_WARN, message, who = who)
			return

	def info(self, message, who = None):
		if (self.verbosity >= LOG_FLAG_INFO):
			self.__write(LOG_FLAG_INFO, message, who = who)
			return

	def print(self, message, who = None):
		if (self.verbosity >= LOG_FLAG_NOFLAG):
			self.__write(LOG_FLAG_NOFLAG, message, who = who)
			return

	def bc(self, b, who = None):
		if (type(b) != int or b < 0 or b > 255):
			self.error("balise must be an integer in [0-255]", who = who)
			return
		balise = BC.get(b,"BC_UNKNOWN_CODE")
		if (self.verbosity >= LOG_FLAG_BC):
			self.__write(LOG_FLAG_BC, "BC code received : {0}".format(balise), who = who)






	def __write(self, flag, message, who = None):

		# flag
		if   (flag == LOG_FLAG_ERROR):
			self.logFile.write("\033[31m [ERROR] \033[0m")
		elif (flag == LOG_FLAG_WARN):
			self.logFile.write("\033[33m  [WARN] \033[0m")
		elif (flag == LOG_FLAG_INFO):
			self.logFile.write("\033[32m  [INFO] \033[0m")
		elif (flag == LOG_FLAG_NOFLAG):
			self.logFile.write("         ")
		elif (flag == LOG_FLAG_BC):
			self.logFile.write("\033[34m[BALISE] \033[0m")
		else:
			raise NameError("[console.py] Flag no supported")

		# who None to string
		if (who == None):
			if (threading.currentThread() == threading.main_thread()): # interpretor thread
				who = "interpretor"
			else:
				who = threading.currentThread().name.split("_")[1]

		# who (string to [string,string])
		if ("-" in who):
			who = who.split("-")[:2]
		else:
			who = ["",who]



		self.logFile.write("{0} ".format(who[0]))

		if ((len(who[0]) + len(who[1]) + 1) > 16):
			self.logFile.write(who[1][:(16 - len(who[0]) - 1 - 4)] + ".." + who[1][-2:])
		else:
			self.logFile.write("".join(" " for i in range(16 - len(who[0]) - 1 - len(who[1]))))
			self.logFile.write(who[1])
		self.logFile.write(" : ")

		# message
		self.logFile.write(message + "\n")

		self.logFile.flush()





console = Console(LOG_FILENAME, VERBOSITY)
