'''
Created on May 20, 2013

@author: daniel
'''
import unixscript
import config
import logging
import os

logger = logging.getLogger("skybo")
class ScriptHandler:
    '''
    A class used for loading scripts
    '''
    def __init__(self):
        '''
        Constructor
        '''   
        #used so the same script isn't included twice
        self._paths = set([])
        self._scripts = {}
    
    def load_script(self, filename, path, command):
        
        if unixscript.UNIXScriptModule.isValid(self, path):
            return unixscript.UNIXScriptModule(filename, path, command)
        else:
            raise RuntimeError('Script: %s cannot be executed' %(filename))
        
    def _loadCommands(self):
        
        logger.debug("loading all custom commands defined in COMMANDS...")
        commandDict = None
        
        if not 'COMMANDS' in vars(config):
            logger.warn("No COMMANDS variable defined in config")
            return
        else:
            commandDict = config.COMMANDS 
        
        if not commandDict:
            logger.debug("No custom commands defined in COMMANDS")
            return False
        
        
        commands = commandDict.keys()
        for command in commands:
            path = commandDict[command]
            filename = os.path.split(path)[1]
            print path
            self._paths.add(path)
            self._scripts[command] = self.load_script(filename, path, command)
            logger.info('Loaded script: %s with command: %s' %(filename, command))            
        
        logger.debug("Finished loading custom commands.")
        return True
    
    def load_custom_scripts(self):
        
        self.unload_scripts()
        self._loadCommands()
        
        for folder in config.CUSTOM_UNIX_SCRIPTS:
            listing = os.listdir(folder)
            for script in listing:
                fullpath = os.path.join(folder, script)
                print fullpath
                if 'COMMANDS' in vars(config) and set([fullpath]) <= self._paths:
                    print "test"
                    continue
                
                #to access the file extension use index 1, use this possibly to add support for multiple languages
                filename = os.path.splitext(script)[0]
                print filename
                script = self.load_script(filename, fullpath, filename)
                self._scripts[filename] = script
                logger.info('Loaded script: %s' %(filename))
                
        return self._scripts
    
    def unload_scripts(self):
        self._scripts.clear()           
                    
def callback(result):
    print result
       
def main():
    scriptHandler = ScriptHandler()
    #scriptHandler.load_commands()
    #scripts = scriptHandler.scripts
   
    scripts = scriptHandler.load_custom_scripts()
    command = raw_input('--->')
    print scripts[command].run([], callback)

if __name__ == '__main__':
    main()
        