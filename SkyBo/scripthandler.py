'''
Created on May 20, 2013

@author: daniel
'''
import unixscript
import config
import logging
import ntpath

logger = logging.getLogger("skybo")
class ScriptHandler:
    '''
    A class used for loading scripts
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._paths = set([])
        self.scripts = {}
    
    def load_script(self, name, path):
        
        if unixscript.UNIXScriptModule.isValid(self, path):
            return unixscript.UNIXScriptModule(name, path)
        else:
            return None
        
    def load_commands(self):
        
        logger.debug("loading all custom commands defined in COMMANDS...")
        
        if not config.COMMANDS:
            logger.debug("No custom commands defined in COMMANDS")
            return False
        
        
        commands = config.COMMANDS.keys()
        for command in commands:
            path = config.COMMANDS[command]
            self._paths.add(path)
            self.scripts[command] = self.load_script(command, path)            
        
        logger.debug("Finished loading custom commands.")
        return True
         
def callback(result):
    print result
       
def main():
    scriptHandler = ScriptHandler()
    scriptHandler.load_commands()
    scripts = scriptHandler.scripts
    command = raw_input('--->')
    print scripts[command].run("", [], callback)
    

if __name__ == '__main__':
    main()
        