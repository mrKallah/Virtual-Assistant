import pint
import time
import sys
import threading
import time
import datetime
import calendar
import os
import requests
import random

from bs4 import BeautifulSoup
from word2number import w2n
from playsound import playsound
from multiprocessing import Value, Process, Manager, Pool
from num2words import num2words
from gtts import gTTS
from helper import get_os

OS = get_os()

if OS == "Windows":
	import win32api


if OS == "Linux":
	None

def get_fact():
	url = 'http://randomfactgenerator.net/'
	code = requests.get(url)
	plain = code.text
	s = BeautifulSoup(plain, "html.parser")

	link = s.findAll('div', {'id': 'z'})[0]

	link = link.getText().replace('<div id="z"> ', "")
	link = link.replace(
		'<br/><br/><a class="twitter-share-button" data-count="horizontal" data-text="The oil used by jewelers to lubricate clocks and watches costs about $3,000 a gallon." data-url="http://www.randomfactgenerator.net?id=1266" href="http://twitter.com/share">Tweet</a><script src="http://platform.twitter.com/widgets.js" type="text/javascript"></script><iframe allowtransparency="true" frameborder="0" scrolling="no" src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.randomfactgenerator.net%3Fid%3D1266&amp;layout=button_count&amp;show_faces=false&amp;width=100&amp;action=like&amp;font=verdana&amp;colorscheme=light&amp;height=21" style="border:none; overflow:hidden; width:100px; height:21px;"></iframe></div>',
		"")
	return link.replace("\nTweet", "")


def tell_me_something_interesting(command, history_obj, listener):
	if "tell me something interesting" in command:
		if random.randint(0, 100) < 10:
			tts("no")
		else:
			tts(get_fact())


def emulate_keyboard(command, history_obj, listener):
	if OS == "Windows":
		emulate_keyboard_win(command)
	else:
		raise NameError("Keyboard emulation capabilities are not yet implmented for {}".format(OS))


def emulate_keyboard_win(command, history_obj, listener):
	# if the music should be toggled then emulate a play music keyboard press.
	triggers = ["start the music", "start playing music", "start music", "play music", "play some music", "stop music", "stop the music", "put on some music", "pause music"]
	for trigger in triggers:
		if trigger in command:
			if ("stop" in command) | ("pause" in command):
				tts("stopping music")
			else:
				tts("playing music")

			vk_media_play_pause = 0xB3
			hardware_code = win32api.MapVirtualKey(vk_media_play_pause, 0)
			win32api.keybd_event(vk_media_play_pause, hardware_code)

	# if next song is in string then emulate a skip key keyboard press
	triggers = ["next song", "skip"]
	for trigger in triggers:
		if trigger in command:
			tts("skipping current song")
			vk_media_next_track = 0xB0
			hardware_code = win32api.MapVirtualKey(vk_media_next_track, 0)
			win32api.keybd_event(vk_media_next_track, hardware_code)


def toggle_audio_device(command, history_obj, listener):
	# if toggle audio device is detected, then toggle audio device.
	if ("toggle audio device" in command) | ("change audio device" in command) | ("use headset" in command) | ("use speaker" in command) | ("you speaker" in command) | ("you headset" in command):
		tts("toggling audio device")
		os.system("C:\\Users\\Kallah\\Dropbox\\projects\\batch\\run_file_from_exe.exe")


def start_a_program(keys, command, history_obj, listener):
	# big bertha can you open notepad
	# starts a program from the programs folder using its name
	# the triggers that enables the command to fire
	triggers = ["can you open", "can you start"]
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
					tts("Starting {}".format(command))
				except FileNotFoundError:
					# if the program is not recognized, print to user
					history_obj.append("{} is not recognized as a program".format(command))
					update(history_obj, listener)


def tts(text):
	"""
	Text to speech, input text outputs speech
	:param text: a string that will be read up
	:return: Null
	"""
	# create a text to speech object with language English using Google API
	text_to_speech = gTTS(text=text, lang='en', slow=False)
	# save the object to an mp3 file
	text_to_speech.save("audio\\tts.mp3")
	# play the file out loud
	playsound('audio\\tts.mp3', block=True)
	os.remove('audio\\tts.mp3')


def set_a_timer(command, history_obj, listener):
	# tested scenarios; all working
	# big bertha set a 1 year, 3 month, two weeks, 5-minute and 20 second timer
	# big bertha set a 5-minute and 20 second timer
	# big bertha set a 20 seconds timer
	# big bertha set a 5 seconds timer
	# big bertha set a 2 seconds timer
	# big bertha set a 1 year, 3 month, two weeks, five-minutes and two hundred and three second timer
	def background(exit_value):
		while True:
			if not exit_value:
				playsound("audio\\alarm.mp3")
			else:
				return

	if ("set a " in command) & ("timer" in command):

		# extract time from sentence
		command = command[command.find("set a ") + len("set a "):command.find("timer")]

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

		for i in range(0, timer):
			history_obj.append("time remaning: {}s".format(str(datetime.timedelta(seconds=timer - i))))
			update(history_obj, listener)
			time.sleep(1)

		history_obj.append("time remaning: {}s".format(str(datetime.timedelta(seconds=0))))
		update(history_obj, listener)

		history_obj.append("Times up, type something to turn the alarm off:")
		update(history_obj, listener)

		args = []
		threading1 = threading.Thread(target=background, args=(args,))
		threading1.daemon = True
		threading1.start()
		while True:
			if input() == 'disarm':
				args.append(1)
				break
			else:
				args.append(1)
				break


def get_date_and_time(command, history_obj, listener):
	if ("what day is it" in command) | ("what is the time" in command) | ("what time is it" in command) | ("what date is it" in command) | ("what is the date" in command):
		now = datetime.datetime.now()
		today = datetime.datetime.today()

		# format date and time
		hour_minute = now.strftime("%H:%M")
		month = today.strftime("%B")
		date_today = num2words(today.strftime("%d"), to='ordinal')
		day = calendar.day_name[datetime.datetime.strptime(today.strftime('%d %m %Y'), '%d %m %Y').weekday()]
		year = today.strftime("%Y")

		# if the question is what day is it and its a wednesday play wed.mp3
		if (day == "Wednesday") & ("what day is it" in command):
			playsound('audio\\wed.mp3', block=False)
		else:
			tts("The time is {} on {} the {} of {}, {}".format(hour_minute, day, date_today, month, year))
