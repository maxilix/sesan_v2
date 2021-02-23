


class Config():

	def __init__(self,dictionary):
		for key in dictionary:
			if (type(dictionary[key]) == dict):
				setattr(self, key, Config(dictionary[key]))
			else:
				setattr(self, key, dictionary[key])


		


