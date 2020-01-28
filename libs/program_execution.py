import os
import platform

import numpy as np

from libs.sound import tts
from libs.helper import thread_print, OS

if OS == "Windows":
	import win32api

if OS == "Linux":
	None


def get_lin_aliases():
	file = "%s.{}".format("cfg") % os.path.join("programs", "lin_program_aliases")
	f = open(file, 'r')
	lines = f.readlines()
	output = []
	for line in lines:
		line = line.replace("\r", "").replace("\n", "")
		output.append([line[:line.find("=")], line[line.find("=") + 1:line.find(";")], line[line.find(";") + 1:]])
	return output


if OS == "Linux":
	lin_program_aliases = get_lin_aliases()

def start_a_program_win(keys, command, obj_manager):
	# big bertha can you open notepad
	# starts a program from the programs folder using its name
	# the triggers that enables the command to fire
	return_value = False
	triggers = ["open", "start"]
	if "music" in command:
		triggers.remove("start")
	for key in keys:
		for trigger in triggers:
			if trigger in command:
				# remove the key from the command
				command = command.replace("{} ".format(key), "")
				# remove the trigger from the command and anything in front of the trigger
				command = command[command.find(trigger) + len(trigger) + 1:]
				# remove anything that occurs after the first word
				index = command.find(" ")
				if index != -1:
					command = command[:index]

				# tries to start the program
				try:
					os.startfile(r"programs\\{}.lnk".format(command))
					# if the program starts, the TTS command fires
					tts("Starting {}".format(command), obj_manager)
				except FileNotFoundError:
					# if the program is not recognized, print to user
					thread_print("{} is not recognized as a program".format(command), obj_manager)
					return_value = True
	return return_value


def find_command_in_alias_list(command):
	global lin_program_aliases
	lin_program_aliases = np.asarray(lin_program_aliases)
	left = lin_program_aliases[:, 0]
	middle = lin_program_aliases[:, 1]
	right = lin_program_aliases[:, 2]

	if command in left:
		return middle[np.where(command == left)[0][0]], right[np.where(command == left)[0][0]]
	else:
		return command, None


def start_a_program_lin(keys, command, obj_manager, error_mode=0):
	# big bertha can you open notepad
	# starts a program from the programs folder using its name
	# the triggers that enables the command to fire
	return_value = False
	triggers = ["open", "start"]
	if "music" in command:
		triggers.remove("start")
	for key in keys:
		for trigger in triggers:
			if trigger in command:
				# remove the key from the command
				command = command.replace("{} ".format(key), "")
				# remove the trigger from the command and anything in front of the trigger
				command = command[command.find(trigger) + len(trigger) + 1:]
				# remove anything that occurs after the first word
				index = command.find(" ")
				if index != -1:
					command = command[:index]

				# checks for known programs in a list of keywords
				command, tts_command = find_command_in_alias_list(command)

				# tries to start the program
				# >/dev/null 2>&1"

				error_mode = 1

				if error_mode == 0:
					# voids output of command
					sh_command = "{} >/dev/null 2>&1 &".format(command)
				else:
					# runs the command while displaying output, useful for testing
					sh_command = "{} &".format(command)
				if os.system(sh_command) != 32512:
					# if the program starts, the TTS command fires
					if tts_command != None:
						tts("Starting {}".format(tts_command), obj_manager)
					else:
						tts("Starting {}".format(command), obj_manager)
				else:
					# if the program is not recognized, print to user
					thread_print("{} is not recognized as a program".format(command), obj_manager)
					return_value = True
	return return_value


def start_a_program(keys, command, obj_manager):
	if OS == "Windows":
		return_value = start_a_program_win(keys, command, obj_manager)
	else:
		return_value = start_a_program_lin(keys, command, obj_manager)
	return return_value