import speech_recognition as sr
import numpy as np

from multiprocessing import Process, Manager

from command_test import exec_commands, contains_key
from helper import history

r = sr.Recognizer()
sample_rate = 8000
chunk_size = 128

def listen(audio, history_obj):
	"""
	Listens to the microphone and appending the audio clip to the audio manager.
	:param audio: an multiprocessing manager list
	:return: Null
	"""

	# continue forever to listen to the microphone
	while True:
		try:
			# its slightly more efficient to have a nested while true within the try.
			while True:
				with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
					history_obj[0].print_listening()
					sound_file = r.listen(source, timeout=0.1, phrase_time_limit=20)
					audio.append(sound_file)
		# if an error occurs ignore it and continue
		except sr.WaitTimeoutError:
			None


def translate(audio, history_obj):
	"""
	Translates an audio file stored in a manager list to text using Google API
	:param audio: the audio manager list.
	:return: Null
	"""
	# continue forever to translate audio
	while True:
		try:
			# extract the most recent audio clip from the list
			audio_file = audio.pop()
			# convert it to string
			output = r.recognize_google(audio_file)
			# if something goes wrong set the output to empty string
			if output.__class__ != "".__class__:
				output = ""
		except (IndexError, sr.UnknownValueError) as e:
			# if something goes wrong set the output to empty string
			output = ""

		# if the output is not empty display it to the user
		if output != "":
			history_obj[0].print(": {}".format(output))

		# convert the output to lowercase for easier comparisons
		output = output.lower()

		# check if the key or something close to the key was spoken in the string
		if contains_key(output):
			# if key is present, convert key into command
			exec_commands(output, history)

if __name__ == "__main__":
	hist = history("test")

	manager = Manager()
	audio_result = manager.list()
	history_obj = manager.list()
	history_obj.append(hist)

	history_obj[0].print("Calibrating microphone, please do not talk for 5 seconds...")
	history_obj[0].print("asdasdasd")
	with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
		r.adjust_for_ambient_noise(source, duration=5)
	r.dynamic_energy_threshold = True
	history_obj[0].print("Calibrated")

	size = (10, 10, 3)
	on = np.ones(size)
	off = np.zeros(size)

	p = Process(target=listen, args=(audio_result, history_obj))
	p.start()
	p = Process(target=translate, args=(audio_result, history_obj))
	p.start()
	history_obj[0].print("Listening ...")
	p.join()