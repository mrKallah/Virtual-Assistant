import datetime
import subprocess
import platform
OS = platform.system()


def get_os():
	return OS


class history:
	def __init__(self, name):
		self.command_history = []
		self.listening = ""
		self.id = datetime.datetime.now().strftime("%H:%M:%S")
		self.name = name

	def update(self):
		if OS == "Windows":
			tmp = subprocess.call('cls',shell=True)
		else:
			tmp = subprocess.call('clear', shell=True)

		size = len(self.command_history)
		if size < 10:
			min = 0
			max = size
		else:
			min = -10
			max = 0

		print("ID = {}".format(self.id))
		print("Name = {}".format(self.name))
		print("Self = {}".format(self))
		for i in range(min, max):
			print(self.command_history[i])
		print(self.listening)

	def _print(self, new):
		self.command_history.append(new)
		self.update()

	def print_listening(self):
		if self.listening == "":
			self.listening = "Listening "

		if self.listening == "Listening ":
			self.listening = "Listening ."

		elif self.listening == "Listening .":
			self.listening = "Listening .."

		elif self.listening == "Listening ..":
			self.listening = "Listening ..."

		elif self.listening == "Listening ...":
			self.listening = "Listening "

		self.update()

def print_listening(history_obj, listener):
	listening = listener[0]
	if listening == "":
		listening = "Listening "

	if listening == "Listening ":
		listening = "Listening ."

	elif listening == "Listening .":
		listening = "Listening .."

	elif listening == "Listening ..":
		listening = "Listening ..."

	elif listening == "Listening ...":
		listening = "Listening "

	listener[0] = listening
	update(history_obj, listener)


def update(command_history, listener):
	if OS == "Windows":
		tmp = subprocess.call('cls',shell=True)
	else:
		tmp = subprocess.call('clear', shell=True)

	size = len(command_history)
	print(size)
	if size < 10:
		min = 0
		max = size
	else:
		min = -10
		max = 0


	for i in range(min, max):
		print(command_history[i])
	print(listener[0])
