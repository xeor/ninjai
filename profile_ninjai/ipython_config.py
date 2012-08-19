c = get_config()
app = c.InteractiveShellApp

# Merge in the base config. If the use have some very generic stuff in there..
load_subconfig('ipython_config.py', profile='default')

# This works just like the generic IPython prompt setting, except it supports {PromptClass} where
# PromptClass is a class that is subclassing the PromptHandler class. This class have access to
# TerminalInteractiveShell, and whatever its prompt() function returns is replaced with its place in
# the prompt variable. Since we are dynamicly building our prompt like this, you can also set colors
# and other magic (like \u@\h), in your class.
c.Ninjai.prompt = u'{GenericPrompt}'

# NOTE; All prompt logic is handeled by the extension called ninjai! Setting it here will have no effect.
#  c.PromptManager.in_template = r''
#  c.PromptManager.in2_template = r''
#  c.PromptManager.out_template = r''

c.PromptManager.justify = True
c.TerminalIPythonApp.display_banner=False

c.InteractiveShell.separate_in = ''
c.InteractiveShell.separate_out = ''
c.InteractiveShell.separate_out2 = ''

c.PrefilterManager.multi_line_specials = True

# The extension doing all the work
c.InteractiveShellApp.extensions += ['ninjai',]

lines = """
%rehashx
"""

# You have to make sure that attributes that are containers already
# exist before using them.  Simple assigning a new list will override
# all previous values.
if hasattr(app, 'exec_lines'):
    app.exec_lines.append(lines)
else:
    app.exec_lines = [lines]

# Load personal configs from the users overwriting every other config if they want..
load_subconfig('config.py')
