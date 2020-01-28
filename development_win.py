from run_commands import *
from libs.helper import create_obj_manager, thread_print


keys = ["big bertha", "big birthday", "big brother", "big births", "big birth"]
commands = []


# obj_manager = create_obj_manager()
obj_manager = create_obj_manager(avoid_threads=True)


thread_print("Please enter a command: ", obj_manager)
for c in commands:
	exec_commands("{} {}".format(keys[0], c), obj_manager)

while True:
	exec_commands ("{} {}".format(keys[0], input()), obj_manager)