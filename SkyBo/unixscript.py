'''
Created on May 19, 2013

@author: daniel
'''

import threading
import logging
import subprocess
import utils
import config
import os

logger = logging.getLogger("skybo")
class UNIXScriptModule:
    
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
        thread = ManagedExecThread(args, default, timeout, callback)
        thread.Run()

class ManagedExecThread(threading.Thread):
    """
    Creates a managed thread that when ran makes sure it runs in a certain timeout period
    """
    
    
    def __init__(self, cmd, default, timeout, callback):
        threading.Thread.__init__(self)
        """
        Thread constructor
        
        :param cmd: is the command being sent to run
        :param default: value that is returned to the callback interface
        :param timeout: is the amount of time the command running has to execute
        :param callback: the callback interface that gets called after the thread is finished running
                it must take in a string a value as a parameter that is a result
        """
        
        self.cmd = cmd
        self.default = default
        self.timeout = timeout
        self.callback = callback
        
    def run(self):
        """
        Creates a subprocess with the supplied command
        and it waits until the process has terminated
        
        This method is not to be run outside of this class
        """
        self.process = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        self.process.wait()
        
    def Run(self):
        """
        Starts the thread, then waits for the thread to terminate for the allotted time
        if the thread is still alive after the timeout warn the user that it has timed out and
        terminate the subprocess and call the callback function
        
        This method is ran outside of the class
        
        if timeout is negative, just run the function
        """
        self.start()
        if self.timeout < 0:
            self.join()
        else:
            self.join(self.timeout)
        
        if self.isAlive():
            logger.warn('The external command timed out')
            self.process.terminate()
            return self.callback(self.default)
        else:
            out = self.process.communicate()[0]
            return self.callback(out)        
        
   
def _callback(val):
    print val
         
def main():
    """
    Before running main to test the module make sure every instance of msg in UNIXScriptModule.run()
    is timed out because it expects a Skype4Py message instance
    """
    unix = UNIXScriptModule("listing", "ls", "ls")
    unix.run(["-l"], _callback)
        
if __name__ == '__main__':
    main()