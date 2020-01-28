import speech_recognition as sr

from multiprocessing import Process

from run_commands import exec_commands, contains_key
from libs.helper import print_listening, create_obj_manager, thread_print, pycharm_hosted

r = sr.Recognizer()
sample_rate = 8000
chunk_size = 128

def listen(obj_manager):
	"""
	Listens to the microphone and appending the audio clip to the audio manager.
	:param audio: an multiprocessing manager list
	:return: Null
	"""

	audio = obj_manager["audio"]

	# continue forever to listen to the microphone
	while True:
		try:
			# its slightly more efficient to have a nested while true within the try.
			while True:
				with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
					if not pycharm_hosted():
						print_listening(obj_manager)
					sound_file = r.listen(source, timeout=0.1, phrase_time_limit=20)
					audio.append(sound_file)
		# if an error occurs ignore it and continue
		except sr.WaitTimeoutError:
			None


def translate(obj_manager):
	"""
	Translates an audio file stored in a manager list to text using Google API
	:param audio: the audio manager list.
	:return: Null
	"""
	audio = obj_manager["audio"]

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
			thread_print(": {}".format(output), obj_manager)
			if pycharm_hosted():
				print("Listening ...")

			# add output to obj_manager
			obj_manager["output"].append(output.lower())

if __name__ == "__main__":
	# Create the object manager which enables multiple threads to have access to the same variables
	obj_manager = create_obj_manager()

	thread_print("Calibrating microphone, please do not talk for 5 seconds...", obj_manager)

	# calibrate the mic
	with sr.Microphone(sample_rate=sample_rate, chunk_size=chunk_size) as source:
		r.adjust_for_ambient_noise(source, duration=5)
	# enable constant update for microphone threshold
	r.dynamic_energy_threshold = True

	thread_print("Calibrated", obj_manager)

	# start listening for audio on separate thread
	listener = Process(target=listen, args=(obj_manager, ))
	listener.daemon = True
	listener.start()

	# start translating audio to text if audio exists
	translator = Process(target=translate, args=(obj_manager, ))
	translator.daemon = True
	translator.start()

	# print listening if ran from pycharm but not if ran from command line
	if pycharm_hosted():
		print("Listening ...")

	# look for the key word in the latest text and run libs within that text if found
	while True:
		try:
			output = obj_manager["output"].pop()
			# check if the key or something close to the key was spoken in the string
			if contains_key(output):
				# if key is present, convert key into command
				exec_commands(output, obj_manager)
		except IndexError:
			# if obj_manager["output"] cannot pop then do nothing
			None