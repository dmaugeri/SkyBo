'''
Created on May 19, 2013

@author: daniel
'''
import Skype4Py
import logging

logger = logging.getLogger("skybo")
class SkyBo:

    def __init__(self):
        #keeps track of the chats that the bot has spoken too
        self.running = False

        
    def start(self):
        """
        Used to start the bot to listen for incoming messages
        """ 
        logger.debug("Creating skype...")
        self.skype = Skype4Py.Skype()
        self.skype.Attach()
        logger.debug("Skype attached.")
        
        self.running = True
        self.skype.OnMessageStatus = self.handleMessages
        
    #stops responding to messages
    def stop(self):
        """
        Used to stop listening to incoming messages
            
        The bot is still attached to skype    
        """
        logger.debug("Stopping from receiving messages")
        
        #reset all the chats the bot has spoken too
        self.chats = {}
        self.running = False
        self.skype.OnMessageStatus = self.doNothing     
    
    def doNothing(self,msg,status):
        pass
    
    def handleMessages(self, msg, status):
        """
        Handle incoming messages
        """
        pass
    
    def sendMessage(self, chat_id, msg):
        """
        Send Message to chat
        
        :param: chat_id is the string id of a chat
        
        :param: msg is a UTF-8 encoded string
        """
        try:
            self.chats[chat_id].SendMessage(msg)
            return "Message sent"
        except KeyError:
            raise RuntimeError("No chat %s" % chat_id)
        
        
    def getSkype(self):
        """
        Exposes skype allows for stateful modules
            
        :return: Active Skype4Py instance
        """
        return self.skype
        
        

def main():
    pass
    
if __name__ == '__main__':
    main()