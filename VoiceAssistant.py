import speech_recognition as sr
import numpy as np

from multiprocessing import Process, Manager

from command_test import exec_commands, contains_key
from helper import update, print_listening

r = sr.Recognizer()
sample_rate = 8000
chunk_size = 128

def listen(audio, history_obj, listener):
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
					print_listening(history_obj, listener)
					sound_file = r.listen(source, timeout=0.1, phrase_time_limit=20)
					audio.append(sound_file)
		# if an error occurs ignore it and continue
		except sr.WaitTimeoutError:
			None


def translate(audio, history_obj, listener):
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
			history_obj.append(": {}".format(output))
			update(history_obj, listener)

		# convert the output to lowercase for easier comparisons
		output = output.lower()

		# check if the key or something close to the key was spoken in the string
		if contains_key(output):
			# if key is present, convert key into command
			exec_commands(output, history_obj, listener)

if __name__ == "__main__":
	manager = Manager()
	audio_result = manager.list()
	history_obj = manager.list()
	listener = manager.list()
	listener.append("")

	history_obj.append("Calibrating microphone, please do not talk for 5 seconds...")
	update(history_obj, listener)

	history_obj.append("asdasdasd")
	update(history_obj, listener)

	with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
		r.adjust_for_ambient_noise(source, duration=5)
	r.dynamic_energy_threshold = True

	history_obj.append("Calibrated")
	update(history_obj, listener)

	size = (10, 10, 3)
	on = np.ones(size)
	off = np.zeros(size)

	p = Process(target=listen, args=(audio_result, history_obj, listener))
	p.start()
	p = Process(target=translate, args=(audio_result, history_obj, listener))
	p.start()
	p.join()
