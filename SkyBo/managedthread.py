'''
Created on May 21, 2013

@author: daniel
'''
import subprocess
import threading
import logging

logger = logging.getLogger("skybo")
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