# -*- coding: utf-8 -*-
"""
Ninjai (Ninjai Is Not Just Another IPython-extension) extension to make IPython more friendly as a shell.

Author: Lars Solberg <lars.solberg@gmail.com>
Author: Jack Weaver <jack.weaver@gmail.com>
"""

import inspect
import sys

from IPython.core.plugin import Plugin
from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic
from IPython.core import ipapi

@magics_class
class DirectoryMagic(Magics):
    """
    Placeholder magics..
    """

    ip = None

    def __init__(self, ip):
        super(DirectoryMagic, self).__init__(ip)
        self.ip = ip

    @line_magic
    def lmagic(self, line):
        "my line magic"
        print "Full access to the main IPython object:", self.ip
        print "Variables in the user namespace:", self.ip.user_ns.keys()
        return line

    @cell_magic
    def cmagic(self, line, cell):
        "my cell magic"
        return line, cell

    @line_cell_magic
    def lcmagic(self, line, cell=None):
        "Magic that works both as %lcmagic and as %%lcmagic"
        if cell is None:
            print "Called as line magic"
            return line
        else:
            print "Called as cell magic"
            return line, cell


class PromptHandler(object):
    """
    Return what ever prompt you want with the prompt() function. You can use {color...} or inject
    functions if there is something special with {function_name}. In case you do that, remember to 
    do something like self.ip.user_ns['function_name'] = your_function, first.

    ip - is the active TerminalInteractiveShell object, if you need that.
    priority - is the sort order of your text in the prompt
    """

    ip = None # In case you need it..
    priority = 999 # Defaults to at the end

    def __init__(self, ip):
        self.ip = ip

    def prompt(self):
        return '{color.Red}Unconfigured prompt'

class TestPrompt(PromptHandler):
    def prompt(self):
        return '{color.Blue}test prompt'

class GenericPrompts(PromptHandler):
    priority = 10

    def prompt(self):
        prompt = ''
        prompt += r'{color.LightGreen}\u@\h' # Hostname
        prompt += r'{color.LightBlue}[{color.LightCyan}\Y1{color.LightBlue}]' # Path
        prompt += r'{color.Green}|\#> '
        return prompt

class Prompt(object):
    ip = None
    prompts = []

    def __init__(self, ip):
        self.ip = ip
        self.populate_prompts()

    def populate_prompts(self):
        # Get all classes that inherits the PromptHandler
        classes = [ c[1] for c in inspect.getmembers(sys.modules[__name__]) if (inspect.isclass(c[1]) and issubclass(c[1], PromptHandler))]
        for cls in classes:
            if cls is PromptHandler:
                continue

            cls = cls(self.ip)
            self.prompts.append((cls.priority, cls.prompt))

    def generate_prompt(self):
        prompt_str = ''
        for prompt_obj in sorted(self.prompts):
            prompt_str += prompt_obj[1]()

        # Need to change this, changes to self.config.... will have no effect
        self.ip.prompt_manager.in_template = prompt_str
        self.ip.prompt_manager.in2_template = r'\C_Green|\C_LightGreen\D\C_Green> '
        self.ip.prompt_manager.out_template = '<\#> '


    def pre_command(self, *args):
        # This is the function called each time you hit enter, before the command..
        self.generate_prompt()

    def post_command(self, *args):
        # This is not in use yet, waiting for IPython 0.14 for this..
        pass


class NinjaiPlugin(Plugin):
    ip = None
    config = None

    def __init__(self, ip, config):
        self.ip = ip
        self.config = config # As a read only reference.. Nothing happened on changes

        self.setup_dyna_prompt()
        self.setup_magics()

    def setup_dyna_prompt(self):
        prompt = Prompt(self.ip)

        # Use 'pre_command_hook' and 'post_command_hook' later, they are available in 0.14dev..?
        # Currently, the only thing we have to play with is the pre_prompt_hook..
        self.ip.set_hook('pre_prompt_hook', prompt.pre_command)

    def setup_magics(self):
        self.ip.register_magics(DirectoryMagic(self.ip))

    def testing(self):
        # Will be runned in the ipython user namespace
        self.ip.ex('import os')
        self.ip.ex("def up(): os.chdir('..')")


def load_ipython_extension(ip):
    print 'loaded extension'

    plugin = NinjaiPlugin(ip=ip, config=ip.config)
    try:
        ip.plugin_manager.register_plugin('ninjai', plugin)
    except KeyError:
        # FIXME: Need to reload proper here.. Or the prompt will double up...
        print("Already loaded")

def unload_ipython_extension(ip):
    print 'unloading'
