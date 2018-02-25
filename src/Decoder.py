# start imports
import fnmatch
import numpy as np
import os, sys, inspect
from pydub import AudioSegment


cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"subfolder")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
# end imports


"""
Class that is mainly responsible for decoding an audio file
"""
class Decoder(object):

    '''
    Function that reads any file supported by pydub (ffmpeg) and returns the data contained within. 

    Param:
      - limit (optional): the limit of amount of seconds from the start of the file

    Returns:
      - channels of the given file
      - sample rate
    '''
    def read(self, filename, limit=-1):
        
        # Retrieve audio file
        audiofile = AudioSegment.from_file(filename)

        # Truncate audio file if limit is provided
        if limit and limit != -1:
            audiofile = audiofile[:limit * 1000]

        # Dump the data into np array
        data = np.fromstring(audiofile._data, np.int16)

        print ("  Data shape ", data.shape)

        channel_count = audiofile.channels
        print ("  Channel count = ", channel_count)

        channels = []
        for ch in range(channel_count):
            channels.append(data[ch::audiofile.channels])

        fs = audiofile.frame_rate
        print ("  Framerate = ", fs)

        return channels, fs

    '''
    Method that finds and returns the file names in the given path within extensions
    '''
    def find_files_in_path(self, path, extensions):
        # Remove any . in extensions
        extensions = [e.replace(".", "") for e in extensions]
        for dirpath, dirnames, files in os.walk(path):
            for extension in extensions:
                for f in fnmatch.filter(files, "*.%s" % extension):
                    p = os.path.join(dirpath, f)
                    yield (p, extension)
