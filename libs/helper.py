import datetime
import subprocess
import platform
import sys

from multiprocessing import Manager

OS = platform.system()


def pycharm_hosted():
	if hasattr(sys.stderr, "isatty") and sys.stderr.isatty():
		return False
	else:
		return True


def get_os():
	return OS


def create_obj_manager(avoid_threads=False, is_test=False):
	"""
	Creates a object manager for shared variables in multi threaded processes
	:param avoid_threads:
	:return:
	"""
	if avoid_threads:
		"""
		Breakpoints are somewhat broken when using multithreading in python (at least in pycharm) so changing to no thread mode for printing.
		This will only be useful if no threads are opened anywhere else
		:return:
		"""
		obj_manager = {}

		output_manager = []
		audio_result = []
		history_obj = []
		listener_obj = []
		riddle_solved = []
		tests_info = []
		test_prints = []
	else:
		manager = Manager()
		obj_manager = manager.dict()

		output_manager = manager.list()
		audio_result = manager.list()
		history_obj = manager.list()
		listener_obj = manager.list()
		riddle_solved = manager.list()
		tests_info = manager.list()
		test_prints = manager.list()


	listener_obj.append("")
	riddle_solved.append(False)
	tests_info.append(is_test)

	obj_manager["output"] = output_manager
	obj_manager["audio"] = audio_result
	obj_manager["history"] = history_obj
	obj_manager["listener"] = listener_obj
	obj_manager["riddle"] = riddle_solved
	obj_manager["tests"] = tests_info
	obj_manager["test_prints"] = test_prints

	return obj_manager


def __update__(obj_manager, from_listening=False):
	# check if run in pycharm or not, if run in pycharm, cls and clear does not work.
	if not obj_manager["tests"][0]:
		if not pycharm_hosted():
			if OS == "Windows":
				tmp = subprocess.call('cls',shell=True)
			else:
				tmp = subprocess.call('clear', shell=True)

			size = len(obj_manager["history"])
			if size > 25:
				obj_manager["history"] = obj_manager["history"][-10:]

			for c in obj_manager["history"]:
				print(c)
			print(obj_manager["listener"][0])
		elif from_listening:
			print(obj_manager["listener"][0])
		else:
			print(obj_manager["history"][0])
			del obj_manager["history"][0]
	else:
		obj_manager["test_prints"].append(obj_manager["history"][0])
		del obj_manager["history"][0]


def thread_print(value, obj_manager):
	obj_manager["history"].append(value)
	__update__(obj_manager)


def print_listening(obj_manager):
	listening = obj_manager["listener"][0]

	if listening == "":
		listening = "Listening "

	elif listening == "Listening ":
		listening = "Listening ."

	elif listening == "Listening .":
		listening = "Listening .."

	elif listening == "Listening ..":
		listening = "Listening ..."

	elif listening == "Listening ...":
		listening = "Listening "

	# removes the current value
	obj_manager["listener"].pop()
	# and replaces it with the enw one
	obj_manager["listener"].append(listening)
	# then updates the command line interface
	__update__(obj_manager, from_listening=True)