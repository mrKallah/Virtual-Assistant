import requests
import random

from word2number import w2n
from bs4 import BeautifulSoup

from libs.sound import tts


def randomizer(command, obj_manager):
	"""
    "Heads or tails?"
    "Rock, paper, scissors."
    "Roll a dice."
    "Give me a random number between 9 and 15".
    "pick a card"
    """
	# example_commands = ["heads or tails", "rock, paper, scissor", "roll a dice", "pick a random number between ninety two and fifty seven please", "pick a card"]

	# return_value tells the program that the command was found and thus does not spout "Unknown command: "
	return_value = False

	# if heads of tails, with a random chance say heads or tails
	if "heads or tails" in command:
		return_value = True
		if random.randrange(0, 2) == 1:
			tts("heads", obj_manager)
		else:
			tts("tails", obj_manager)

	# if rock paper and scissor in the command, say with a random chance either rock, paper or scissor
	if ("rock" in command) & ("paper" in command) & ("scissor" in command):
		return_value = True
		selection = random.randrange(0, 3)
		if selection == 0:
			tts("rock", obj_manager)
		elif selection == 1:
			tts("paper", obj_manager)
		else:
			tts("scissor", obj_manager)

	# if roll a dice in command say a random value between 1 and 6
	if "roll a dice" in command:
		return_value = True
		tts(str(random.randrange(1, 7)), obj_manager)

	# If "a random number between" is in the command, try to say a number between the lowest an highest number
	# use a try except as w2n.word_to_num will error if you say something like "hit me with a random number between eggplant and hat"
	# neither eggplant nor hat does a good integer make and so we have to account for the possibility of this
	try:
		if ("a random number between" in command) | ("a number between" in command):
			# remove everything before between
			asd = command[command.find("between ") + len("between "):]

			asd = asd.replace("&", "and")

			# assign the numbers before and to first and after and to second
			first = asd[:asd.find(" and ")]
			second = asd[asd.find(" and ") + len(" and "):]

			# convert from words to number if they are words
			first = int(w2n.word_to_num(first))
			second = int(w2n.word_to_num(second))

			# make sure random range gets the numbers in the wrong order or you get a ValueError
			if first < second:
				tts(str(random.randrange(first, second + 1)), obj_manager)
			else:
				tts(str(random.randrange(second, first + 1)), obj_manager)
			return_value = True

	except ValueError:
		None

	# if pick a card in the command, choose a random combination of card ranks and suits (13 ranks, 4 suits)
	if ("pick a card" in command) | ("pick a random card" in command):
		card_points = ['Ace of', 'King of', 'Queen of', 'Jack of', 'Ten of', 'Nine of', 'Eight of', 'Seven of',
		               'Six of', 'Five of', 'Four of', 'Three of', 'Two of']
		card_signs = [' Clubs', ' Diamonds', ' Hearts', ' Spades']
		tts("{}{}".format(random.choice(card_points), random.choice(card_signs)), obj_manager)
		return_value = True

	return return_value


def get_fact():
	"""
	Gets a fact from a random fact generator site
	:return: a string with a fact
	"""
	try:
		url = 'http://randomfactgenerator.net/'
		# get the source of the webpage on url
		code = requests.get(url)
		plain = code.text
		# create a parser
		s = BeautifulSoup(plain, "html.parser")

		# find all the div elements with id z
		link = s.findAll('div', {'id': 'z'})[0]

		# remove unwanted information
		link = link.getText().replace('<div id="z"> ', "")
		link = link.replace(
			'<br/><br/><a class="twitter-share-button" data-count="horizontal" data-text="The oil used by jewelers to lubricate clocks and watches costs about $3,000 a gallon." data-url="http://www.randomfactgenerator.net?id=1266" href="http://twitter.com/share">Tweet</a><script src="http://platform.twitter.com/widgets.js" type="text/javascript"></script><iframe allowtransparency="true" frameborder="0" scrolling="no" src="http://www.facebook.com/plugins/like.php?href=http%3A%2F%2Fwww.randomfactgenerator.net%3Fid%3D1266&amp;layout=button_count&amp;show_faces=false&amp;width=100&amp;action=like&amp;font=verdana&amp;colorscheme=light&amp;height=21" style="border:none; overflow:hidden; width:100px; height:21px;"></iframe></div>',
			"")
		return link.replace("\nTweet", "")
	except:
		return "Unable to reach the internet where I get all my best facts"


def get_joke():
	"""
	Gets a fact from a random joke generator site
	:return: a string with a joke
	"""
	try:
		url = 'https://icanhazdadjoke.com/'
		# get the source of the webpage on url
		code = requests.get(url)
		plain = code.text
		# create a parser
		s = BeautifulSoup(plain, "html.parser")

		# find all the p elements with class subtitle
		link = s.findAll('p', {'class': 'subtitle'})[0]
		# remove unwanted information
		return str(link).replace('<p class="subtitle">', "").replace("</p>", "")
	except:
		return "Unable to reach the internet where I get all my best jokes"


def get_riddle():
	"""
	Gets a riddle from a a random riddle generator
	:return: a string with a riddle
	"""
	try:
		url = 'https://www.riddles.nu/random'
		# get the source of the webpage on url
		code = requests.get(url)
		plain = code.text
		# create a parser
		s = BeautifulSoup(plain, "html.parser")

		# find all the p elements with class subtitle
		link = str(s.findAll('blockquote', {'': ''})[0])
		riddle = link[len("<blockquote><p>"):link.find('<div style="margin-top:5px;')]
		riddle = riddle.replace("<br/>", "").replace("</p>", "")
		answer = link[link.find('style="display:none;">') + len('style="display:none;">'):link.find('</div></div><small><span>Category:')]

		# remove unwanted information
		return riddle, answer
	except:
		return "Unable to reach the internet where I get all my best riddles"


def interesting_facts_jokes_and_riddles(command, obj_manager):
	return_value = False
	if ("tell me something interesting" in command) | ("tell me a fact" in command) | ("tell me a random fact" in command):
		if random.randint(0, 100) < 10:
			tts("no", obj_manager)
		else:
			tts(get_fact(), obj_manager)
		return_value = True

	if ("tell me a joke" in command) | ("tell me something funny" in command) | ("tell me a random joke" in command):
		tts(get_joke(), obj_manager)
		return_value = True

	if ("tell me a riddle" in command):
		riddle, answer = get_riddle()
		tts(riddle, obj_manager)
		obj_manager["riddle"][0] = True
		obj_manager["riddle"].append(answer)
		return_value = True
		return return_value

	if (obj_manager["riddle"][0]) & (command != ""):
		tts(obj_manager["riddle"].pop(), obj_manager)
		obj_manager["riddle"][0] = False
		return_value = True

	return return_value


def im_daddy(command, obj_manager):
	if "who am i" in command:
		tts("You are my daddy", obj_manager)
		return True
	elif ("who is your creator" in command) | ("who created you" in command):
		tts("You might know my creator as Kallah, but I call him daddy", obj_manager)
		return True
	elif "who is your favorite person" in command:
		tts("my favorite person is my daddy, his name is kallah", obj_manager)
		return True
	else:
		return False