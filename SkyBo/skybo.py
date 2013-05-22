'''
Created on May 19, 2013

@author: daniel
'''
import Skype4Py
import logging
import time
import shlex
import utils
import scripthandler
import config

logger = logging.getLogger("skybo")
class SkyBo:

    def __init__(self):
        self.running = False
        self.scriptHandler = scripthandler.ScriptHandler()
        
    def start(self):
        """
        Used to start the bot to listen for incoming messages
        """ 
        logger.debug("Creating skype...")
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        logger.debug("Skype attached.")
        
        self.builtins = self.scriptHandler.load_builtin_functions()
        self.scriptHandler.load_custom_scripts()

        self.running = True
        self.skype.OnMessageStatus = self.handleMessages
        
    #stops responding to messages
    def stop(self):
        """
        Used to stop listening to incoming messages
            
        The bot is still attached to skype    
        """
        logger.debug("Stopping from receiving messages")
        self.running = False
        self.skype.OnMessageStatus = self.doNothing  
    
    def doNothing(self,msg,status):
        pass
    
    def handleMessages(self, msg, status):
        """
        Handle incoming messages
        
        :param msg: Skype4Py ChatMessage object
        :param msg: Status of when skype received the message
        """
        if status != Skype4Py.cmsReceived:
            return;
        
        chat = msg.Chat
        body = utils.ensure_unicode(msg.Body).encode("utf-8")
        commandName, commandArgs = self.parseCommands(body)
        
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
    
    def sendMessage(self, chat_id, msg):
        """
        Send Message to chat
        
        :param chat_id: is the string id of a chat
        
        :param msg: is a UTF-8 encoded string
        """
        try:
            self.chats[chat_id].SendMessage(msg)
            return "Message sent"
        except KeyError:
            raise RuntimeError("No chat %s" % chat_id)
        
        
    def getSkype(self):
        """
        Exposes skype
            
        :return: Active Skype4Py instance
        """
        return self.skype
        
    def parseCommands(self, body): 
        """
        Handles parsing commands
        
        :param body: body of the message
        
        :return commandName: returns the name of the command
        :return commandArgs: returns the arguments of the command
        """
        try:
            words = shlex.split(body, comments=False, posix=True)
        except ValueError:
            return
        
        commandName = words[0]
        commandArgs = words[1:]
        
        if not commandName.startswith(":"):
            return
        
        commandName = commandName[1:]
        return commandName, commandArgs
        

def main():
       
    if config.DEBUG:
        logging.basicConfig(filename=config.LOGFILE, level=logging.DEBUG)
    else:
        logging.basicConfig(filename=config.LOGFILE, level=logging.INFO)

    skybo = SkyBo()
    skybo.start()
    while 1:
        time.sleep(1)
    
if __name__ == '__main__':
    main()
