# start imports
import numpy as np
import os, sys, inspect
import RunParams
import AbstractRecognizer
import pyaudio
import RunParams

cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# end imports


'''
Class that is mainly responsible for recognizing from microphone
'''
class MicRecorder(object):
    
    '''
    Constructor
    '''
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.data = []
        self.channels = RunParams.Default_Num_Channels
        self.chunksize = RunParams.Default_Width_FFT * 2
        self.samplerate = RunParams.Default_Frequency_Rate
        self.recorded = False

    '''
    Method that starts the recording
    '''
    def start_recording(self):
        print ("Recoding started ...")

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        # Open stream
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.samplerate,
            input=True,
            frames_per_buffer=self.chunksize,
        )

        # Collect data for this chunk
        self.data = [[] for i in range(self.channels)]

    '''
    Method that processes the recordings from the stream and adds to the data
    '''
    def process_recording(self):
        data = self.stream.read(self.chunksize)
        nums = np.fromstring(data, np.int16)
        for c in range(self.channels):
            self.data[c].extend(nums[c::self.channels])

    '''
    Method that stops the recording
    '''
    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.recorded = True
        print ("Recording completed.")

    '''
    API method that returns the recorded data
    '''
    def get_recording(self, seconds):
        self.start_recording()

        # Record and process the data chunk by chunk
        for i in range(0, int(self.samplerate / self.chunksize * seconds)):
            self.process_recording()

        # Stop recording
        self.stop_recording()
        return self.get_recorded_data()

    '''
    Internal method for safety check
    '''
    def get_recorded_data(self):
        if not self.recorded:
            raise NoRecordingError("Recording was not complete/begun")
        return self.data


