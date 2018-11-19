import curses
import curses.textpad
import os
import cli_exceptions
import sys

"""  Interactive GUI for the Player, shows what song is currently being played """
class FrontEnd:

    def __init__(self, player):
        ##check the size of the window
        ##code from:https://stackoverflow.com/questions/566746/how-to-get-linux-console-window-width-in-python
        rows, columns = os.popen('stty size', 'r').read().split()
        try:
            if (int(rows) < 24 or int(columns) < 80):
                raise Exception
        except Exception:
            print("Window is too small. Please make it larger.")
            sys.exit()

        self.player = player
        #self.player.play(sys.argv[1])
        curses.wrapper(self.menu)

    def menu(self, args):
        self.stdscr = curses.initscr()
        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(9,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            # When the user selects the 'library' option
            elif c == ord('l'):
                self.listLibrary()
                self.stdscr.touchwin()
                self.stdscr.refresh()
    
    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        #self.player.stop()
        ##try to play song, and catch error if it doesn't exist.
        try:
            self.player.play(path.decode(encoding="utf-8"))
        except CLI_Audio_File_Exception:
            print("***That song doesn't exist, or was typed incorrectly.***")

    def listLibrary(self):
        """ Creates a new window, and displays all .wav files in the media directory  """
        #https://askubuntu.com/questions/98181/how-to-get-screen-size-through-python-curses
        #		answer provided by Timo
        height, width = self.stdscr.getmaxyx()
        changeWindow = curses.newwin(height, width, 0, 0)

        # Adds a border to the Window
        changeWindow.border()
        changeWindow.addstr(0, 0, "Library", curses.A_REVERSE)

        #https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
        #		answer provided by sepp2k
        # Creates an array from the files in media
        arry = os.listdir("media");
        
        #y-value offset
        offset = 0
        for x in range(len(arry)):
            if arry[x].endswith(".wav"):
                changeWindow.addstr(2*offset + 2,1, arry[x]) 
                offset = offset + 1

        # Refreshes the window
        self.stdscr.refresh()

        # Waits for user input before switching back to the main window
        char = changeWindow.getch()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
         

    def quit(self):
        self.player.stop()
        exit()
