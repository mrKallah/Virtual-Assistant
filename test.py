import unittest
from io import StringIO
import sys
import time
import warnings

class JSONUnitTests(unittest.TestCase):
    def _test_timers(self):
        warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
        warnings.filterwarnings("ignore", message="the imp module is deprecated")
        from libs.helper import create_obj_manager
        from libs.date_and_time import set_a_timer

        obj_manager = create_obj_manager(avoid_threads=True, is_test=True)
        text = "set a 2 second timer"
        start = time.time()
        set_a_timer(text, obj_manager)
        end = time.time()

        time_expired_within_range = False
        if (end - start > 2) & (end - start < 4):
            time_expired_within_range = True

        self.assertTrue(time_expired_within_range)
        self.assertEqual(obj_manager["tests"].pop(), "setting a 2 seconds timer")

    def _test_helper_get_os(self):
        """
            Tests that "" is equal to ""
        """
        import platform
        from libs.helper import get_os
        OS = platform.system()
        os = get_os()

        self.assertEqual(os, OS)

    def _test_thread_print(self):
        """
            Tests printing is working
        """


        # without threads
        from libs.helper import create_obj_manager, thread_print
        obj_manager = create_obj_manager(avoid_threads=True, is_test=True)

        text = "something"
        thread_print(text, obj_manager)

        self.assertEqual(obj_manager["test_prints"][0], text)

        # with threads
        obj_manager = create_obj_manager(avoid_threads=False, is_test=True)

        text = "something else"
        thread_print(text, obj_manager)
        self.assertEqual(obj_manager["test_prints"][0], text)

    def _test_tts(self):
        from libs.helper import create_obj_manager
        from libs.sound import tts
        obj_manager = create_obj_manager(avoid_threads=True, is_test=True)
        text = "This is a test"
        tts(text, obj_manager)

        self.assertEqual(obj_manager["tests"].pop(), text)

    def _test_random(self):
        who_am_i_q = ["who am i", "who is your creator", "who created you", "who is your favorite person"]
        who_am_i_a = ["You are my daddy", "You might know my creator as Kallah, but I call him daddy", "You might know my creator as Kallah, but I call him daddy", "my favorite person is my daddy, his name is kallah"]
        riddles_and_jokes_q = ["tell me something interesting", "tell me a fact",  "tell me a random fact", "tell me a joke", "tell me something funny", "tell me a riddle", "go on"]

        from libs.helper import create_obj_manager
        from libs.random import im_daddy, interesting_facts_jokes_and_riddles, randomizer
        obj_manager = create_obj_manager(avoid_threads=True, is_test=True)

        for q in range(len(who_am_i_q)):
            im_daddy(who_am_i_q[q], obj_manager)
            self.assertEqual(obj_manager["tests"].pop(), who_am_i_a[q])

        for q in range(len(riddles_and_jokes_q)):
            is_resonably_correct = True
            interesting_facts_jokes_and_riddles(riddles_and_jokes_q[q], obj_manager)
            answer = obj_manager["tests"].pop()
            if answer.__class__ != "".__class__:
                is_resonably_correct = False

            if len(answer) == 0:
                is_resonably_correct = False

            if answer.replace(".", "").replace(",", "").replace("\n", "").replace("\r", "").replace("\t", "").replace("!", "") == "":
                is_resonably_correct = False

            self.assertTrue(is_resonably_correct)


        for i in range(10):
            randomizer("heads or tails", obj_manager)
            a = obj_manager["tests"].pop()
            is_resonably_correct = False
            if (a == "heads") | (a == "tails"):
                is_resonably_correct = True
            else:
                print("a = '{}'".format(a))
            self.assertTrue(is_resonably_correct)

        for i in range(10):
            randomizer("rock paper scissors", obj_manager)
            a = obj_manager["tests"].pop()
            is_resonably_correct = False
            if (a == "rock") | (a == "paper") | (a == "scissor"):
                is_resonably_correct = True
            else:
                print("a = '{}'".format(a))
            self.assertTrue(is_resonably_correct)

        for i in range(10):
            randomizer("roll a dice", obj_manager)
            a = obj_manager["tests"].pop()
            self.assertTrue(0 <= int(a) <= 6)

        rand_num_between = ["give me a random number between ninety two and fifty seven", "pick a random number between ninety two and fifty seven please", "choose a number between 57 & 92", "choose a number between fifty seven & 92", "choose a number between 57 and ninety two"]
        for i in range(2):
            for r in rand_num_between:
                randomizer(r, obj_manager)
                a = obj_manager["tests"].pop()
                self.assertTrue(57 <= int(a) <= 92)

        for i in range(10):
            found = False
            card_points = ['Ace of', 'King of', 'Queen of', 'Jack of', 'Ten of', 'Nine of', 'Eight of', 'Seven of',
                           'Six of', 'Five of', 'Four of', 'Three of', 'Two of']
            card_signs = [' Clubs', ' Diamonds', ' Hearts', ' Spades']
            randomizer("pick a card", obj_manager)
            a = obj_manager["tests"].pop()
            for i in range(len(card_points)):
                for j in range(len(card_signs)):
                    if a == "{}{}".format(card_points[i], card_signs[j]):
                        found = True
            self.assertTrue(found)

    def _test_date_and_time(self):
        warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
        warnings.filterwarnings("ignore", message="the imp module is deprecated")
        import datetime
        import calendar
        import time
        from num2words import num2words
        from libs.helper import create_obj_manager
        from libs.date_and_time import get_date_and_time
        obj_manager = create_obj_manager(avoid_threads=True, is_test=True)
        qs = ["what is the day, date and time", "what is the time and date",
              "what is the day and date today", "what's the time and date",
              "what day is it today", "what is the time", "what date is it today"]

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = days[datetime.datetime.today().weekday()]
        current_time = time.strftime("%H:%M:%S", time.localtime())

        date_today = num2words(datetime.date.today().strftime("%d"), to='ordinal')
        month = datetime.date.today().strftime("%B")
        year = datetime.date.today().strftime("%Y")

        full_date = "{} of {}, {}".format(date_today, month, year)

        one = "The time is {} on {} the {}".format(current_time, day, full_date)
        two = "The time is {} on the {}".format(current_time, full_date)
        three = "It is {} the {}".format(day, full_date)
        four = "The time is {} on the {}".format(current_time, full_date)
        five = "It is {}".format(day)
        six = "The time is {}".format(current_time)
        seven = "Today is the {}".format(full_date)
        answers = [one, two, three, four, five, six, seven]

        for i in range(len(qs)):
            if (i == 4) & (day == "Wednesday"):
                # this plays a sound using the sound playing library
                self.assertEqual(obj_manager["tests"].pop(), "Wednesday my dude")
            else:
                get_date_and_time(qs[i], obj_manager)
                self.assertEqual(obj_manager["tests"].pop(), answers[i])


if __name__ == '__main__':
    unittest.main()

# manual tests:
    # Testing alarm sound
    # Testing sound from tts
    # Testing its Wednesday my dude
    # Testing turning alarm off
    # Testing taking input while on the timer
    # music control
    # starting programs

