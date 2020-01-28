import datetime
import calendar
import pint
import os
import time

from playsound import playsound
from word2number import w2n
from num2words import num2words
from multiprocessing import Process

from libs.sound import tts
from libs.helper import OS, thread_print

def get_date_and_time(command, obj_manager):
	if ("what" in command) & (("is" in command) | ("'s" in command)):
		if (" time" in command) | (" date" in command) | (" day" in command):
			now = datetime.datetime.now()
			today = datetime.datetime.today()

			# format date and time
			hour_minute = now.strftime("%H:%M:%S")
			month = today.strftime("%B")
			date_today = num2words(today.strftime("%d"), to='ordinal')
			day = calendar.day_name[datetime.datetime.strptime(today.strftime('%d %m %Y'), '%d %m %Y').weekday()]
			year = today.strftime("%Y")


			# date time and day vars
			_d = False
			_t = False
			_D = False
			command = command.replace(",", "").replace(".", "").replace("!", "").replace("?", "")
			# check what to comment on in terms of day date and time
			if " date" in command:
				_d = True
			if " time" in command:
				_t = True
			if " day" in command:
				_D = True

			# logic for replying based on content
			if _d & _t & _D:
				# date time and day
				tts("The time is {} on {} the {} of {}, {}".format(hour_minute, day, date_today, month, year), obj_manager)
			elif _d & _t:
				# date and time
				tts("The time is {} on the {} of {}, {}".format(hour_minute, date_today, month, year), obj_manager)
			elif _d & _D:
				# day and date
				tts("It is {} the {} of {}, {}".format(day, date_today, month, year), obj_manager)
			elif _t & _D:
				# time and date
				tts("The time is {} on {}".format(hour_minute, day), obj_manager)
			elif _D:
				# day
				# if the question is what day is it and its a wednesday play wed.mp3
				if day == "Wednesday":
					playsound(os.path.join("..", "audio", "wed.mp3"), block=False)
					if obj_manager["tests"][0]:
						obj_manager["test_prints"].append("Wednesday my dude")
				else:
					tts("It is {}".format(day), obj_manager)
			elif _t:
				# time
				tts("The time is {}".format(hour_minute), obj_manager)
			else:
				# date
				tts("Today is the {} of {}, {}".format(date_today, month, year), obj_manager)

			return True


def set_a_timer(command, obj_manager):

	if ("set " in command) & ("timer" in command):

		# extract time from sentence
		if command.find("set a ") != -1:
			command = command[command.find("set a ") + len("set a "):command.find("timer")]
		else:
			command = command[command.find("set ") + len("set "):command.find("timer")]

		# streamline plural to singular
		command = command.replace("seconds", "second").replace("minutes", "minute").replace("hours", "hour")
		command = command.replace("weeks", "week").replace("months", "month").replace("years", "year")

		# convert textual numbers from two hundred and three to two-hundred-three to make one number one word
		command = command.replace("-", " ").replace(" and", "").replace(",", "")
		command = command.replace(" second", ".second.").replace(" minute", ".minute.").replace(" hour", ".hour.")
		command = command.replace(" week", ".week.").replace(" month", ".month.").replace(" year", ".year.")
		command = command.replace(" ", "-").replace(".", " ").replace(" -", " ")

		# convert any textual numbers to ints
		output = ""
		for word in command.split(" "):
			try:
				output += "{} ".format(w2n.word_to_num(word))
			except ValueError:
				output += "{} ".format(word)
		command = output

		# concatenate the numerical values to its time unit I.E 1 year 2 month -> 1year 2month
		output = ""
		last = ""
		for i in command:
			try:
				int(last)
				if i != " ":
					output += i
				last = i
			except ValueError:
				output += i
				last = i
		command = output

		# Convert from time units in words to seconds
		unit_reg = pint.UnitRegistry()

		# set init time to 0s
		duration = unit_reg("0seconds")

		for word in command.split(" "):
			try:
				duration += unit_reg(word)
			except pint.errors.DimensionalityError:
				None

		timer = int(duration.magnitude)

		str_time = str(datetime.timedelta(seconds=timer))

		# convert from 2:12:01 to 2 hours 12 minutes 1 second
		# and 0:00:04 to 04 seconds
		output_time = ""
		h = False
		m = False
		for i in range(len(str_time)):
			if (h == False) & (str_time[i] == ":"):
				if str_time[i - 1] == "1":
					output_time += " hour "
				else:
					output_time += " hours "
				h = True
			elif (m == False) & (str_time[i] == ":"):
				if str_time[i - 1] == "1":
					output_time += " minute "
				else:
					output_time += " minutes "
				m = True
			else:
				output_time += str_time[i]

		if str_time[-1] == "1":
			output_time += " second "
		else:
			output_time += " seconds "

		# remove empty values such as 0 minutes
		output_time = output_time.replace("0 hours ", "").replace("0 hour ", "").replace("00 minutes ", "").replace(
			"00 minute ", "")

		# remove any zeroes in the first position, IE 02 seconds -> 2 seconds
		while output_time[0] == "0":
			output_time = output_time[1:]

		tts("setting a {}timer".format(output_time), obj_manager)

		for i in range(0, timer):
			thread_print("time remaning: {}s".format(str(datetime.timedelta(seconds=timer - i))), obj_manager)
			time.sleep(1)

		thread_print("time remaning: {}s".format(str(datetime.timedelta(seconds=0))), obj_manager)

		thread_print("BEEP BEEP BEEP BEEP, type something to turn the alarm off:", obj_manager)

		# do not sound the alarm if it is a test
		if not obj_manager["tests"][0]:
			get_user_input_in_thread(alarm)
		return True


def alarm():
	while True:
		if OS == "Windows":
			playsound("audio//alarm.mp3")
		else:
			file = "%s.{}".format("mp3") % os.path.join("audio", "alarm")
			os.system("mpg123 {} >/dev/null 2>&1".format(file))
		# playsound(file, block=True)


def get_user_input_in_thread(target):
	thread = Process(target=target)
	thread.daemon = True
	thread.start()
	input()
	while thread.is_alive():
		thread.terminate()
		thread.join(timeout=1.0)