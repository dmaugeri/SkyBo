'''
Created on May 20, 2013

@author: daniel
'''

def reloadscripts(args, msg, status, scriptHandler):
    commands = scriptHandler.load_custom_scripts()
    builtins = scriptHandler.get_builtin_scripts()
    msg.Chat.SendMessage('These are the commands available:\n%s\n%s' %('\n'.join(commands), 
                                                                       '\n'.join(builtins)))