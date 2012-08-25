import random

from ninjai import PromptHandler

class TestState(PromptHandler):
    called = 0

    def prompt(self):
        self.called += 1
        return 'call_times(%s)' % (str(self.called))

class TestInfo(PromptHandler):
    def prompt(self):
        return 'prev_command_time(%s)' % str(self.info['starttime'])

class TestColor(PromptHandler):
    def prompt(self):
        str = ''
        str += '{color.Blue}b'
        str += '{color.BlinkGreen}g'
        str += '{color.NoColor}n'
        str += '{color.Red}r'
        str += '{color.Normal}N'
        #str += ''
        return str
class TestRandom(PromptHandler):
    def prompt(self):
        return 'random_int(%s)' % str(random.randint(10, 1000))
