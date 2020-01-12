from commands import *

implemented = "1. Windows 10\n2. "

keys = ["big bertha", "big birthday", "big brother", "big births", "big birth"]

def exec_commands_win(command, history_obj, listener):
	"""
	Uses the command string to perform actions.
	:param command: a string of commands
	:return: Null
	"""

	# if the command is not a string then return
	if command.__class__ != "".__class__:
		return None

	# convert command to lowercase to make comparison easier
	command = command.lower()

	tell_me_something_interesting(command, history_obj, listener)
	emulate_keyboard(command, history_obj, listener)
	toggle_audio_device(command, history_obj, listener)
	get_date_and_time(command, history_obj, listener)
	set_a_timer(command, history_obj, listener)
	start_a_program(keys, command, history_obj, listener)


def exec_commands_ubuntu(commands, history_obj, listener):
	raise ModuleNotFoundError("Support for {} has not yet been implemented, apologies for any inconvenience\nCurrently supported platforms are: \n{}".format(OS, implemented))


def exec_commands(command, history_obj, listener):
	if contains_key(command):
		if OS == "Windows":
			exec_commands_win(command, history_obj, listener)
		elif OS == "Linux":
			exec_commands_ubuntu(command, history_obj, listener)
		else:
			raise ModuleNotFoundError("Support for {} has not yet been implemented, apologies for any inconvenience\nCurrently supported platforms are: \n{}".format(OS, implemented))
	else:
		history_obj.append("Unknown command: {}".format(command))
		update(history_obj, listener)

def contains_key(command):
	command = command.lower()
	return_value = False
	for key in keys:
		if key in command:
			return_value = True
	return return_value

# if __name__ == "__main__":
# 	from helper import history
# 	history = []
# 	history_obj.append("command testing")
# 	update(history_obj, listener)
# 	while True:
# 		get_commands(input("write a command: "))