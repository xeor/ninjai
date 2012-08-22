ninjai
======

Ninjai Is Not Just Another Ipython-extension


Installation
============

* Create a sh (currently pysh) profile in IPython using 'ipython --profile pysh'
* Append this 3 lines to the profile; nano $(ipython locate profile pysh)/ipython_config.py

    import sys
    sys.path.append('/home/user/path/to/ninjai')
    c.InteractiveShellApp.extensions = ['ninjai',]
