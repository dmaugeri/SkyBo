'''
Created on May 19, 2013

@author: daniel
'''

import managedthread
import logging
import config
import os

logger = logging.getLogger("skybo")
class UNIXScript:
    
    """
    class that represents a unix script
    """
    
    def __init__(self, filename, path, command):
        self.name = filename
        self.path = path
        self.command = command
        
    @staticmethod
    def isValid(self, path):
        """
        :return: whether it's possible to execute the file
        """
        return os.access(path, os.X_OK)
        
    def run(self, args, callback):
        """
        Method to run the unix script
        
        :param msg: is the skype msg object that told the bot to run the command
        :param args: is the arguments sent to the message it must be an array
        :param callback: is the callback function that gets executed after the command finishes running
                it must have a value as a parameter that represents the result
        """
        args.insert(0, unicode(self.path))
        
        timeout = 0
        
        if not 'TIMEOUT' in vars(config):
            logger.warn("No TIMEOUT variable located in config")
        else:
            timeout = config.TIMEOUT
            
        default = 'Command %s timed out in %s seconds' % (self.name, timeout)
        thread = managedthread.ManagedExecThread(args, default, timeout, callback)
        thread.Run()        
   
def _callback(val):
    print val
         
def main():
    """
    Before running main to test the module make sure every instance of msg in UNIXScript.run()
    is timed out because it expects a Skype4Py message instance
    """
    unix = UNIXScript("listing", "ls", "ls")
    unix.run(["-l"], _callback)
        
if __name__ == '__main__':
    main()