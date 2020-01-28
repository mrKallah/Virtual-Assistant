from libs.date_and_time import *
from libs.program_execution import *
from libs.random import *
from libs.sound import *

implemented = "1. Windows 10\n2. "

keys = ["big bertha", "big birthday", "big brother", "big births", "big birth"]

def exec_commands(command, obj_manager):
	if contains_key(command):
		if (OS != "Windows") & (OS != "Linux"):
			raise ModuleNotFoundError("Support for {} has not yet been implemented, apologies for any inconvenience\nCurrently supported platforms are: \n{}".format(OS, implemented))

		return_value = False
		# if the command is not a string then return
		if command.__class__ != "".__class__:
			return None

		# convert command to lowercase to make comparison easier
		command = command.lower()

		a = interesting_facts_jokes_and_riddles(command, obj_manager)
		b = control_music(command, obj_manager)
		c = toggle_audio_device(command, obj_manager)
		d = get_date_and_time(command, obj_manager)
		e = set_a_timer(command, obj_manager)
		f = start_a_program(keys, command, obj_manager)
		g = im_daddy(command, obj_manager)
		h = randomizer(command, obj_manager)

		# checks if any of the libs fired
		returns = [a, b, c, d, e, f, g, h]
		for r in returns:
			if r == True:
				return_value = True

		# if none of the libs fired, tell the user they input a unknown command
		if return_value == False:
			thread_print("Unknown command: {}".format(command), obj_manager)
	else:
		if command != "":
			if obj_manager["riddle"][0]:
				interesting_facts_jokes_and_riddles(command, obj_manager)

def contains_key(command):
	command = command.lower()
	return_value = False
	for key in keys:
		if key in command:
			return_value = True
	return return_value

if __name__ == "__main__":
	from libs.helper import create_obj_manager

	obj_manager = create_obj_manager()

	commands = []

	# commands = ["set a two second timer", "tell me something interesting", "what day is it", "set a 5 second timer", "toggle audio device", "play music"]

	start_commands = [commands[0]]  #

	while True:
		for c in commands:
			thread_print("command = {}".format(c), obj_manager)
			exec_commands("{} {}".format("big bertha", c), obj_manager)

		thread_print("write a command: ", obj_manager)
		command = input()
		thread_print("{}{}".format(obj_manager["history"].pop(), command), obj_manager)
		exec_commands("{} {}".format("big bertha", command), obj_manager)

