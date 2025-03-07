import re

class MateyQueryAndProcessDataError(Exception):
    '''
    Exception raised for custom error in the application.
    '''
    
    def __init__(self, instance_name:  str, error: str):
        self.instance_name = instance_name
        self.error = error
        
    def __str__(self):
        return f"{self.instance_name} - {self.error.__class__.__name__}: {self.error}"
    
    
class MateyYamlConfigValidationError(Exception):
    '''
    Exception raised for configuration errors in yaml config file.
    '''
    
    def __init__(self, func, error: str):
        error = re.sub(r"'api_key': '\S*',", '', str(error)) # Remove api_key from logging output
        error = re.sub(r"'password': '\S*',", '', str(error)) # Remove password from logging output
        try:
            self.instance_name = error.splitlines()[1].split()[-3] # Get instance name from error message.
            self.error = error.splitlines()[-2]
        except IndexError:
            self.instance_name = 'Unknown'
            self.error = error
        
    def __str__(self):
        return f"instance {self.instance_name} - {self.error.__class__.__name__}: {self.error}"
    
