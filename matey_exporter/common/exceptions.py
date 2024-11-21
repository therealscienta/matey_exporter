
class MateyQueryAndProcessDataError(Exception):
    """Exception raised for custom error in the application."""
    
    def __init__(self, instance_name:  str, error: str):
        self.instance_name = instance_name
        self.error = error
        
    def __str__(self):
        return f"{self.instance_name} - {self.error.__class__.__name__}: {self.error}"