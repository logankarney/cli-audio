import Exception

class CLI_Audio_Exception(Exception):
    """ Base class for exceptions in CLI_Audio """
    pass

class CLI_Audio_File_Exception(CLI_Audio_Exception):
    """ Exception raised when a flie does not exist """
    super().__init__("That file does not exist")
