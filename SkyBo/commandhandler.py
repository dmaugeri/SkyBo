'''
Created on May 19, 2013

@author: daniel
'''
import Skype4Py
import utils
import shlex
import logging
import scripthandler

logger = logging.getLogger("skybo") 
class CommandHandler:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        ''' 
        self.scriptHandler = scripthandler.ScriptHandler()
        self.builtins = self.scriptHandler.load_builtin_functions()
        self.scriptHandler.load_custom_scripts()
        
    def handleMessage(self, msg, status):
    
        if status != Skype4Py.cmsReceived:
            return;
        
        chat = msg.Chat
        body = utils.ensure_unicode(msg.Body).encode("utf-8")
        
        try:
            words = shlex.split(body, comments=False, posix=True)
        except ValueError:
            return
        
        commandName = words[0]
        commandArgs = words[1:]
        
        if not commandName.startswith("!"):
            return
        
        commandName = commandName[1:]
        
        script = self.scriptHandler.get_script_by_command(commandName)
        
        if commandName in self.builtins:
            self.builtins[commandName](commandArgs, msg, status, self.scriptHandler)
            logger.info('Running built in command %s with arguments %s' %(commandName, commandArgs))
        elif script:
            
            def scriptCallback(result):
                chat.SendMessage(result)
                
            logger.info('Running command: %s with arguments: %s' %(commandName, commandArgs))
            script.run(commandArgs, scriptCallback)
        else:
            chat.SendMessage('Don\'t know what %s does!' % commandName)