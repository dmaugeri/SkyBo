'''
Created on May 19, 2013

@author: daniel
'''

"""
TIMEOUT the amount of allotted time in seconds given to
a script to run before the bot kills the script
"""
TIMEOUT = 60

"""
CUSTOM_UNIX_SCRIPTS is the path to custom unix scripts
that you want the bot to execute
"""
CUSTOM_UNIX_SCRIPTS = ["~/bin", "/usr/bin"]


"""
COMMANDS is variable that allows you to customize your commands that the bot has
and which script should be run. If COMMANDS is not defined it just takes all scripts
under CUSTOM_UNIX_SCRIPTS and the command to run them is the name of the script
in which case just set COMMANDS = {}
"""
COMMANDS = {"command": "/home/daniel/bin/helloworld.sh"}

"""
LOGFILE is the variable that allows where the logfile should be saved
"""
LOGFILE = "logs/skypbo.log"