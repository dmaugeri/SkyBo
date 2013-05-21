'''
Created on May 20, 2013

@author: daniel
'''
import unixscript
import config
import logging
import os
import builtinfunctions
import inspect

logger = logging.getLogger("skybo")
class ScriptHandler:
    '''
    A class used for loading scripts
    '''
    def __init__(self):
        '''
        Constructor
        '''   
        #used so the same script isn't included twice with config COMMANDS and CUSTOM_UNIX_SCRIPTS
        self._paths = set([])
        self._scripts = {}
    
    def load_script(self, filename, path, command):
        """
        Basic function to load a script 
        
        :param filename: filename of the script
        :param path: path of the script
        :param command: command to run the script
        
        :return: an instance of a unix script wrapper that can be run
        """
        if unixscript.UNIXScript.isValid(self, path):
            return unixscript.UNIXScript(filename, path, command)
        else:
            raise RuntimeError('Script: %s cannot be executed' %(filename))
        
    def _loadCommands(self):
        """
        Loads all Commands in the config.COMMANDS variable, if the variable doesn't exist in the config file
        just return and warn the user
        
        :return: True if COMMANDS exists and has values in it otherwise False
        """
        
        logger.debug("loading all custom commands defined in COMMANDS...")
        commandDict = None
        
        if not 'COMMANDS' in vars(config):
            logger.warn("No COMMANDS variable defined in config")
            return False
        else:
            commandDict = config.COMMANDS 
        
        if not commandDict:
            logger.debug("No custom commands defined in COMMANDS")
            return False
        
        
        commands = commandDict.keys()
        for command in commands:
            path = commandDict[command]
            filename = os.path.split(path)[1]
            self._paths.add(path)
            self._scripts[command] = self.load_script(filename, path, command)
            logger.info('Loaded script: %s with command: %s' %(filename, command))            
        
        logger.debug("Finished loading custom commands.")
        return True
    
    def load_builtin_functions(self):
        """
        Loads all built in functions that are runnable
        
        :returns: a dictionary with all built in functions
        """
        
        members = inspect.getmembers(builtinfunctions, inspect.isfunction)
        self.builtins  = {}
        for member in members:
            self.builtins[member[0]] = member[1]
            logger.info('Built in function %s was loaded' %(member[0]))
        return self.builtins
    
    def get_builtin_scripts(self):
        return self.builtins
    
    def load_custom_scripts(self):
        """
        Function used to load all scripts defined in the Config file including
        the COMMANDS variable and CUSTOM_SCRIPTS variable
        
        If there is not 'CUSTOM_SCRIPTS' variable defined sends a warning and returns _scripts which is empty
        
        :return: a dictionary of script instances
        """
        self.unload_scripts()
        self._loadCommands()
        customScripts = None
        
        if not 'CUSTOM_SCRIPTS' in vars(config):
            logger.warn("No CUSTOM_SCRIPTS variable defined in the config")
            return self._scripts
        else:
            customScripts = config.CUSTOM_SCRIPTS
        
        logger.debug("Loading custom scripts from CUSTOM_SCRIPTS")
        for folder in customScripts:
            listing = os.listdir(folder)
            for script in listing:
                fullpath = os.path.join(folder, script)

                if 'COMMANDS' in vars(config) and set([fullpath]) <= self._paths:
                    continue
                
                #to access the file extension use index 1, use this possibly to add support for multiple languages
                filename = os.path.splitext(script)[0]
                script = self.load_script(filename, fullpath, filename)
                self._scripts[filename] = script
                logger.info('Loaded script: %s' %(filename))
        
        logger.debug("Finished loading custom scripts.")
        return self._scripts
    
    def unload_scripts(self):
        """
        Clears the dictionary of scripts
        """
        self._scripts.clear()
        logger.debug("Unloaded all the scripts")
        
    def get_script_by_command(self, command):
        """
        :return: associated script with that command name
        """
        try:
            val = self._scripts[command]
        except KeyError:
            return None
        
        return val
                    
def _callback(result):
    print result
       
def main():
    """
    Test to make sure that i runs the correct scripts with the correct commands
    based off of the config
    """
    
    scriptHandler = ScriptHandler()
    scripts = scriptHandler.load_custom_scripts() 
    command = raw_input('--->')
    while command != 'q':
        try:
            print scripts[command].run([], _callback)
            command = raw_input('--->')
        except KeyError:
            print "Key Error"
            continue

if __name__ == '__main__':
    main()
        