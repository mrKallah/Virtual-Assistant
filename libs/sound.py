import os


from gtts import gTTS
from playsound import playsound

from libs.helper import OS, thread_print

if OS == "Windows":
	import win32api

if OS == "Linux":
	None


def tts(text, obj_manager):
	"""
	Text to speech, input text outputs speech
	:param text: a string that will be read up
	:return: Null
	"""
	# if its not run from a test
	if obj_manager["tests"][0] == False:
		file_name_win = "audio\\tts.mp3"
		file_folder_lin = "audio"
		file_name_lin = "tts"
		file_ext_lin = "mp3"  # this should always be mp3

		# create a text to speech object with language English using Google API

		text_to_speech = gTTS(text=text, lang='en', slow=False)

		# save the object to an mp3 file

		# play the file out loud
		if OS == "Windows":
			text_to_speech.save(file_name_win)
			thread_print(text, obj_manager)
			playsound(file_name_win, block=True)
			os.remove(file_name_win)
		else:
			# text_to_speech.save(file_name_lin)
			file = "%s.{}".format(file_ext_lin) % os.path.join(file_folder_lin, file_name_lin)
			text_to_speech.save(file)
			playsound(file, block=True)
			os.remove(file)
	else:
		obj_manager["tests"].append(text)


def control_music(command, obj_manager):
	return_value = False
	if OS == "Windows":
		return_value = control_music_win(command, obj_manager)
	else:
		return_value = control_music_lin(command, obj_manager)
	return return_value


next_song_triggers = ["start the music", "start playing music", "start music", "play music", "play some music",
                      "stop music", "stop the music", "put on some music", "pause music"]
skip_song_trigger = ["next song", "skip"]


def control_music_lin(command, obj_manager):
	return_value = False
	# if the music should be toggled then emulate a play music keyboard press.
	for trigger in next_song_triggers:
		if trigger in command:
			return_value = True
			if "stop" in command:
				tts("stopping music", obj_manager)
			elif "pause" in command:
				tts("pausing music", obj_manager)
			else:
				tts("playing music", obj_manager)

			# get a lsit of all avaliable players
			players = os.popen("playerctl -l").read()
			# convert to array of different devices and remove the last empty string
			players = players.split("\n")[0:-1]

			has_played = False
			for player in players:
				if player in command:
					os.system("playerctl play-pause {}".format(player))
					has_played = True

			if has_played == False:
				os.system("playerctl play-pause")

	# if next song is in string then emulate a skip key keyboard press
	for trigger in skip_song_trigger:
		if trigger in command:
			return_value = True
			tts("skipping current song", obj_manager)

			# get a lsit of all avaliable players
			players = os.popen("playerctl -l").read()
			# convert to array of different devices and remove the last empty string
			players = players.split("\n")[0:-1]
			has_played = False
			for player in players:
				if player in command:
					os.system("playerctl next {}".format(player))
					has_played = True

			if has_played == False:
				os.system("playerctl next")

	return return_value


def control_music_win(command, obj_manager):
	return_value = False
	# if the music should be toggled then emulate a play music keyboard press.
	for trigger in next_song_triggers:
		if trigger in command:
			return_value = True
			if "stop" in command:
				tts("stopping music", obj_manager)
			elif "pause" in command:
				tts("pausing music", obj_manager)
			else:
				tts("playing music", obj_manager)

			vk_media_play_pause = 0xB3
			hardware_code = win32api.MapVirtualKey(vk_media_play_pause, 0)
			win32api.keybd_event(vk_media_play_pause, hardware_code)

	# if next song is in string then emulate a skip key keyboard press
	for trigger in skip_song_trigger:
		if trigger in command:
			return_value = True
			tts("skipping current song", obj_manager)
			vk_media_next_track = 0xB0
			hardware_code = win32api.MapVirtualKey(vk_media_next_track, 0)
			win32api.keybd_event(vk_media_next_track, hardware_code)

	return return_value


def toggle_audio_device(command, obj_manager):
	if OS == "Windows":
		# if toggle audio device is detected, then toggle audio device.
		if ("audio device" in command) | ("use headset" in command) | ("use speaker" in command) | (
				"you speaker" in command) | ("you headset" in command) | ("play music loud" in command):
			tts("toggling audio device", obj_manager)
			# os.system("C:\\Users\\Kallah\\Dropbox\\projects\\batch\\run_file_from_exe.exe")
			if ("speaker" in command) | ("loud" in command):
				os.system('nircmd setdefaultsounddevice "DSP" 1')
				os.system('nircmd setdefaultsounddevice "DSP" 2')
			elif ("headset" in command) | ("headphones" in command) | ("earphones" in command):
				os.system('nircmd setdefaultsounddevice "China" 1')
				os.system('nircmd setdefaultsounddevice "China" 2')
			else:
				os.system("C:\\Users\\Kallah\\Dropbox\\projects\\batch\\run_file_from_exe.exe")
			return True
	else:
		if ("audio device" in command) | ("use headset" in command) | ("use speaker" in command) | (
				"you speaker" in command) | ("you headset" in command) | ("play music loud" in command):
			thread_print("Toggling audio devices is not yet avaliable on {}".format(OS), obj_manager)