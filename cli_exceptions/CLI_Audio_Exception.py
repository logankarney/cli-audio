class CLI_Audio_Exception(Exception):
    """ Base class for exceptions in CLI_Audio """
    def __init__(self, error):
        self.error = error

class CLI_Audio_File_Exception(CLI_Audio_Exception):
    """ Exception raised when a flie does not exist """
#    super().__init__("That file does not exist")
    pass

class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    """ Exception raised when the screen is too small """
#    super().__init__("The screen is too small")
    pass
