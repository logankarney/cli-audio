"""PyAudio Example: Play a wave file (callback version)."""

import pyaudio
import wave
import time
import os #used for finding a file
from cli_exceptions import CLI_Audio_Exception

class Player:
    def __init__(self):
        self.currentSong = "Nothing playing."
        self.paused = True
        self.position = 0

    def getCurrentSong(self):
        return self.currentSong

    def pause(self):
        if self.paused == False:
            self.paused = True
           # self.stream.stop_stream()
        else:
            self.paused = False
            #self.stream.start_stream()

    def play(self, track):
        self.paused = False
        ##code for using os functions to see if a file exists found here:
        ##https://therenegadecoder.com/code/how-to-check-if-a-file-exists-in-python/

        exists = os.path.isfile('/media/'+track)
        if exists:
            self.currentSong = track
            self.wf = wave.open(track, 'rb')
        else:
            raise CLI_Audio_Exception.CLI_Audio_File_Exception("That file doesn't exist, or was spelled incorrectly")

        # instantiate PyAudio (1)
        self.p = pyaudio.PyAudio()

        # open self.stream using callback (3)
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
           channels=self.wf.getnchannels(),
           rate=self.wf.getframerate(),
           output=True,
           stream_callback=self.callback)

        # start the self.stream (4)
        self.stream.start_stream()

    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.wf.close()

        self.p.terminate() 

    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

