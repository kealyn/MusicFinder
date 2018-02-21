
import os
import sys
import src.Decoder as Decoder
'''
Class body for MusicFinder. It defines the constructor and member functions.
'''
class MusicFinder(object):

    '''
    Constructor
    '''
    def __init__(self):
        self.Decoder = Decoder.Decoder()

    '''
    Function that records fingerprints of all files with given extension in the given path
    '''
    def record_fingerprints_directory(self, path, extensions):
        filenames_to_fingerprint = []
        for filename, _ in self.Decoder.find_files_in_path(path, extensions):
            filenames_to_fingerprint.append(filename)

        print ("Recording fingerprints from [", path, "] for all extensions: ", extensions)
        print ("Files to process (total: ", len(filenames_to_fingerprint), ")")
        print ("---------------------------------------------------------")
        print ("\n".join(filenames_to_fingerprint))
        print ("---------------------------------------------------------")

        # Process files
        # TODO: This process can be optimized by processing multiple files in parallel
        for file_name in filenames_to_fingerprint:
            self.record(file_name)

    '''
    Function that triggers the recording of the fingerprints for the given file
    '''
    def record(self, filename, limit=None):
        song_name, extension = os.path.splitext(os.path.basename(filename))
        channels, Fs = self.Decoder.read(filename, limit)

