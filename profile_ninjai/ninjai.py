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

from IPython.utils.traitlets import Int, Float, Unicode, Bool, CUnicode


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
    """

    ip = None # In case you need it..
    ninjai = None # Ninjai object; used to get eg configs

    def __init__(self, ip=None, ninjai=None):
        self.ip = ip
        self.ninjai = ninjai

    def prompt(self):
        return '{color.Red}Unconfigured prompt'

class TestPrompt(PromptHandler):
    def prompt(self):
        return '{color.Blue}test prompt'

class GenericPrompt(PromptHandler):
    def prompt(self):
        prompt = ''
        prompt += r'{color.LightGreen}\u@\h' # Hostname
        prompt += r'{color.LightBlue}[{color.LightCyan}\Y1{color.LightBlue}]' # Path
        prompt += r'{color.Green}|\#> '
        return prompt

class Prompt(object):
    ip = None
    ninjai = None

    prompts = {}

    def __init__(self, ip=None, ninjai=None):
        self.ip = ip
        self.ninjai = ninjai
        self.populate_prompts()

    def populate_prompts(self):
        # Dynamicly get all classes that inherits the PromptHandler
        classes = [ c for c in inspect.getmembers(sys.modules[__name__]) if (inspect.isclass(c[1]) and issubclass(c[1], PromptHandler))]
        for cls in classes:
            cls_name = cls[0]
            cls_obj = cls[1]

            if cls_obj is PromptHandler:
                continue

            self.prompts[cls_name] = cls_obj(ip=self.ip, ninjai=self.ninjai).prompt()

    def generate_prompt(self):
        prompt_str = self.ninjai.prompt.format(**self.prompts)

        # Need to change self.ip.prompt_manager instead of the config. Changes to self.config.... will have no effect when it is loaded.
        self.ip.prompt_manager.in_template = prompt_str
        self.ip.prompt_manager.in2_template = r'\C_Green|\C_LightGreen\D\C_Green> '
        self.ip.prompt_manager.out_template = '<\#> '


    def pre_command(self, *args):
        # This is the function called each time you hit enter, before the command..
        self.generate_prompt()

    def post_command(self, *args):
        # This is not in use yet, waiting for IPython 0.14 for this..
        pass


class Ninjai(Plugin):
    ip = None

    # Casting version of unicode
    # FIXME; help=... doesn't show up in --help-all, therefor it is left out
    prompt = CUnicode('{GenericPrompt}{TestPrompt}', config=True)

    def __init__(self, ip, config):
        super(Ninjai, self).__init__(shell=ip, config=config)

        self.ip = ip

        self.setup_prompt()
        self.setup_magics()
        self.setup_inline()

    def setup_prompt(self):
        prompt = Prompt(ip=self.ip, ninjai=self)

        # Use 'pre_command_hook' and 'post_command_hook' later, they are available in IPython 0.14dev..?
        # With both of them, we can time commands and have some timing stat in the prompt...

        # Currently, the only thing we have to play with is the pre_prompt_hook..
        self.ip.set_hook('pre_prompt_hook', prompt.pre_command)

    def setup_magics(self):
        self.ip.register_magics(DirectoryMagic(self.ip))

    def setup_inline(self):
        # Will be runned in the ipython user namespace
        self.ip.ex('import os')
        self.ip.ex("def up(): os.chdir('..')")


def load_ipython_extension(ip):
    print 'loaded extension'

    plugin = Ninjai(ip=ip, config=ip.config)

    try:
        ip.plugin_manager.register_plugin('ninjai', plugin)
    except KeyError:
        print("Already loaded")

def unload_ipython_extension(ip):
    print 'unloading'
    ip.plugin_manager.unregister_plugin('ninjai')
